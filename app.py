from flask import Flask, request
import vk_api
import json
import re
from rapidfuzz import fuzz
import urllib.parse
from collections import defaultdict

app = Flask(__name__)

TOKEN = "vk1.a.pHrouDYDYTT_kZ-PZ4IAxZEAALVGs2I_wciv8DSnN2LVsUR8epKl0Mg6DYaBGrh9iSuKs61nY4pQETpss3HDlmd8xKCmj3aDp2jolkI7W09i6D-2lEHQxudYaHpmuZ0xyFHHCImX2838UX67vFiqedj3VmlHIiKZsGcPabpebnphmH3yBJ8mkiM_BGUDNEx7Akl0QvEgFQdU9TXjiyXpEQ"
CONFIRMATION_TOKEN = "2262c629"

vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()

with open("faq.json", "r", encoding="utf-8") as f:
    faq = json.load(f)

curse_words = ["пизда", "бля", "хуй", "пиздец", "хуе", "ебать", "ебал", "ебл", "гандон", "пидор", "педик", "траха"]
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

last_topic = defaultdict(lambda: {"topic": None})


def watch_manners(message_text):
    text = message_text.lower()
    words = re.findall(r'\w+', text)

    for word in words:
        if word in look_like_curse_but_not_one:
            continue

        for root in curse_words:
            if root in word:
                return True

    return False


def search_faq(text, short=False):
    highest_score = 0
    best_question = None
    best_entry = None

    for question, entry in faq.items():
        score = fuzz.partial_ratio(text, question)
        if score > highest_score:
            highest_score = score
            best_question = question
            best_entry = entry

    if highest_score > 80 and best_entry:
        if short and best_entry.get("type") == "yesno":
            return best_entry.get("short"), best_question
        return best_entry.get("answer"), best_question

    return None, None


def search_related(text, last_question):
    if last_question in faq:
        related_questions = faq[last_question].get("related", [])
        for rel_q in related_questions:
            score = fuzz.partial_ratio(text, rel_q)
            if score > 75:
                return faq[rel_q]["answer"], rel_q
    return None, None


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

        greetings = ["привет", "хай", "здорова", "добрый день", "доброе утро", "здравствуй", "хэллоу", "уассап",
                     "добрый вечер", "доброй ночи", "доброго вечера", "доброй ночи", "доброго утра", "доброго дня"]
        if text in greetings or text == "/start":
            vk.messages.send(
                user_id=user_id,
                message=(
                    "Привет! Я бот VK Education. Задавай то., что тебя интересует!\n"
                    "Для помощи можешь воспользоваться командой /help."
                ),
                random_id=0,
                keyboard=json.dumps(keyboard)
            )
            return "ok"

        if text == "/help":
            help_message = (
                "Справка:\n\n"
                "/start — вернуться к началу\n"
                "/faq — список часто задаваемых вопросов\n"
                "/help — список доступных команд (использовано сейчас)\n\n"
                "Используй кнопки ниже или задай интересующий вопрос:\n"
                "«Как попасть в программу», «Можно ли совмещать работу», и т.д."
            )
            vk.messages.send(
                user_id=user_id,
                message=help_message,
                random_id=0
            )
            return "ok"

        elif text == "/faq" or text == "частые вопросы":
            questions = "\n".join([f"• {q}" for q in list(faq.keys())[:19]])
            vk.messages.send(
                user_id=user_id,
                message=f"Часто задаваемые вопросы:\n\n{questions}\n\nСпрашивай, что хочешь и даже больше.",
                random_id=0
            )
            return "ok"

        faq_short_answer, matched_q = search_faq(text, short=True)
        if faq_short_answer:
            last_topic[user_id]["topic"] = matched_q
            vk.messages.send(
                user_id=user_id,
                message=faq_short_answer,
                random_id=0
            )
            return "ok"

        faq_answer, matched_q = search_faq(text)
        if faq_answer:
            last_topic[user_id]["topic"] = matched_q
            vk.messages.send(
                user_id=user_id,
                message=faq_answer,
                random_id=0
            )
            return "ok"

        if text == "связаться":
            vk.messages.send(
                user_id=user_id,
                message="Связаться с нами можно тут: https://education.vk.company/contacts",
                random_id=0,
            )
            return "ok"
        elif "расписание" in text:
            vk.messages.send(
                user_id=user_id,
                message="Расписание занятий можно найти здесь: https://education.vk.company/schedule",
                random_id=0
            )
            return "ok"
        elif "занятия" in text:
            vk.messages.send(
                user_id=user_id,
                message="Занятия проводятся регулярно онлайн. Следи за анонсами на сайте VK Education.",
                random_id=0
            )
            return "ok"
        elif "проекты" in text:
            vk.messages.send(
                user_id=user_id,
                message="Все проекты доступны по ссылке: https://education.vk.company/education_projects",
                random_id=0
            )
            return "ok"
        elif "контакт" in text:
            vk.messages.send(
                user_id=user_id,
                message="Связаться с нами можно через форму на сайте VK Education или по email: support@edu.vk.com",
                random_id=0
            )
            return "ok"
        elif "спасибо" in text or "благодарю" in text:
            vk.messages.send(
                user_id=user_id,
                message="Пожалуйста! Обращайся, а я тебе помогу.",
                random_id=0
            )
            return "ok"
        elif "как попасть" in text or "отбор" in text:
            vk.messages.send(
                user_id=user_id,
                message="Чтобы попасть в программу, нужно заполнить анкету и пройти отбор.",
                random_id=0
            )
            return "ok"

        topic = last_topic.get(user_id)
        user_last_topic = topic["topic"] if topic else None

        if user_last_topic:
            related_answer, related_match = search_related(text, user_last_topic)
            if related_answer:
                last_topic[user_id]["topic"] = related_match
                vk.messages.send(
                    user_id=user_id,
                    message=related_answer,
                    random_id=0
                )
                return "ok"

            search_link = f"https://www.google.com/search?query={urllib.parse.quote(str(user_last_topic))}"
            vk.messages.send(
                user_id=user_id,
                message=(
                    "Я пока не знаю точного ответа на это.\n"
                    f"Попробуй поиск на сайте: {search_link}"
                ),
                random_id=0
            )
            return "ok"

    return "ok"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

# ,
# "расскажи что-то о саше": {
#     "answer": "Честно, он мне ничего не говорит. Единственное, что он твердит постоянно, что любит Дашу. Если б я знал, что такое любить и кто такая эта Даша. Говорит, очень красивая и крутая...",
#     "type": "open"
# },
# "саша": {
#     "answer": "Наверное, ты говоришь о создателе. О Высоцком Александре.",
#     "type": "open"
# },
# "даша": {
#     "answer": "Такая невероятная, такая красиваааая, такая замечательная и прекрасная....Ой, кажется, я говорю словами создателя.",
#     "type": "open"
# }
