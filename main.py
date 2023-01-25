from tarot_meaning import *
import constants as keys
from telegram.ext import *
from telegram import *
import responses as R
import random
from datetime import datetime

print("Bot started...")


def hello(update: Update, context) -> None:
    update.message.reply_text(f'Привет, {update.effective_user.first_name} {update.effective_user.last_name}')

def wisdom(update, context):
    update.message.reply_text(f"{R.fuko()}")

def start_command(update, context):
    update.message.reply_text('Type something random to get started!')

def help_command(update, context):
    update.message.reply_text("""
    Полезные команды:
    /game - играть в "Угадай пидора"
    /wisdom - дэйли мудрость от Ларош Фуко
    /pidor - узнать насколько ты сегодня пидор
    /start - Старт бота
    /help - помощь
    /contact - техподдержка
    """)

def contact(update, context):
    update.message.reply_text("@Gockie in TG")

def pidor(update, context):
    rate = random.randint(-100, 100)
    if update.effective_user.id == 6647365:
        update.message.reply_text(f"{update.effective_user.first_name} {update.effective_user.last_name}, ты пидор на 101%!")
    elif update.effective_user.first_name == "Dini":
        update.message.reply_text(f"{update.effective_user.first_name} {update.effective_user.last_name}, ты пидор на все 100%! ТЫ САМЫЙ ГЕЙСКИЙ ГЕЙ! С ДНЕМ РОЖДЕНИЯ!")
    else:
        update.message.reply_text(f"{update.effective_user.first_name} {update.effective_user.last_name}, ты пидор на {rate}%!")
        stat_data = {"id" : update.effective_user.id,
        "first" : update.effective_user.first_name,
        "last" : update.effective_user.last_name
        }
        print(stat_data)
        stat = open("statistics.txt", "a")
        stat.write(f"{rate}:{stat_data['id']}\n")
        stat.close()

def tarot(update, context):
    chat_id = update.message.chat_id
    cards = R.triple()
    card_name0 = cards[0].split("/")[-1]
    card_name0 = card_name0.split('.')[0]
    card_name1 = cards[1].split("/")[-1]
    card_name1 = card_name1.split('.')[0]
    card_name2 = cards[2].split("/")[-1]
    card_name2 = card_name2.split('.')[0]
    update.message.reply_text(f"Для {update.effective_user.first_name} {update.effective_user.last_name} что было:\n{R.card_reading(card_name0)}")
    context.bot.send_photo(chat_id=chat_id, photo=open(cards[0], "rb"))
    update.message.reply_text(f"Для {update.effective_user.first_name} {update.effective_user.last_name} что есть:\n{R.card_reading(card_name1)}")
    context.bot.send_photo(chat_id=chat_id, photo=open(cards[1], "rb"))
    update.message.reply_text(f"Для {update.effective_user.first_name} {update.effective_user.last_name} и что будет:\n{R.card_reading(card_name2)}")
    context.bot.send_photo(chat_id=chat_id, photo=open(cards[2], "rb"))

    now = datetime.now()
    stat_data = {"id": update.effective_user.id,
                 "first": update.effective_user.first_name,
                 "last": update.effective_user.last_name,
                 "nickname": update.effective_user.username
                 }
    print(stat_data)
    stat = open("statistics.txt", "a")
    stat.write(f"{stat_data['id']}, {stat_data['first']} {stat_data['last']}, '{stat_data['nickname']}' got cards: {card_name0, card_name1, card_name2} on {now}\n")
    stat.close()

def game(update, context):
    update.message.reply_text(f"{update.effective_user.first_name} {update.effective_user.last_name} playing")
    """Sends a predefined poll"""
    questions = ["Hitler", "Putin", "Medvedev"]
    number = random.randint(0, 2)
    update.message.reply_text(f"{R.game(number)}")
    message = context.bot.send_poll(update.effective_chat.id,
        f"Что за пидор это сказал?",
        questions,
        is_anonymous=False,
        allows_multiple_answers=False,)

    # Save some info about the poll the bot_data for later use in receive_poll_answer
    payload = {
        message.poll.id: {
            "key": number,
            "questions": questions,
            "message_id": message.message_id,
            "chat_id": update.effective_chat.id,
            "answers": 0,
        }
    }
    context.bot_data.update(payload)
    print(payload)

    text = str(update.message.text).lower()
    response = f"{R.sample_responses(text)}"
    # print(response)

def receive_poll_answer(update, context):
    """Summarize a users poll vote"""
    answer = update.poll_answer
    answered_poll = context.bot_data[answer.poll_id]
    print(answered_poll['key'])
    try:
        questions = answered_poll["questions"]
    # this means this poll answer update is from an old poll, we can't do our answering then
    except KeyError:
        return
    selected_options = answer.option_ids
    answer_string = ""
    for question_id in selected_options:
        if question_id != selected_options[-1]:
            answer_string += questions[question_id] + " and "
        else:
            answer_string += questions[question_id]

    context.bot.send_message(
        answered_poll["chat_id"],
        f"{update.effective_user.mention_html()} думает что {answer_string}!",
        parse_mode = ParseMode.HTML
    )

    answered_poll["answers"] += 1
    # Close poll after one participants voted
    if answered_poll["answers"] == 1:
        context.bot.stop_poll(answered_poll["chat_id"], answered_poll["message_id"])
        context.bot.send_message(
            answered_poll["chat_id"],
            f"И правильный ответ -  {R.winner(answered_poll['key'])}!\n\nдавай еще?\n/game",
            parse_mode=ParseMode.HTML
        )

def receive_poll(update, context):
    """On receiving polls, reply to it by a closed poll copying the received poll"""
    actual_poll = update.effective_message.poll
    # Only need to set the question and options, since all other parameters don't matter for a closed poll
    update.effective_message.reply_poll(
        question = actual_poll.question,
        options = [o.text for o in actual_poll.options],
        # with is_closed true, the poll/quiz is immediately closed
        is_closed = True,
        reply_markup = ReplyKeyboardRemove(),
    )
    print("recieve poll activated")

def handle_message(update, context):
    user_message = update.message.text
    user = update.message.from_user
    update.message.reply_text(R.sample_responses(update.message.text))


def error(update, context):
    print(f"Update {update} caused error {context.error}")

def main():
    updater = Updater(keys.API_KEY, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start_command))
    dp.add_handler(CommandHandler('help', help_command))
    dp.add_handler(CommandHandler('contact', contact))
    dp.add_handler(CommandHandler("wisdom", wisdom))
    dp.add_handler(CommandHandler("tarot", tarot))
    dp.add_handler(CommandHandler('hello', hello))
    dp.add_handler(CommandHandler("game", game))
    dp.add_handler(CommandHandler('pidor', pidor))


    dp.add_handler(MessageHandler(Filters.text, handle_message))
    dp.add_handler(MessageHandler(Filters.poll, receive_poll))
    dp.add_handler(PollAnswerHandler(receive_poll_answer))


    dp.add_error_handler(error)

    updater.start_polling(2)
    updater.idle()

main()