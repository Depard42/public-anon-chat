from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from uuid import uuid4

from flask import session
from flask_session import Session

from engineio.payload import Payload
Payload.max_decode_packets = 50
import os


import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = uuid4().hex
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

socketio = SocketIO(app)
if 'DYNO' in os.environ:
    from socketio import socketio_manage
    from socketio.server import SocketIOServer
class MyNamespace(object):
    def __init__(self, *args, **kwargs):
        pass
    
    def on_connect(self, *args, **kwargs):
        if not 'sid' in session.keys():
            session['sid'] = request.sid
            print(session['sid'], "connected")
    
    def on_disconnect(self, *args, **kwargs):
        print("discon!!!!!")
    
    def send_mes(self, *args, **kwargs):
        mes.append([session['sid'],kwargs['data']['mes']])
        socketio.emit('take_mes', {'id':mes[-1][0], 'mes': mes[-1][1], 'private':'False'})
    def send_private(self, *args, **kwargs):
        to = kwargs['data']['mes'].split('==>')[0]
        text = kwargs['data']['mes'].split('==>')[1]
        socketio.emit('take_mes', {'id':session['sid'], 'mes': "("+to+'): '+text, 'private':'True'}, room=session['sid'])
        socketio.emit('take_mes', {'id':session['sid'], 'mes': "("+to+'): '+text, 'private':'True'}, room=to)

mes = []
from zoneinfo import ZoneInfo
start_date = datetime.datetime.now(ZoneInfo('Europe/Moscow'))
@app.route("/", methods=["GET", "POST"])
def func():
    return render_template("index.html", mes=mes, L=len(mes), date = start_date)
@app.route('/socket.io/<path:remaining>')
def handle_socketio(remaining):
    from flask import request
    socketio_manage(request.environ, {'': MyNamespace}, request)


@socketio.on('connect')
def connect():
    if not 'sid' in session.keys():
        session['sid'] = request.sid
        print(session['sid'], "connected")

@socketio.on('disconnect')
def disconnect():
    print("discon!!!!!")


@socketio.on('send_mes')
def send_mes(data):
    mes.append([session['sid'],data['mes']])
    socketio.emit('take_mes', {'id':mes[-1][0], 'mes': mes[-1][1], 'private':'False'})

@socketio.on('send_private')
def send_mes(data):
    to = data['mes'].split('==>')[0]
    text = data['mes'].split('==>')[1]
    socketio.emit('take_mes', {'id':session['sid'], 'mes': "("+to+'): '+text, 'private':'True'}, room=session['sid'])
    socketio.emit('take_mes', {'id':session['sid'], 'mes': "("+to+'): '+text, 'private':'True'}, room=to)