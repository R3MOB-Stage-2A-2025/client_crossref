from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS

# To put in a .env file
BACKEND_PORT: int = 5001
BACKEND_SECRETKEY: str = "lol123test!"

app = Flask(__name__)
app.config['SECRET_KEY'] = BACKEND_SECRETKEY
CORS(app, resources={r"/*": { "origins": "*" }})
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on("connect")
def connected():
    """event listener when client connects to the backend"""
    print(f'client number {request.sid} is connected')

@socketio.on('data')
def handle_message(data):
    """event listener when client types a message"""
    print("data from the front end: ", str(data))

@socketio.on("search_query")
def handle_search_query(query: str):
    print(f"Search query received: {query}")

    # For demonstration, dummy "search results":
    users = [
        {"id": 1, "name": "Alice Anderson"},
        {"id": 2, "name": "Bob Brown"},
        {"id": 3, "name": "Charlie Chaplin"},
        {"id": 4, "name": "David Dawson"},
        {"id": 5, "name": "Eve Evans"},
    ]

    results = [
        user for user in users \
        if query.lower() in user["name"].lower() \
    ]

    emit("search_results", { "results": results }, to=request.sid)

@socketio.on("disconnect")
def disconnected():
    """event listener when client disconnects to the backend"""
    print(f'client number {request.sid} is disconnected')

if __name__ == '__main__':
    socketio.run(app, debug=True, port=BACKEND_PORT)

