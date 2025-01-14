
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import random
import string

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yanbel0706'  # Remplacez par une clé secrète sécurisée
socketio = SocketIO(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'  # Fichier SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

# Modèle pour les utilisateurs
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    
# Modèle pour les messages

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Modèle pour les rooms
class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(4), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    users = db.relationship('User', secondary='room_user', backref='rooms_in_user', lazy='subquery')

class RoomUser(db.Model):
    __tablename__ = 'room_user'
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)

# Générer un code de room aléatoire
def generate_room_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))

# Créer la base de données et les tables
with app.app_context():
    db.create_all()  # Crée toutes les tables si elles n'existent pas
@app.route('/')
def index():
    return redirect(url_for('login'))  # Redirection vers la page de création/join de room

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Vérifier si l'utilisateur existe déjà
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Cet utilisateur existe déjà !', 'danger')
            return redirect(url_for('signup'))

        # Hacher le mot de passe
        hashed_password = generate_password_hash(password)

        # Créer un nouvel utilisateur
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        

        flash('Inscription réussie ! Vous pouvez vous connecter maintenant.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Trouver l'utilisateur
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Connexion réussie !', 'success')
            return redirect(url_for('create_or_join_room'))
        else:
            flash('Nom d\'utilisateur ou mot de passe incorrect', 'danger')

    return render_template('login.html')

@app.route('/chat/<room_code>')
def chat(room_code):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    room = Room.query.filter_by(code=room_code).first()

    if room:
        messages = Message.query.filter_by(room_id=room.id).all()
        return render_template('chat.html', room=room, messages=messages)
    else:
        flash('Room not found', 'danger')
        return redirect(url_for('create_or_join_room'))
@app.route('/create_or_join_room', methods=['GET', 'POST'])
def create_or_join_room():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    joined_rooms = [room_user.room for room_user in user.user_rooms]

    if request.method == 'POST':
        if 'create_room' in request.form:
            room_name = request.form['room_name']
            room_code = generate_room_code()

            new_room = Room(name=room_name, code=room_code)
            db.session.add(new_room)
            db.session.commit()

            room = Room.query.filter_by(code=room_code).first()
            new_room_user = RoomUser(room_code=room.code, username=user.username)
            db.session.add(new_room_user)
            db.session.commit()

            flash(f'Room créée avec le code : {room_code}', 'success')
            return redirect(url_for('chat', room_code=room_code))

        elif 'join_room' in request.form:
            room_code = request.form['room_code']
            room = Room.query.filter_by(code=room_code).first()

            if room:
                existing_room_user = RoomUser.query.filter_by(room_code=room.code, username=user.username).first()
                if not existing_room_user:
                    new_room_user = RoomUser(room_code=room.code, username=user.username)
                    db.session.add(new_room_user)
                    db.session.commit()
                    flash(f'Vous avez rejoint la room avec le code : {room_code}', 'success')
                else:
                    flash('Vous avez déjà rejoint cette room', 'info')
                return redirect(url_for('chat', room_code=room_code))
            else:
                flash('Code de room invalide', 'danger')

    return render_template('create_or_join_room.html', joined_rooms=joined_rooms)

@app.route('/quit_room')
def quit_room():
    flash('Vous avez quitté la room', 'info')
    return redirect(url_for('create_or_join_room'))

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    socketio.emit('message', {'user': 'System', 'message': f'{username} a rejoint la room.'}, room=room)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Déconnexion réussie !', 'info')
    return redirect(url_for('login'))

@socketio.on('message')
def handle_message(data):
    user = User.query.get(session['user_id'])
    room = Room.query.filter_by(code=data['room']).first()

    if room:
        message = Message(user_id=user.id, room_id=room.id, content=data['message'])
        db.session.add(message)
        db.session.commit()

        socketio.emit('message', {
            'user': user.username,
            'message': data['message'],
            'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }, room=data['room'])

if __name__ == '__main__':
    socketio.run(app, debug=True)
