# app.py v1.0.0.0.1

import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

# Flaskアプリ初期化
app = Flask(__name__)

# Render環境変数からLINE Botトークン取得
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.environ.get("LINE_CHANNEL_SECRET")
print(f"🔐 TOKEN = {LINE_CHANNEL_ACCESS_TOKEN[:10]}...", flush=True)
print(f"🔐 SECRET = {LINE_CHANNEL_SECRET[:10]}...", flush=True)

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/", methods=["GET"])
def home():
    return "✅ AIKO LINE Bot 起動中", 200

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature")
    body = request.get_data(as_text=True)
    print(f"📩 受信メッセージ: {body}", flush=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("❌ シグネチャ検証失敗")
        abort(400)

    return "OK", 200

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    reply_text = f"こんにちは、{event.message.text} と言いましたね！"
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )

if __name__ == "__main__":
    app.run(debug=True)
