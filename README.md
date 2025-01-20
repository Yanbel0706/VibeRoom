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
   

## Usage

### User Authentication
Users can sign up with a username and password.
After logging in, users can either create or join a room by entering a room code.
Messages are displayed in real-time in the chat room.

### Room Management
To create a new room, enter a unique room code.
To join an existing room, use the room code provided by another user.
Users can send messages to the room, and messages will appear for everyone in real-time.

### Chat Room

Messages from the user appear on the right side of the screen, while messages from other users appear on the left.
The username of the user is displayed next to their message.
The date and time of each message is displayed below the message in a smaller font.
### Logout
Users can log out at any time, which will redirect them to the login page.
