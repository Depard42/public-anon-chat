from app.app import app, socketio
HOST="0.0.0.0"
PORT=8124
from werkzeug.middleware.proxy_fix import ProxyFix

app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)

if __name__ == "__main__":
    socketio.run(app, debug=False, host=HOST, port=PORT, allow_unsafe_werkzeug=True)