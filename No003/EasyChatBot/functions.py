# -*- coding:utf-8 -*-
import yaml
import emoji
from pathlib import Path


def get_config():
    return yaml.load(Path("config", "app.yaml").open(mode='r', encoding='utf-8'))


def get_logging_config():
    return str(Path("config", "logging.conf"))


def is_webhook(reply_token):
    return (
            reply_token == "00000000000000000000000000000000" or
            reply_token == "ffffffffffffffffffffffffffffffff"
    )


def remove_emoji(message):
    return ''.join(c for c in message if c not in emoji.UNICODE_EMOJI)
