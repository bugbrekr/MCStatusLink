import flask
import time
import message_templates
import threading
import requests
import toml
import os

app = flask.Flask(__name__)

config = toml.load("config/config.toml")
tg_templates = message_templates.TelegramMessage()

def _sendMessageRequest(text):
    url = f"http://{config['tg_server_bind']}/"
    data = {"message": text}
    requests.post(url, json=data)

def sendMessage(text):
    if text == None:
        return
    threading.Thread(target=_sendMessageRequest, args=(text,)).start()

def populate_template(template_id, **kwargs):
    message = tg_templates.__getattribute__(template_id).format(**kwargs)[:-1]
    return message

@app.route('/serverStarting', methods=["POST"])
def serverStarting():
    data = flask.request.json
    global init_time
    if data['type'] != "serverLifeCycle" or data['status'] != "STARTING":
        return
    print("Server is starting...")
    return ""

@app.route('/serverUp', methods=["POST"])
def serverUp():
    data = flask.request.json
    if data['type'] != "serverLifeCycle" or data['status'] != "ONLINE":
        return
    print("Server is up!")
    return ""

@app.route('/serverDown', methods=["POST"])
def serverDown():
    data = flask.request.json
    if data['type'] != "serverLifeCycle" or data['status'] != "OFFLINE":
        return
    print("Server is down.")
    return ""

@app.route("/chat/playerMessage", methods=["POST"])
def chat_playerMessage():
    data = flask.request.json
    message = populate_template(
            'playerMessage',
        player_name=data['player']['username']['string'],
        message=data['message']
    )
    sendMessage(message)
    return ""

@app.route("/player/advancement", methods=["POST"])
def player_advancement():
    data = flask.request.json
    print(f"{data['player']['username']['string']} has completed the advancement {data['title']['string']}: {data['description']['string']}")
    message = populate_template(
        'playerAdvancement',
        player_name=data['player']['username']['string'],
        advancement_title=data['title']['string'],
        advancement_description=data['description']['string']
    )
    sendMessage(message)
    return ""

@app.route("/player/death", methods=["POST"])
def player_death():
    data = flask.request.json
    print(data["deathMessage"]["string"])
    message = populate_template(
        'playerDeath',
        death_message=data['deathMessage']['string']
    )
    sendMessage(message)
    return ""

@app.route("/player/join", methods=["POST"])
def player_join():
    data = flask.request.json
    # print(data)
    print(data['player']['username']['string']+" has joined the server!")
    message = populate_template(
        'playerJoin',
        player_name=data['player']['username']['string']
    )
    sendMessage(message)
    return ""

@app.route("/player/leave", methods=["POST"])
def player_leave():
    data = flask.request.json
    print(data['player']['username']['string']+" left the server.")
    message = populate_template(
        'playerLeave',
        player_name=data['player']['username']['string']
    )
    sendMessage(message)
    return ""

@app.errorhandler(500)
def handler_error(error):
    return ""

def run_telegram_bot_server():
    gunicorn_cmd = f"gunicorn telegram_bot:app -b {config['tg_server_bind']} -w 1"
    thread = threading.Thread(target=os.system, args=(gunicorn_cmd,))
    thread.start()

if os.path.isdir("store/") == False:
    os.mkdir("store")

run_telegram_bot_server()