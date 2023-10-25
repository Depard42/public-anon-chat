from app.app import app, socketio
HOST="0.0.0.0"
PORT=8124

if __name__ == "__main__":
    socketio.run(app, debug=False, host=HOST, port=PORT, allow_unsafe_werkzeug=True)