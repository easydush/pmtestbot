import telebot

from db_worker import DBConnector
import os
from dotenv import load_dotenv

load_dotenv()

bot = telebot.TeleBot(os.getenv('KEY'))
db = DBConnector()
questions = db.get_all_questions()
question_cursor = 0
game_id = 0
db.close()


def send_statistics(message):
    db = DBConnector()
    game = db.get_game(message.from_user.id)
    answer = f'persuasion: {game[1]},\tauthority: {game[2]},\texperience: {game[3]},\trelationships: {game[4]},\tperformance: {game[5]},\tmoney: {game[6]},\tterms: {game[7]},\tquality: {game[8]},\treadiness: {game[9]}'
    bot.send_message(message.from_user.id, text=answer)
    db.close()


@bot.message_handler(func=lambda message: message.text in ['0', '1', '2', '3'])
def handle_answer(message):
    db = DBConnector()
    global question_cursor
    answer = db.get_answers(question_cursor + 1)[int(message.text)]
    bot.reply_to(message, answer[12])
    db.change_game(game_id, *answer[3:12])
    db.close()
    send_statistics(message)
    question_cursor += 1
    if question_cursor < len(questions):
        send_question(message)
    else:
        bot.send_message(message.from_user.id, text='Game is over!')


def send_question(message):
    bot.send_message(message.from_user.id, text=f'{questions[question_cursor][1]}')
    db = DBConnector()
    answers = db.get_answers(question_cursor + 1)
    answers = [f'{index}: {value}\n' for index, value in enumerate(answer[2] for answer in answers)]
    bot.send_message(message.from_user.id, text=f'{"".join(answers)}')
    db.close()


@bot.message_handler(commands=['go'], content_types=['text'])
def start_game(message):
    bot.send_message(message.from_user.id, "Игра началась.")
    db = DBConnector()
    game = db.init_game(str(message.from_user.id))
    global game_id
    game_id = db.get_game(message.from_user.id)[0]
    send_question(message)
    db.close()
    send_statistics(message)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == 'Привет':
        bot.send_message(message.from_user.id, "Привет, давай сыграем!Напиши /go, чтобы начать игру.")
    elif message.text == '/help':
        bot.send_message(message.from_user.id, "Напиши /go, чтобы начать игру.")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


bot.polling(none_stop=True, interval=0)
