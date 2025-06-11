from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS

# To put in a .env file
BACKEND_PORT: int = 5001
BACKEND_SECRETKEY: str = "lol123test!"

app = Flask(__name_)
app.config['SECRET_KEY'] = BACKEND_SECRETKEY
CORS(app, resources={r"/*": { "origins": "*" }})
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route("/http-call")
def http_call():
    data = { 'data': 'HTTP request Hello World!' }
    return jsonify(data)

@socketio.on("connect")
def connected():
    """event listener when client connects to the backend"""
    print(request.sid)
    print("client has connected")
    emit("connect", { "data": f"id: {request.sid} is connected" })

@socketio.on('data')
def handle_message():
    """event listener when client types a message"""
    print("data from the front end: ", str(data))
    emit("data", { 'data': data; 'id': request.sid }, broadcast=True)


@socketio.on("disconnect")
def disconnected():
    """event listener when client disconnects to the backend"""
    print("user disconnected")
    emit("disconnect", f"user {request.sid} disconnected", broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True, port=BACKEND_PORT)

