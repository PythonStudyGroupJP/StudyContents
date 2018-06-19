# -*- coding:utf-8 -*-
import numpy as np
import tensorflow as tf
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input
from keras.applications.vgg16 import decode_predictions


vgg16 = VGG16(weights='imagenet')
graph = tf.get_default_graph()


def predict(img_file_path):
    global graph
    with graph.as_default():
        img = load_img(img_file_path, target_size=(224, 224))
        img_data = np.expand_dims(img_to_array(img), axis=0)
        pre_dict = vgg16.predict(preprocess_input(img_data))
        predictions = decode_predictions(pre_dict, top=5)[0]
        result = ""
        ans = {"name": "", "rate": 0.0}
        for word_net_id, class_name, rate in predictions:
            _rate = rate * 100.0
            result += "{0}\n{1:03}%\n".format(class_name, _rate)
            if ans["rate"] < _rate:
                ans["name"] = class_name
                ans["rate"] = _rate
        return result + "\nAns.\n{0}".format(ans["name"])
    return "Failed"
