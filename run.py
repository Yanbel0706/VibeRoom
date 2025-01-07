
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

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
# Créer la base de données et les tables
with app.app_context():
    db.create_all()  # Crée toutes les tables si elles n'existent pas



if __name__ == '__main__':
    socketio.run(app, debug=True)
