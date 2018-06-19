# -*- coding:utf-8 -*-
import os
import tempfile
from pathlib import Path
from datetime import datetime

import yaml


def get_config():
    return yaml.load(Path("config", "app.yaml").open(mode='r', encoding='utf-8'))


def get_logging_config():
    return str(Path("config", "logging.conf"))


def is_webhook_confirmed(reply_token):
    return (
            reply_token == "00000000000000000000000000000000" or
            reply_token == "ffffffffffffffffffffffffffffffff"
    )


def save_img_tmp_file(tmp_dir_path, message_contents):
    # with tempfile.NamedTemporaryFile(dir=tmp_dir_path, prefix='jpg-', delete=False) as tf:
    #     for chunk in message_contents.iter_content():
    #         tf.write(chunk)
    #     tmp_file_path = tf.name
    # dist_path = "{0}.jpg".format(tmp_file_path)
    # dist_name = os.path.basename(dist_path)
    # os.rename(tmp_file_path, dist_path)
    # return dist_name
    fp = Path(tmp_dir_path, datetime.now().strftime("%Y%m%d%H%M%S.jpg"))
    fh = fp.open(mode='w+b')
    for chunk in message_contents.iter_content():
        fh.write(chunk)
    fh.close()
    return fp.name
