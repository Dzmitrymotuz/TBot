import time
from telegram.ext import *
from telegram import Poll, PollAnswer, PollOption, User, Update
import random
from tarot_meaning import *
from datetime import datetime
from Putin import *
from Hitler import *
from Medved import *
import os
from maximas_fuko import *

def photosend():
    path = "/Users/dzmitrymotuz/PycharmProjects/Guess_the_politic/tarot/"
    names = os.listdir(path)
    num = random.randint(0, len(names) - 1)
    card_name = names[num].split(".")[0]
    print(card_name)

    return f"{path}{names[num]}"

def triple():
    path = "/Users/dzmitrymotuz/PycharmProjects/Guess_the_politic/tarot/"
    names = os.listdir(path)
    cards_amount = len(names) - 1
    num1, num2, num3 = random.sample(range(0, cards_amount), 3)
    card_name1 = names[num1].split(".")[0]
    card_name2 = names[num2].split(".")[0]
    card_name3 = names[num3].split(".")[0]
    values = [f"{path}{names[num1]}", f"{path}{names[num2]}", f"{path}{names[num3]}"]
    return values

def card_reading(card_name):
    names = ['shut', 'mag', 'verhovaya_zhrica', 'imperatrica', 'imperator', 'verhovnyi_zhrec', 'vlublennye', 'kolesnica', 'sila', 'otshelnik', 'koleso_fortuny', 'spravedlivost', 'poveshennyi', 'smert', 'umerennost', 'diyavol', 'padayushaya_bashnya', 'zvezda', 'luna', 'solnce', 'strashnyi_sud', 'mir']
    num = random.randint(0, 3)
    if card_name in names[0]:
        return shut[num]
    if card_name in names[1]:
        return mag[num]
    if card_name in names[2]:
        return verhovaya_zhrica[num]
    if card_name in names[3]:
        return imperatrica[num]
    if card_name in names[4]:
        return imperator[num]
    if card_name in names[5]:
        return verhovnyi_zhrec[num]
    if card_name in names[6]:
        return vlublennye[num]
    if card_name in names[7]:
        return kolesnica[num]
    if card_name in names[8]:
        return sila[num]
    if card_name in names[9]:
        return otshelnik[num]
    if card_name in names[10]:
        return koleso_fortuny[num]
    if card_name in names[11]:
        return spravedlivost[num]
    if card_name in names[12]:
        return poveshennyi[num]
    if card_name in names[13]:
        return smert[num]
    if card_name in names[14]:
        return umerennost[num]
    if card_name in names[15]:
        return diyavol[num]
    if card_name in names[16]:
        return padayushaya_bashnya[num]
    if card_name in names[17]:
        return zvezda[num]
    if card_name in names[18]:
        return luna[num]
    if card_name in names[19]:
        return solnce[num]
    if card_name in names[20]:
        return strashnyi_sud[num]
    if card_name in names[21]:
        return mir[num]

def monetka():
    x  = random.randint(0,100)
    if x < 50:
        return "Решка"
    elif x > 50:
        return "Орел"
    elif x == 50:
        return "Ребро"
    elif x == 100:
        return "Зависла в воздухе"
    elif x == 0:
        return "Пошел нахуй"

def fuko():
    infile = open('maximas.txt', 'r')
    text = infile.read()
    text = text.split(sep="&")
    num = random.randint(0, len(text) -1)
    return text[num]

def winner(key):
    if key == 0:
        return "Hitler"
    elif key == 1:
        return "Putin"
    elif key == 2:
        return "Medvedev"
    else:
        return "Something wrong, please, call back later"

def game(number):
    if number == 1:
        # print("1 Putin")
        name = "Putin"
        name = 1
        quote = putin_quotes[random.randint(0, (len(putin_quotes) - 1))]
        return quote
    elif number == 0:
        # print("2 Hitler")
        name = "Hitler"
        name = 0
        quote = hitler_quotes[random.randint(0, len(hitler_quotes) -1)]
        return quote
    elif number == 2:
        # print("3 Medved")
        name = "Medved"
        name = 2
        quote = medved_quotes[random.randint(0, len(medved_quotes) -1)]
        return quote

def sample_responses(input_text):
    user_message = str(input_text).lower()
    user_message_space = user_message.split(" ")
    # user_message_point = user_message.split(",")
    value_number = random.randint(0, 100)
    print(value_number)

    if user_message[0:3] == "ева" or "eva":
        user_message = user_message[4:].lstrip()
        # print(user_message)
        if user_message in ("кинь монетку", "монетку кинь", "кинуть монетку", "подбрось монетку", "подбрось монету", "кинь монету", "монету кинь", "монету брось", "брось монетку", "брось монету"):
            return monetka()
        elif user_message in ("кто ты?", "кто ты такая?", "что ты такое?", "кто ты", "кто ты такая", "что ты такое") and value_number > 70:
            return "Я - Ева-01, огромный боевой человекоподобный робот, защищающий остатки человечества. Люди называют меня - Евангелион"
        elif user_message in ("hello", "hi", "sup"):
            return "Hello!"
        elif user_message.lower() in ["putin", "hitler", "medvedev", "путин", "медведев", "гитлер", "путлер", "медвепут", "пидор"]:
            return f"Ну {user_message.capitalize()} уж точно - ПИДОР!\nТак что давайте поиграем!\n\n/game "
        elif user_message in ("who are you", "you?", "who are you?"):
            return "I am Eva-01, a huge fighting humanoid robot protecting the remnants of humanity. People call me Evangelion"
        # elif user_message in ("поставь напоминание про скрам", "скрам напоминание"):
        #     return "Принято. Напоминание о скрам-митинге установлено."
        elif user_message in ("time", "time?"):
            now = datetime.now()
            date_time = now.strftime("%d/%m/%y, %H:%M:%S")
            return str(date_time)
        elif user_message in ("start synchronisation", "синхронизация", "запуск синхронизации", "запуск"):

            pass
        else:
            pass
            # return f"Я ничего не поняла, уровень синхронизации с пилотом - {random.randint(70, 95)}%"
    elif user_message[0:3] != "ева" or "eva":
        pass




