# -*- coding:utf-8 -*-
from flask import Flask
from flask import request
from flask import abort
from linebot import LineBotApi
from linebot import WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.exceptions import LineBotApiError
from linebot.models import MessageEvent
from linebot.models import TextMessage
from linebot.models import TextSendMessage
from linebot.models import StickerSendMessage
from linebot.models import TemplateSendMessage
from linebot.models import ButtonsTemplate
from linebot.models import MessageTemplateAction


app = Flask(__name__)

line_bot_api = LineBotApi('YOUR_CHANNEL_ACCESS_TOKEN')
handler = WebhookHandler('YOUR_CHANNEL_SECRET')


def is_webhook(reply_token):
    return (
            reply_token == "00000000000000000000000000000000" or
            reply_token == "ffffffffffffffffffffffffffffffff"
    )


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
    if is_webhook(event.reply_token):
        return
    try:
        if event.message.text == "クイズ出して":
            items = [
                MessageTemplateAction(
                    label='LINE Botを作ろう',
                    text='item1'
                ),
                MessageTemplateAction(
                    label='機械学習をちょっと学んでみよう',
                    text='item2'
                ),
                MessageTemplateAction(
                    label='オセロゲームを作ろう',
                    text='item3'
                ),
                MessageTemplateAction(
                    label='ブラック・ジャックゲームを作ろう',
                    text='item4'
                ),
            ]
            messages = [
                TemplateSendMessage(
                    alt_text='quiz',
                    template=ButtonsTemplate(
                        title='Quiz',
                        text='第２回Python勉強会のテーマは？',
                        actions=items
                    )
                )
            ]

        elif event.message.text == "item1":
            messages = [
                StickerSendMessage(
                    package_id='1',
                    sticker_id='22'
                ),
                TextSendMessage(text="正解！")
            ]

        elif event.message.text in ["item2", "item3", "item4"]:
            messages = [
                StickerSendMessage(
                    package_id='1',
                    sticker_id='39'
                ),
                TextSendMessage(text="残念...")
            ]

        else:
            messages = [
                StickerSendMessage(
                    package_id='1',
                    sticker_id='38'
                ),
                TextSendMessage(text="...ごめん。何言ってるかわかんないや。\nクイズを始めるなら「クイズ出して」って呼びかけてね！")
            ]

        line_bot_api.reply_message(
            event.reply_token,
            messages
        )

    except LineBotApiError as error:
        print(error.status_code)
        print(error.error.message)
        print(error.error.message)


if __name__ == "__main__":
    app.run()
