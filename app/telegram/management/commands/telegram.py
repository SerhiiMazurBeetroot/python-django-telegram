from django.core.management.base import BaseCommand
from django.conf import settings

from telebot import types, TeleBot
from datetime import date
import emoji

from telegram.services.weather import Weather
from telegram.services.nbu import Nbu
from telegram.services.jokes import Jokes
from telegram.services.translators import t
import telegram.services.helpers as helpers
import telegram.services.game as game

bot = TeleBot(settings.TELEGRAM_BOT_API_KEY, threaded=False)
btn_main = types.KeyboardButton(f'{emoji.emojize(":house:")} Main')


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        bot.enable_save_next_step_handlers(delay=2)
        bot.load_next_step_handlers()
        bot.infinity_polling()


def bot_send_message(fn_name, message, response_to_user, markup):
    chat_id = message.chat.id
    if markup:
        bot.send_message(
            chat_id,
            response_to_user,
            parse_mode="html",
            reply_markup=markup,
        )
    else:
        bot.send_message(
            chat_id,
            response_to_user,
            parse_mode="html",
        )
    helpers.save_user_action(fn_name, message, response_to_user)


@bot.message_handler(commands=["start"])
def start(message):
    message_text = helpers.handle_user(message)

    show_main_menu(message, message_text)
    bot.register_next_step_handler(message, handle_main_menu)


def show_main_menu(message, response_to_user):
    fn_name = "show_main_menu"
    reset_game()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    markup.add(
        types.KeyboardButton(f'{emoji.emojize(":money_bag:")}' f" NBU"),
        types.KeyboardButton(
            f'{emoji.emojize(":sun_behind_small_cloud:")}' f" Weather"
        ),
    )
    markup.add(
        types.KeyboardButton(f'{emoji.emojize(":joker:")}' f" Jokes"),
        types.KeyboardButton(f'{emoji.emojize(":game_die:")}' f" Tic-Tac-Toe"),
    )

    bot_send_message(fn_name, message, response_to_user, markup)


def return_main_menu(message):
    message_text = f'{emoji.emojize(":house:")}...'
    show_main_menu(message, message_text)
    bot.register_next_step_handler(message, handle_main_menu)


def handle_main_menu(message):
    fn_name = "handle_main_menu"

    response_to_user = ""
    message_text = helpers.handle_message_text(message.text)
    reset_matrix()

    if message_text == "weather":
        response_to_user = f'{emoji.emojize(":cityscape:")} Select a city'

        on_weather_menu(message, response_to_user)
        bot.register_next_step_handler(message, handle_weather_menu)

    elif message_text == "nbu":
        response_to_user = f'{emoji.emojize(":heavy_dollar_sign:")} Select currency'

        on_nbu_menu(message, response_to_user)
        bot.register_next_step_handler(message, handle_nbu_menu)

    elif message_text == "jokes":
        handle_jokes_menu(message)
    elif message_text == "game":
        on_game_menu(message)
    elif message_text == "stop":
        handle_stop(message)
    else:
        show_main_menu(message, "Please choose an option:")
        bot.register_next_step_handler(message, handle_main_menu)


def handle_stop(message):
    fn_name = "handle_stop"

    response_to_user = "Bye. See you next time"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    markup.add(types.KeyboardButton("/start"))
    bot_send_message(fn_name, message, response_to_user, markup)


# Weather
def on_weather_menu(message, response_to_user):
    fn_name = "on_weather_menu"

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    cities = ["Kyiv", "Odesa", "London", "Other city"]
    markup.row(*[types.KeyboardButton(city) for city in cities])
    markup.row(btn_main)

    bot_send_message(fn_name, message, response_to_user, markup)


def handle_weather_menu(message):
    fn_name = "handle_weather_menu"
    response_to_user = ""
    message_text = helpers.handle_message_text(message.text)

    if message_text == "main":
        return_main_menu(message)
    elif message_text == "stop":
        handle_main_menu(message)
    elif message_text != "Other city":
        weather = Weather(message_text)

        if weather.status:
            response_to_user = weather.message
            on_weather_menu(message, response_to_user)
            bot.register_next_step_handler(message, handle_weather_menu)

        else:
            response_to_user = "Something went wrong, try again later"
            bot_send_message(fn_name, message, response_to_user, False)

            return_main_menu(message)

    elif message_text == "Other city":
        response_to_user = "Enter city"
        markup = types.ReplyKeyboardMarkup(
            resize_keyboard=True, one_time_keyboard=False
        )
        markup.row(btn_main)

        bot_send_message(fn_name, message, response_to_user, markup)
        bot.register_next_step_handler(message, click_weather_others)


