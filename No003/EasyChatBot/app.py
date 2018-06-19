# -*- coding:utf-8 -*-
from logging import getLogger
from logging import config
from logging import INFO
from logging import ERROR

import pya3rt
from flask import Flask
from flask import request
from flask import abort
from linebot import LineBotApi
from linebot import WebhookHandler
from linebot.exceptions import LineBotApiError
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent
from linebot.models import TextMessage
from linebot.models import TextSendMessage

from .functions import get_config
from .functions import get_logging_config
from .functions import is_webhook
from .functions import remove_emoji


config.fileConfig(get_logging_config())
logger = getLogger()

app = Flask(__name__)

app_config = get_config()
client = pya3rt.TalkClient(app_config["A3RT"]["ApiKey"])
line_bot_api = LineBotApi(app_config["LineConfig"]["AccessToken"])
handler = WebhookHandler(app_config["LineConfig"]["ChannelSecret"])


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
        message_text = 'すみません。よく分りません。'
        bot_message = client.talk(remove_emoji(event.message.text))
        if bot_message["message"] == "ok":
            message_text = '\n'.join([message["reply"] for message in bot_message["results"]])
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=message_text)
        )
        logger.log(INFO, event.reply_token)
        logger.log(INFO, message_text)

    except LineBotApiError as error:
        logger.log(ERROR, error.status_code)
        logger.log(ERROR, error.error.message)
        logger.log(ERROR, error.error.details)


if __name__ == "__main__":
    app.run()
