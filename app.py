import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# 取得環境變數
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')

# Channel Access Token
line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))

# Channel Secret
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))

# 根路由，測試伺服器是否正常
@app.route('/')
def index():
    return "Hello, world!"

# Webhook 路由，處理來自 LINE 的訊息
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

if __name__ == "__main__":
    # 使用 Render 提供的 PORT 環境變數，如果沒有提供，默認為 10000
    port = int(os.getenv("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
