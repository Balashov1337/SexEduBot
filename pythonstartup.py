import telebot #Подключаем апи
import cfg     #подключаем файл конфига
import db      #поключаем файл с заданиями  и картинками
from telebot import types # импортируем типы для кнопок
import random #подключаем библеотеку рандома


#datainit from dp.py
lvltxt1 = db.LVLTXT1
lvlpic1 = db.LVLPIC1
lvltxt2 = db.LVLTXT2
lvlpic2 = db.LVLPIC2
lvltxt3 = db.LVLTXT3
lvlpic3 = db.LVLPIC3
lvltxt4 = db.LVLTXT4
lvlpic4 = db.LVLPIC4
lvlpic5 = db.LVLPIC5
fngpic = db.FNGPIC

#кнопки
markup = types.ReplyKeyboardMarkup(resize_keyboard = True) #сгенирировали поле для клавы
markup0 = types.ReplyKeyboardMarkup(resize_keyboard = True)
markup1 = types.ReplyKeyboardMarkup(resize_keyboard = True)
markup2 = types.ReplyKeyboardMarkup(resize_keyboard = True)
markup3 = types.ReplyKeyboardMarkup(resize_keyboard = True)
markup4 = types.ReplyKeyboardMarkup(resize_keyboard = True)

item1 = types.KeyboardButton("Выполнили") #какие кнопки туда добавляем
item2 = types.KeyboardButton("Пропустить")
item3 = types.KeyboardButton("Следующий уровень")
item4 = types.KeyboardButton("Новая игра")
item5 = types.KeyboardButton("Продолжить")
item6 = types.KeyboardButton("Поблагодарить")
item7 = types.KeyboardButton("Вопросы и пожелания")

markup.add(item1,item2,item4,item7)
markup0.add(item1,item2,item3,item4,item7)
markup1.add(item4)
markup2.add(item5,item6)
markup3.add(item4,item6)
markup4.add(item4,item5)

bot = telebot.TeleBot(cfg.TOKEN) #присваиваем значение конфига

@bot.message_handler(commands=['start']) #обрботчик команды /start
def hellomessage(message):
    bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!".format(message.from_user, bot.get_me()))
    file = open('rules.txt', 'r')
    rules = file.read()
    bot.send_message(message.chat.id, "{0}".format(rules), reply_markup = markup3)
    #Генерация файлов для каждого человека
    nullfile(message)



@bot.message_handler(commands=['info']) #обрботчик команды /test
def test(message):
    file = open('rules.txt', 'r')
    rules = file.read()
    bot.send_message(message.chat.id, "{0}".format(rules), reply_markup = markup2)

@bot.message_handler(content_types=['text'])
def Handler(message):
    global lvltxt1
    global lvlpic1
    global lvltxt2
    global lvlpic2
    global lvltxt3
    global lvlpic3
    global lvltxt4
    global lvlpic4

    print(message.from_user.id)

    if message.text == 'Поблагодарить':
        bot.send_message(message.chat.id, 'Платежи принимаются на карту СБЕРБАНКА по номеру 4276 3801 6435 6227 на имя Владимира Ляхова', reply_markup=markup4)

    elif message.text == 'Вопросы и пожелания':
        bot.send_message(message.chat.id, 'Все вопросы и пожелания пишите сюда➡️ @katyaspeaker', reply_markup=markup2)

    elif message.text == 'Новая игра':
        nullfile(message)
        name_file = str(message.from_user.id)
        path = 'users/'+name_file+'.txt'
        file = open(path, 'r')
        user = list(file)
        arr = user[2]
        file.close()
        arr = arr.split(',')
        ask = random.choice(arr)
        asktxt = lvltxt1[int(ask)]
        askimg = lvlpic1[int(ask)]
        bot.send_photo(message.chat.id, open(askimg, 'rb'));
        bot.send_message(message.chat.id,asktxt, reply_markup=markup)
        try:
            arr.remove(ask)
        except:
            print('Новая игра ошибка удлаения элемента из массива')
        file = open(path, 'w')
        lvluser = 1
        point = 0
        if len(arr) > 0:
            data = '{0}\n{1}\n{2}\n'.format(lvluser,point,','.join(arr))
        file.write(data)
        file.close()


    elif message.text == 'Следующий уровень':
        movelvl(message);

    elif message.text == 'Пропустить' or message.text == 'Выполнили' or message.text =='Продолжить':

        if message.text == 'Выполнили':
            pointcounter(message)
        name_file = str(message.from_user.id)
        path = 'users/'+name_file+'.txt'
        file = open(path, 'r')
        user = list(file)
        file.close()
        lvluser = user[0]
        point = user[1]
        if len(user) > 2:
            arr = user[2]
            arr = arr.split(',')
            arr = [line.rstrip() for line in arr]
            print (arr)
        print (lvluser)
        print (point)

        if len(user) == 3:
            flag = 0
            ask = random.choice(arr)
            if int(lvluser) == 1:
                asktxt = lvltxt1[int(ask)]
                askimg = lvlpic1[int(ask)]
                if int(ask) > 3 & int(ask) < 11 :
                    flag = 1
            if int(lvluser) == 2:
                asktxt = lvltxt2[int(ask)]
                askimg = lvlpic2[int(ask)]
                if int(ask) == 1 or int(ask) ==4 or int(ask) ==8 or int(ask) == 11:
                    flag = 1
            if int(lvluser) == 3:
                asktxt = lvltxt3[int(ask)]
                askimg = lvlpic3[int(ask)]
                if int(ask) == 7 or int(ask) == 8 or int(ask) == 11:
                    flag = 1
            if int(lvluser) == 4:
                asktxt = lvltxt4[int(ask)]
                askimg = lvlpic4[int(ask)]
                askimg2 = lvlpic5[int(ask)]
                bot.send_photo(message.chat.id, open(askimg2, 'rb'))
                if int(ask) == 4:
                    bot.send_photo(message.chat.id, open(fngpic, 'rb'))
            bot.send_photo(message.chat.id, open(askimg, 'rb'))
            if flag == 0:
                bot.send_message(message.chat.id,asktxt, reply_markup=markup)
            else:
                bot.send_message(message.chat.id,asktxt, reply_markup=markup0)

            try:
                arr.remove(ask)
                print('Удален элемент из массива')
                file = open(path, 'w')
                lvluser = int(lvluser)
                data = '{0}\n{1}{2}'.format(lvluser,point,','.join(arr))
                file.write(data)
                file.close()
                print('Файл обновлен')
            except:
                print('Не удален элемент массива, файл не обновлен')
        else:
            movelvl(message)


    else:
        bot.send_message(message.chat.id, 'Я тебя не понял для того что бы узнать ,что правила напиши команду /info', reply_markup=markup)


