from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os
import database

# 初始化 LINE Bot API 和 Webhook Handler
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

# 處理記帳訊息
def process_message(message):
    if message.startswith('記帳'):
        try:
            _, category, name, amount = message.split()
            amount = int(amount)
            # 使用 database 模組插入新記錄
            database.insert_transaction(category, name, amount)
            return f"已記錄 {category} {name} {amount} 元"
        except:
            return "格式錯誤，請輸入：記帳 [類別] [名稱] [金額]"
    elif message == '查看記錄':
        # 使用 database 模組查詢所有記錄
        rows = database.get_all_transactions()
        if not rows:
            return "目前沒有任何記錄。"
        records = "\n".join([f"{row[1]} - {row[2]}: {row[3]} 元 - {row[4]}" for row in rows])
        return f"記帳記錄：\n{records}"
    else:
        return "請輸入記帳指令，例如：記帳 餐飲 午餐 100 或 查看記錄"

# 處理 LINE Bot 的訊息事件
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    response_message = process_message(user_message)
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=response_message))
