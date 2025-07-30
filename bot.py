import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

TOKEN = "vk1.a.pHrouDYDYTT_kZ-PZ4IAxZEAALVGs2I_wciv8DSnN2LVsUR8epKl0Mg6DYaBGrh9iSuKs61nY4pQETpss3HDlmd8xKCmj3aDp2jolkI7W09i6D-2lEHQxudYaHpmuZ0xyFHHCImX2838UX67vFiqedj3VmlHIiKZsGcPabpebnphmH3yBJ8mkiM_BGUDNEx7Akl0QvEgFQdU9TXjiyXpEQ"

vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)


faq = {
    "как выбрать проект": "Выбери интересующий проект на сайте https://education.vk.company/projects/",
    "где запись вебинара": "Записи доступны на сайте в разделе 'Вебинары'.",
    "можно ли несколько проектов": "Да, можно выбрать несколько проектов одновременно.",
}

print("Бот запущен. Ожидаю сообщения...")

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        user_id = event.user_id
        message_text = event.text

        print(f"Сообщение от {user_id}: {message_text}")

        response = None
        text_lower = message_text.lower()

        for question, answer in faq.items():
            if question in text_lower:
                response = answer
                break

        if not response:
            response = "Извините, я пока не знаю ответа на этот вопрос. Попробуйте задать его по-другому."

        vk.messages.send(
            user_id=user_id,
            message=response,
            random_id=0
        )
