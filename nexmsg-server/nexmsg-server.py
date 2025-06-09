from flask import Flask, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'grim_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")

connected_users = {}

@app.route("/")
def index():
    return "🧬 NEXMSG Server Running - GR!M_Protocol"

@socketio.on('connect')
def on_connect():
    print(f"🔌 Client connected: {request.sid}")

@socketio.on('disconnect')
def on_disconnect():
    username = connected_users.get(request.sid, "Unknown")
    print(f"❌ {username} disconnected.")
    emit('server_message', f"📴 {username} has left the chat.", broadcast=True)
    connected_users.pop(request.sid, None)

@socketio.on('join')
def handle_join(data):
    username = data.get("username", "Anonymous")
    connected_users[request.sid] = username
    emit('server_message', f"✅ {username} joined the chat.", broadcast=True)

@socketio.on('send_message')
def handle_message(data):
    username = connected_users.get(request.sid, "Unknown")
    message = data.get("message", "")
    emit('receive_message', {"username": username, "message": message}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
