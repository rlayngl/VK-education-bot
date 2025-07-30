from flask import Flask, request
import vk_api
import json
import os

app = Flask(__name__)

TOKEN = "vk1.a.pHrouDYDYTT_kZ-PZ4IAxZEAALVGs2I_wciv8DSnN2LVsUR8epKl0Mg6DYaBGrh9iSuKs61nY4pQETpss3HDlmd8xKCmj3aDp2jolkI7W09i6D-2lEHQxudYaHpmuZ0xyFHHCImX2838UX67vFiqedj3VmlHIiKZsGcPabpebnphmH3yBJ8mkiM_BGUDNEx7Akl0QvEgFQdU9TXjiyXpEQ"
CONFIRMATION_TOKEN = "токен_подтверждения_из_ВК"

vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()

@app.route('/', methods=['POST'])
def callback():
    data = request.json

    if data['type'] == 'confirmation':
        return CONFIRMATION_TOKEN

    if data['type'] == 'message_new':
        user_id = data['object']['message']['from_id']
        text = data['object']['message']['text'].lower()

        if "проект" in text:
            answer = "Проекты доступны на сайте VK Education."
        else:
            answer = "Извините, я пока не знаю ответа."

        vk.messages.send(
            user_id=user_id,
            message=answer,
            random_id=0
        )

    return "ok"