#Функция перехода на следующий уровень
def movelvl(message):
    #bot.send_message(message.chat.id, 'Задания на этом уровне закончились, но это ещё не всё ;)', reply_markup=markup)
    name_file = str(message.from_user.id)
    path = 'users/'+name_file+'.txt'
    file = open(path, 'r')
    user = list(file)
    lvluser = user[0]
    point = user[1]
    arr = '0,1,2,3,4,5,6,7,8,9,10,11'
    flag = 0
    if int(lvluser) < 4:
        lvluser = int(lvluser)+1
    else:
        bot.send_message(message.chat.id, 'Поздравляю, вы прошли игру! Ваше количество очков {0}. Желаете начать новую?'.format(point), reply_markup=markup3)
        lvluser = 1
        point = 0
        flag = 1
    file.close()
    file = open(path, 'w')
    data = '{0}\n{1}{2}'.format(lvluser,point,arr)
    file.write(data)
    file.close()
    if flag == 0:
        if int(lvluser) == 1:
            bot.send_message(message.chat.id, 'Добро пожаловать на уровень Знакомство👋', reply_markup=markup2)
        if int(lvluser) == 2:
            bot.send_message(message.chat.id, 'Добро пожаловать на уровень Флирт💝', reply_markup=markup2)
        if int(lvluser) == 3:
            bot.send_message(message.chat.id, 'Добро пожаловать на уровень Первая близость👩‍❤️‍👨', reply_markup=markup2)
        if int(lvluser) == 4:
            bot.send_message(message.chat.id, 'Добро пожаловать на уровень Во все тяжкие😎', reply_markup=markup2)
    #bot.send_message(message.chat.id, 'ты на {0} уровне'.format(lvluser),reply_markup =markup)
    print('Перешел на следующий лвл')


#Функция подсчета очков
def pointcounter(message):
    name_file = str(message.from_user.id)
    path = 'users/'+name_file+'.txt'
    file = open(path, 'r')
    user = list(file)
    file.close()
    lvluser = int(user[0])
    point = int(user[1])
    if len(user) > 2:
        arr = user[2]
        arr = arr.split(',')
        arr = [line.rstrip() for line in arr]
        point+=lvluser
        data = '{0}\n{1}\n{2}'.format(lvluser,point,','.join(arr))
        file = open(path, 'w')
        file.write(data)
        file.close()
    print('Point ++')


def nullfile(message):
    path="users/"
    name_file = str(message.from_user.id);
    name=path+name_file+'.txt'
    file =open(name,'w')
    lvluser = 1
    point = 0
    arr = '0,1,2,3,4,5,6,7,8,9,10,11'
    data = '{0}\n{1}\n{2}'.format(lvluser,point,arr)
    file.write(data)
    file.close()


#RUN
bot.polling(none_stop = True)