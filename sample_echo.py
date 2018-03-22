#-*- coding:utf-8 -*-
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)


user_info = {
    'YOUR_CHANNEL_ACCESS_TOKEN': 'xxx',
    'YOUR_CHANNEL_SECRET': 'xxx',
    'host': 'localhost',
    'port': 8080
}

app = Flask(__name__)
line_bot_api = LineBotApi(user_info['YOUR_CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(user_info['YOUR_CHANNEL_SECRET'])


@app.route("/", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # Webhook接続確認か判定
    if event.reply_token == "00000000000000000000000000000000":
        return

    # メッセージを送信してきたユーザに書いた内容をエコーする
    line_bot_api.reply_message(
        event.reply_token,
        [
            TextSendMessage(text=event.message.text)
        ]
    )


if __name__ == "__main__":
    app.run(
        host=user_info['host'],
        port=user_info['port']
    )
