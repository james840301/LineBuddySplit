from flask import Flask, request, send_from_directory, jsonify
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

# 設定靜態檔案夾位置
STATIC_DIR = os.path.join(os.getcwd(), "static", "charts")
os.makedirs(STATIC_DIR, exist_ok=True)  # 確保資料夾存在

# 初始化 LINE Bot API、Handler、OpenAI
BASE_URL = os.getenv("BASE_URL", "http://localhost:5000")  # 動態設定 BASE_URL
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))
openai.api_key = os.getenv("OPENAI_API_KEY")

# 使用者上下文與處理器
user_context = {}
response_handler = MessageHandler(line_bot_api, user_context)

@app.route('/')
def index():
    return "Welcome to LineBuddySplit! Your app is up and running."

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
def serve_chart(filename):
    # 提供生成的 HTML 圖表檔案
    return send_from_directory(STATIC_DIR, filename, mimetype='text/html')

if __name__ == "__main__":
    app.run(debug=True, port=5000)