from flask import Flask, request
import vk_api
import json
import os

app = Flask(__name__)

TOKEN = "vk1.a.pHrouDYDYTT_kZ-PZ4IAxZEAALVGs2I_wciv8DSnN2LVsUR8epKl0Mg6DYaBGrh9iSuKs61nY4pQETpss3HDlmd8xKCmj3aDp2jolkI7W09i6D-2lEHQxudYaHpmuZ0xyFHHCImX2838UX67vFiqedj3VmlHIiKZsGcPabpebnphmH3yBJ8mkiM_BGUDNEx7Akl0QvEgFQdU9TXjiyXpEQ"
CONFIRMATION_TOKEN = "2262c629"

vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()

keyboard = {
    "one_time": False,
    "buttons": [
        [
            {
                "action": {
                    "type": "text",
                    "label": "Расписание"
                },
                "color": "primary"
            },
            {
                "action": {
                    "type": "text",
                    "label": "Занятия"
                },
                "color": "primary"
            },
            {
                "action": {
                    "type": "text",
                    "label": "Проекты"
                },
                "color": "primary"
            }
        ]
    ]
}

@app.route('/', methods=['POST'])
def callback():
    data = request.json

    if data['type'] == 'confirmation':
        return CONFIRMATION_TOKEN

    if data['type'] == 'message_new':
        user_id = data['object']['message']['from_id']
        text = data['object']['message']['text'].lower()

        if text == "/start":
            vk.messages.send(
                user_id=user_id,
                message="Привет! Я бот VK Education. Выбери, что тебя интересует:",
                random_id=0,
                keyboard=json.dumps(keyboard)
            )
        elif "расписание" in text:
            vk.messages.send(
                user_id=user_id,
                message="Расписание занятий можно найти здесь: https://edu.vk.com/schedule",
                random_id=0
            )
        elif "занятия" in text:
            vk.messages.send(
                user_id=user_id,
                message="Занятия проводятся регулярно онлайн. Следите за анонсами на сайте VK Education.",
                random_id=0
            )
        elif "проект" in text:
            vk.messages.send(
                user_id=user_id,
                message="Все проекты доступны по ссылке: https://edu.vk.com/projects",
                random_id=0
            )
        else:
            vk.messages.send(
                user_id=user_id,
                message="Я пока не знаю ответа на этот вопрос. Напиши /start, чтобы увидеть доступные команды.",
                random_id=0
            )

    return "ok"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)