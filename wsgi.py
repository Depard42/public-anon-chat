from app.app import app, socketio
HOST="127.0.0.0"
PORT=8124

if __name__ == "__main__":
    socketio.run(app, debug=False, host=HOST, port=PORT)