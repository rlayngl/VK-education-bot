from flask import Flask, request
import vk_api
import json
from rapidfuzz import fuzz

app = Flask(__name__)

TOKEN = "vk1.a.pHrouDYDYTT_kZ-PZ4IAxZEAALVGs2I_wciv8DSnN2LVsUR8epKl0Mg6DYaBGrh9iSuKs61nY4pQETpss3HDlmd8xKCmj3aDp2jolkI7W09i6D-2lEHQxudYaHpmuZ0xyFHHCImX2838UX67vFiqedj3VmlHIiKZsGcPabpebnphmH3yBJ8mkiM_BGUDNEx7Akl0QvEgFQdU9TXjiyXpEQ"
CONFIRMATION_TOKEN = "2262c629"

vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()

with open("faq.json", "r", encoding="utf-8") as f:
    faq = json.load(f)

curse_words = ["пизда", "бля", "хуй", "пиздец", "хуе", "ебать", "ебал", "ебл"]
look_like_curse_but_not_one = ["оскорблять", "потреблять", "употреблять", "сабля", "колеблются", "колеблетесь",
                               "колеблется", "застрахуй", "подстрахуй", "страхуй"]

keyboard = {
    "one_time": False,
    "buttons": [
        [
            {"action": {"type": "text", "label": "Расписание"}, "color": "primary"},
            {"action": {"type": "text", "label": "Занятия"}, "color": "primary"},
            {"action": {"type": "text", "label": "Проекты"}, "color": "primary"},
        ],
        [
            {"action": {"type": "text", "label": "Частые вопросы"}, "color": "secondary"},
            {"action": {"type": "text", "label": "Связаться"}, "color": "secondary"},
        ]
    ]
}


def watch_manners(message_text):
    for ex in look_like_curse_but_not_one:
        if ex in message_text:
            return False

    return any(word in message_text for word in curse_words)


def search_faq(text, short=False):
    highest_score = 0
    best_entry = None

    for question, entry in faq.items():
        score = fuzz.partial_ratio(text, question)
        if score > highest_score:
            highest_score = score
            best_entry = entry

    if highest_score > 80 and best_entry:
        if short and best_entry.get("type") == "yesno":
            return best_entry.get("short")
        return best_entry.get("answer")

    return None


@app.route('/', methods=['POST'])
def callback():
    data = request.json

    if data['type'] == 'confirmation':
        return CONFIRMATION_TOKEN

    if data['type'] == 'message_new':
        user_id = data['object']['message']['from_id']
        text = data['object']['message']['text'].lower()

        if watch_manners(text):
            vk.messages.send(
                user_id=user_id,
                message="Пожалуйста, не используй ненормативную лексику.",
                random_id=0
            )
            return "ok"

        faq_short_answer = search_faq(text, short=True)
        if faq_short_answer:
            vk.messages.send(
                user_id=user_id,
                message=faq_short_answer,
                random_id=0
            )
            return "ok"

        faq_answer = search_faq(text)
        if faq_answer:
            vk.messages.send(
                user_id=user_id,
                message=faq_answer,
                random_id=0
            )
            return "ok"

        if text == "/start":
            vk.messages.send(
                user_id=user_id,
                message="Привет! Я бот VK Education. Выбери, что тебя интересует:",
                random_id=0,
                keyboard=json.dumps(keyboard)
            )
        elif text == "/help":
            help_message = (
                "Справка:\n\n"
                "/start — запустить бота\n"
                "/help — список доступных команд\n\n"
                "Используй кнопки ниже или задай интересующий вопрос:\n"
                "«Как попасть в программу», «Можно ли совмещать работу», и т.д."
            )
            vk.messages.send(
                user_id=user_id,
                message=help_message,
                random_id=0
            )
        elif text == "/faq" or text == "частые вопросы":
            questions = "\n".join([f"• {q}" for q in list(faq.keys())[:10]])
            vk.messages.send(
                user_id=user_id,
                message=f"🔎 Часто задаваемые вопросы:\n\n{questions}\n\nТы можешь задать любой из них",
                random_id=0
            )
            return "ok"
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
        elif "контакт" in text:
            vk.messages.send(
                user_id=user_id,
                message="Связаться с нами можно через форму на сайте VK Education или по email: support@edu.vk.com",
                random_id=0
            )
        elif "как попасть" in text or "отбор" in text:
            vk.messages.send(
                user_id=user_id,
                message="Чтобы попасть в программу, нужно заполнить анкету и пройти отбор.",
                random_id=0
            )
        else:
            vk.messages.send(
                user_id=user_id,
                message="Я пока не знаю ответа на этот вопрос. Переформулируй вопрос или напиши /start, чтобы увидеть доступные команды.",
                random_id=0
            )

    return "ok"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
