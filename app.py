import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# 取得環境變數
channel_id = os.getenv("LINE_CHANNEL_ID")
channel_secret = os.getenv("LINE_CHANNEL_SECRET")

# 設置 Line API
line_bot_api = LineBotApi(channel_id)
handler = WebhookHandler(channel_secret)

# 根路由
@app.route('/')
def index():
    return "Hello, world!"

# Webhook 路由
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理使用者的記帳訊息
def process_message(message):
    if message.startswith('記帳'):
        try:
            _, category, amount = message.split()
            amount = int(amount)
            # 保存記帳資料到資料庫（此處僅為範例，實際應用中可加入資料庫操作）
            return f"已記錄 {category} {amount} 元"
        except:
            return "格式錯誤，請輸入：記帳 [類別] [金額]"
    else:
        return "請輸入記帳指令，例如：記帳 餐飲 100"

# 處理訊息事件
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    response_message = process_message(user_message)
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=response_message))

if __name__ == "__main__":
    app.run(port=8000)
