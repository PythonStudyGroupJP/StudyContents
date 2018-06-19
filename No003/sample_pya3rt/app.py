# -*- coding:utf-8 -*-
import pya3rt

apikey = "API_KEY"
client = pya3rt.TalkClient(apikey)
while True:
    comment = input("> ")
    if comment in ["終了", "終わり", "おわり", "quit", "q", "Quit", "QUIT", "Q"]:
        break
    response = client.talk(comment)

    if response["message"] == "ok":
        for ans in response["results"]:
            print(ans["reply"])


