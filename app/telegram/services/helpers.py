# https://carpedm20.github.io/emoji/

from telegram.models import User
from telegram.models import History

import emoji


def handle_message_text(message_text):
    message_type = ""

    if message_text.endswith("Weather") or message_text.lower() == "/weather":
        message_type = "weather"
    elif message_text.endswith("NBU") or message_text.lower() == "/nbu":
        message_type = "nbu"
    elif message_text.endswith("Stop") or message_text.lower() == "/stop":
        message_type = "stop"
    elif (
        message_text.endswith("Main")
        or message_text.endswith("Start")
        or message_text.lower() == "/start"
    ):
        message_type = "main"
    elif message_text.endswith("Jokes") or message_text.lower() == "/jokes":
        message_type = "jokes"
    elif message_text.endswith("Tic-Tac-Toe") or message_text.lower() == "/game":
        message_type = "game"
    else:
        message_type = message_text

    return message_type


def save_user_action(action, data, message_text):
    History.objects.create(
        telegram_id=data.from_user.id,
        action=action,
        message_text=message_text,
    )


def handle_user(message):
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username
    telegram_id = message.from_user.id

    try:
        User.objects.get(telegram_id=telegram_id)
        message_text = f'Welcome back {emoji.emojize(":grinning_face:")} {first_name}'

    except User.DoesNotExist:
        user = User.objects.create(
            telegram_id=telegram_id,
            first_name=first_name,
            last_name=last_name,
            username=username,
        )
        message_text = f'Hello {emoji.emojize(":grinning_face:")} {first_name}'
    return message_text
