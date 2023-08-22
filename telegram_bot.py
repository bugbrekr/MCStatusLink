import flask
import pyrogram
import toml
import os

config = toml.load(os.getcwd()+"/config/config.toml")

if os.path.isdir("store/") == False:
    os.mkdir("store")

tg = pyrogram.Client(
    os.getcwd()+"/store/telegramBot", 
    api_id=config['tg_api_id'], 
    api_hash=config['tg_api_hash']
)
app = flask.Flask(__name__)

CHAT_ID = config['telegram_chat_id']

@app.route("/", methods=["POST"])
def onRequest():
    data = flask.request.json
    message = data['message']
    tg.send_message(CHAT_ID, message)
    return ""

tg.start()
print("Telegram Bot Server up!")