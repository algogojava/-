# -*- coding: utf-8 -*-
import json
import os
import re
import urllib.request
import time

# 쓰레드, 큐를 위한 라이브러리 추가
import multiprocessing as mp
from threading import Thread
from bs4 import BeautifulSoup
from slackclient import SlackClient
from flask import Flask, request, make_response, render_template

app = Flask(__name__)

slack_token = "xoxb-503049869125-506900504897-OYYOlUiFlwyNQp8PVdgnTitY"
slack_client_id = "503049869125.507394574051"
slack_client_secret = "06d5a8ef3d229a567992826d1e14c75f"
slack_verification = "i6F05a07b5ALurYKWM2OKE6W"
sc = SlackClient(slack_token)


# threading function
def processing_event(queue):
    print("여기는?")
    while True:       # 큐가 비어있지 않은 경우 로직 실행
        if not queue.empty():
            slack_event = queue.get()

            # Your Processing Code Block gose to here
            channel = slack_event["event"]["channel"]
            text = slack_event["event"]["text"]

            # 챗봇 크롤링 프로세스 로직 함수
            keywords = processing_function(text)

            # 아래에 슬랙 클라이언트 api를 호출하세요
            sc.api_call(
                "chat.postMessage",
                channel=channel,
                text=keywords
            )


# 크롤링 함수
def processing_function(text):
    # 함수를 구현해 주세요
    print("여기 들어와?")
    keywords = "성공!!~"

    # delay test...
    # TODO: 아래  time.sleep(5) 를 지워주세요! 테스트용 코드입니다.
    #time.sleep(5)

    return keywords


# 이벤트 핸들하는 함수
def _event_handler(event_type, slack_event):
    print(slack_event['event'])

    if event_type == "app_mention":
        event_queue.put(slack_event)
        return make_response("App mention message has been sent", 200, )


@app.route("/listening", methods=["GET", "POST"])
def hears():
    slack_event = json.loads(request.data)

    if "challenge" in slack_event:
        return make_response(slack_event["challenge"], 200, {"content_type": "application/json"})

    if slack_verification != slack_event.get("token"):
        message = "Invalid Slack verification token: %s" % (slack_event["token"])
        make_response(message, 403, {"X-Slack-No-Retry": 1})

    if "event" in slack_event:
        event_type = slack_event["event"]["type"]
        return _event_handler(event_type, slack_event)

    return make_response("[NO EVENT IN SLACK REQUEST] These are not the droids\
                             you're looking for.", 404, {"X-Slack-No-Retry": 1})


@app.route("/", methods=["GET"])
def index():
    return "<h1>Server is ready.</h1>"


if __name__ == '__main__':
    print("main!!")
    event_queue = mp.Queue()

    p = Thread(target=processing_event, args=(event_queue,))
    p.start()
    print("subprocess started")

    app.run('0.0.0.0', port=5000)
    print("오잉?")
    p.join()
