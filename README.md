# Real-Time Chat Application

## Project Description
This project is a simple real-time chat application that allows users to create chat rooms, join existing rooms, and send messages instantly to other users in the same room. The application is designed to be intuitive and functional, making it an excellent foundation for further enhancements.

---

## Features
1. **User Authentication**:
   - Secure sign-up and log-in functionality.
   - Users are uniquely identified during chat sessions.

2. **Chat Room Management**:
   - Create chat rooms with unique codes.
   - Join existing chat rooms using a code.

3. **Real-Time Messaging**:
   - Messages are delivered and displayed instantly to all participants in a room.
   - The chat interface updates dynamically without page refresh.

4. **Room Navigation**:
   - Users can leave a room and join another seamlessly.

5. **Database Management**:
   - SQLite used to store user and room data efficiently.
---

## Technologies Used
- **Backend**:
  - Flask: web framework for Python.
  - Flask-SQLAlchemy: For ORM-based database management.
  - Socket.IO: For handling real-time communication.

- **Frontend**:
  - HTML: simple and functional user interface.

- **Database**:
  - SQLite:  for storing user and chat room data.

---

## Project Structure
```
VibeRoom/
├── templates/             # HTML templates for frontend
│   ├── login.html         # Login page
│   ├── signup.html        # Sign-up page
│   ├── create_or_join_room.html  # Room creation/joining page
│   └── chat.html          # Chat room page
├── instances/             #for the database
│   ├── chat.db            # the database                         
├── run.py                 # Entry point of the application
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

## Installation

Follow these steps to get your development environment up and running.

### Prerequisites

Ensure you have the following installed on your machine:

- Python 3.x
- Flask
- Flask-SocketIO
- SQL database (such as SQLite, MySQL, or PostgreSQL)
---

### Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/yanbel0706/VibeRoom.git
   cd VibeRoom
   ```
 2. Install the required dependencies
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Application
   ```bash
   Python run.py
   ```
4. Open your browser and go to http://localhost:5000 to start using the chat app.
   
---

## Usage Guide
1. **Sign Up**:
   - Enter a unique username and password on the sign-up page.

2. **Log In**:
   - Use your credentials to log in.

3. **Create or Join a Room**:
   - Create a new room with a unique name or join an existing room using its code.

4. **Send Messages**:
   - Type a message and send it to other participants in the room.

5. **Switch Rooms**:
   - Leave the current room and join another one by entering the corresponding room code.

6. **logout**:
   - Click the logout button to log out and return to the login page.

---

---

## Testing with SQLite Browser
You can verify the data in the database using SQLite Browser:
1. Open the database file `chat.db` in SQLite Browser.
2. Inspect the `users` table to confirm user registration.
3. Inspect the `rooms` table to verify created rooms and their participants.
4. Review the `messages` table to check the saved chat messages.

---

## Challenges and Solutions
1. **Real-Time Communication**:
   - Challenge: Implementing instant updates for multiple users.
   - Solution: Used Socket.IO for reliable real-time messaging.

2. **User Session Management**:
   - Challenge: Ensuring unique user sessions.
   - Solution: Incorporated Flask sessions to maintain user state.

---

## Future Enhancements
1. **Private Messaging**: Allow users to send direct messages to specific participants.
2. **Enhanced UI/UX**: Improve the frontend design for better usability.
3. **User Profiles**: Add support for profile pictures and bios.

---

## License
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
