# -*- coding:utf-8 -*-
from logging import getLogger
from logging import config
from logging import INFO
from logging import ERROR
from pathlib import Path

from flask import Flask
from flask import request
from flask import abort
from linebot import LineBotApi
from linebot import WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.exceptions import LineBotApiError
from linebot.models import MessageEvent
from linebot.models import ImageMessage
from linebot.models import TextSendMessage

from .functions import get_config
from .functions import get_logging_config
from .functions import is_webhook_confirmed
from .functions import save_img_tmp_file
from .classified_image import predict


config.fileConfig(get_logging_config())
logger = getLogger()

app = Flask(__name__)

app_config = get_config()
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


@handler.add(MessageEvent, message=ImageMessage)
def handle_message(event):
    if is_webhook_confirmed(event.reply_token):
        return
    try:

        tmp_dir_path = Path('img', 'tmp')
        message_contents = line_bot_api.get_message_content(event.message.id)
        dist_name = save_img_tmp_file(str(tmp_dir_path), message_contents)
        message = predict(str(tmp_dir_path / dist_name))
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text=message)
            ]
        )
        logger.log(INFO, event.reply_token)

    except LineBotApiError as error:
        logger.log(ERROR, error.status_code)
        logger.log(ERROR, error.error.message)
        logger.log(ERROR, error.error.details)

    except Exception as error:
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text='ちょっと問題が起きてしまいました...')
            ]
        )
        logger.log(ERROR, error.args)


if __name__ == '__main__':
    app.run(port=8080)