def click_weather_others(message):
    fn_name = "click_weather_others"

    response_to_user = ""
    message_text = helpers.handle_message_text(message.text)

    if message_text == "main":
        return_main_menu(message)
    elif message_text == "stop":
        handle_main_menu(message)
    else:
        weather = Weather(message_text)

        if weather.status:
            response_to_user = weather.message
            on_weather_menu(message, response_to_user)
            bot.register_next_step_handler(message, handle_weather_menu)
        else:
            response_to_user = f"{weather.message}.\nEnter other city"
            markup = types.ReplyKeyboardMarkup(
                resize_keyboard=True, one_time_keyboard=False
            )
            markup.row(btn_main)

            bot_send_message(fn_name, message, response_to_user, markup)
            bot.register_next_step_handler(message, click_weather_others)


# Nbu
def on_nbu_menu(message, response_to_user):
    fn_name = "on_nbu_menu"

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    currencies = ["USD", "EUR", "GBP", "Other currency"]
    markup.row(*[types.KeyboardButton(currency) for currency in currencies])
    markup.row(btn_main)

    bot_send_message(fn_name, message, response_to_user, markup)


def handle_nbu_menu(message):
    fn_name = "handle_nbu_menu"

    response_to_user = ""
    message_text = helpers.handle_message_text(message.text)

    if message_text == "main":
        return_main_menu(message)
    elif message_text in ("USD", "EUR", "GBP"):
        current_date = date.today()
        nbu = Nbu(current_date, message_text.upper()[0:3])

        if nbu.status:
            response_to_user = nbu.message
            on_nbu_menu(message, response_to_user)
            bot.register_next_step_handler(message, handle_nbu_menu)
        else:
            response_to_user = nbu.message
            bot_send_message(fn_name, message, response_to_user, False)

    elif message_text == "Other currency":
        response_to_user = "Enter currency"
        markup = types.ReplyKeyboardMarkup(
            resize_keyboard=True, one_time_keyboard=False
        )
        markup.row(btn_main)

        bot_send_message(fn_name, message, response_to_user, markup)
        bot.register_next_step_handler(message, click_nbu_others)


def click_nbu_others(message):
    fn_name = "click_nbu_others"

    response_to_user = ""
    message_text = helpers.handle_message_text(message.text)

    if message_text == "main":
        return_main_menu(message)
    elif message_text == "stop":
        handle_main_menu(message)
    else:
        current_date = date.today()
        nbu = Nbu(current_date, message_text.upper())

        if nbu.status:
            response_to_user = nbu.message
            on_nbu_menu(message, response_to_user)
            bot.register_next_step_handler(message, handle_nbu_menu)
        else:
            response_to_user = f"{nbu.message}.\nPlease enter correct currency code"
            markup = types.ReplyKeyboardMarkup(
                resize_keyboard=True, one_time_keyboard=False
            )
            markup.row(btn_main)

            bot_send_message(fn_name, message, response_to_user, markup)
            bot.register_next_step_handler(message, click_nbu_others)


# Jokes
lang_code = "en"
lang_default = "en"
lang_avaliable = ("cs", "de", "en", "es", "fr", "pt")


def handle_jokes_menu(message):
    fn_name = "handle_jokes_menu"

    message_text = helpers.handle_message_text(message.text)
    response_to_user = f'{emoji.emojize(":heavy_dollar_sign:")} Select language'

    if message_text == "main":
        return_main_menu(message)
    elif message_text == "stop":
        handle_main_menu(message)
    else:
        markup = types.ReplyKeyboardMarkup(
            resize_keyboard=True, one_time_keyboard=False
        )
        languages = ["UK", "EN", "DE", "ES", "FR", "PT"]
        markup.row(*[types.KeyboardButton(lang) for lang in languages])
        markup.row(btn_main)

        bot_send_message(fn_name, message, response_to_user, markup)
        bot.register_next_step_handler(message, on_jokes_menu)


def on_jokes_menu(message):
    fn_name = "on_jokes_menu"

    global lang_code
    message_text = helpers.handle_message_text(message.text)

    if message_text == "main":
        return_main_menu(message)
    elif message_text == "stop":
        handle_main_menu(message)
    elif message_text == "Next joke":
        send_next_joke(message)
    elif message_text == "Change language":
        handle_jokes_menu(message)
    else:
        lang_code = message_text.lower()
        send_next_joke(message)


