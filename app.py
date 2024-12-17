from flask import Flask, request, send_file
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import LineBotApiError, InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os
from dotenv import load_dotenv
from message_processor import ExpenseManager
from expense_chart_generator import ChartGenerator
import openai
from user_message_handler import MessageHandler

# 載入環境變數
load_dotenv()

app = Flask(__name__)

# 初始化 LINE Bot API、Handler、OpenAI
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))
openai.api_key = os.getenv("OPENAI_API_KEY")

# 使用者上下文與處理器
user_context = {}
response_handler = MessageHandler(line_bot_api, user_context)

@app.route("/callback", methods=["POST"])
def callback():
    # 接收並處理 LINE Webhook 請求
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        return "Invalid signature", 400
    return "OK", 200

@handler.add(MessageEvent, message=TextMessage)
def handle_line_message(event):
    # 處理使用者的文字訊息事件
    response_handler.handle_message(event)

@app.route('/chart/<filename>')
def serve_html_chart(filename):
    # 提供生成的圖表檔案
    return send_file(filename, mimetype='text/html')

if __name__ == "__main__":
    app.run(debug=True, port=5000)