def send_next_joke(message):
    fn_name = "send_next_joke"

    response_to_user = ""
    message_text = helpers.handle_message_text(message.text)

    if message_text == "main":
        return_main_menu(message)
    else:
        if lang_code in lang_avaliable:
            joke_api = Jokes(lang_code)
            response_to_user = joke_api.get_joke()
        else:
            joke_api = Jokes(lang_default)
            response_to_user = joke_api.get_joke()
            response_to_user = t(response_to_user)

        markup = types.ReplyKeyboardMarkup(
            resize_keyboard=True, one_time_keyboard=False
        )
        buttons = ["Change language", "Next joke"]
        markup.row(*[types.KeyboardButton(btn) for btn in buttons])
        markup.row(btn_main)

        bot_send_message(fn_name, message, response_to_user, markup)
        bot.register_next_step_handler(message, on_jokes_menu)


# Tic-Tac-Toe
players = ["X", "O"]
current_player = 0
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
player_wins = [0, 0]


def on_game_menu(message):
    fn_name = "on_game_menu"

    global current_player, matrix
    message_text = helpers.handle_message_text(message.text)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)

    if message_text == "main":
        return_main_menu(message)
    elif message_text == "stop":
        handle_main_menu(message)
    else:
        response_to_user = "Let's play Tic-Tac-Toe!"
        bot_send_message(fn_name, message, response_to_user, markup)
        display_board(message)


def play_game(message):
    fn_name = "play_game"

    global current_player, matrix
    response_to_user = ""
    message_text = helpers.handle_message_text(message.text)

    if message_text == "main":
        return_main_menu(message)
    elif message_text == "stop":
        handle_main_menu(message)
    else:
        try:
            selected_number = int(message_text)

            if 1 <= selected_number <= 9:
                row = (selected_number - 1) // 3
                col = (selected_number - 1) % 3

                if isinstance(matrix[row][col], int):
                    matrix[row][col] = players[current_player]

                    if game.check_winner(matrix, players[current_player]):
                        player_wins[current_player] += 1

                        response_to_user = print_game_result(
                            f"Player {players[current_player]} wins!"
                        )
                        bot_send_message(fn_name, message, response_to_user, False)
                        restart_game(message)
                        return

                    elif game.is_full(matrix):
                        response_to_user = print_game_result("It's a draw!")
                        bot_send_message(fn_name, message, response_to_user, False)
                        restart_game(message)
                        return

                    current_player = 1 - current_player

                    display_board(message)
                else:
                    response_to_user = f"This position is already taken. Try again"
                    bot_send_message(fn_name, message, response_to_user, False)
                    display_board(message)

            else:
                response_to_user = f"Please select a number between 1 and 9"
                bot_send_message(fn_name, message, response_to_user, False)

        except ValueError:
            response_to_user = f"Try again."
            bot_send_message(fn_name, message, response_to_user, False)
            display_board(message)


def display_board(message):
    fn_name = "display_board"

    global current_player, matrix
    response_to_user = f"Current player: {players[current_player]}"

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    for row in matrix:
        buttons = [types.KeyboardButton(str(col)) for col in row]
        markup.row(*buttons)

    markup.row(btn_main)

    bot_send_message(fn_name, message, response_to_user, markup)
    bot.register_next_step_handler(message, play_game)


def restart_game(message):
    fn_name = "restart_game"

    reset_matrix()
    response_to_user = "Play again ?"

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    markup.row(types.KeyboardButton("Yes"), btn_main)

    bot_send_message(fn_name, message, response_to_user, markup)
    bot.register_next_step_handler(message, on_game_menu)


def print_game_matrix():
    global matrix
    matrix_str = ""
    for row in matrix:
        matrix_str += " ".join(str(col) for col in row) + "\n"
    return matrix_str


def print_game_result(head):
    response_to_user = (
        f"{head} \n\n"
        f"<b>Board:</b> \n"
        f"{print_game_matrix()} \n"
        f"<b>Score:</b> \n"
        f"Player X: {player_wins[0]}, Player 0: {player_wins[1]}"
    )
    return response_to_user


def reset_matrix():
    global matrix
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]


def reset_game():
    global player_wins
    player_wins = [0, 0]
