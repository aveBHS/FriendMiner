# -*- coding: utf-8 -*-
import vk_api
import time
from vk_api.longpoll import VkLongPoll, VkEventType
from random import randint
import os
from PIL import Image
import urllib.request
import requests
import re

print("BHS VK FirendMiner v2.0 SE\n--------------------------")
token = input("Токен пользователя: ")
api = vk_api.VkApi(token=token)
peer_id = int(input("VK ID пользователя: "))
captcha_price = 44 
firends = int(input("Сколько накрутить (рекоменд. не более 40 в день): "))

def add_firend(id):
    api.method('friends.add', {'user_id': id})

def captcha(url):
    urllib.request.urlretrieve(url, "./Captcha/captcha.jfif")
    Image.open("./Captcha/captcha.jfif").save("./Captcha/captcha.png")

    key = ""
    data = {"key" : key}
    files = {"file": open("./Captcha/captcha.png", "rb")}

    response = requests.post("https://rucaptcha.com/in.php", data=data, files=files)
    print("Отправка запроса на решение капчи...")
    if(response.status_code == 200):
        print("Запрос отправлен успешно! Будем запрашивать ответ через 5 секунд")
        id = str(response.text).split('|')[1]
        while True:
            time.sleep(5)
            print("Запрос ответа...")
            response = requests.get("https://rucaptcha.com/res.php?key=" + key + "&action=get&id=" + id)
            if(str(response.text).split('|')[0] == "OK"):
                print("Капча готова: " + str(response.text).split('|')[1])
                send("Капчу решил: " + str(response.text).split('|')[1])
                return str(response.text).split('|')[1]
            elif(str(response.text) == "CAPCHA_NOT_READY"):
                print("Капча еще не готова, повторим запрос через 5 сек...")
            else:
                print("Неизвестный ответ: " + str(response.text))
                if(input("Продолжить запросы? (y/n) ").upper() == "Y"):
                    print("Повторим запрос через 5 сек...")
                    continue
                else:
                    print("Отменено пользователем.")
                    return -1

def add_firend_captcha(id, sid, key):
    api.method('friends.add', {'user_id': id, 'captcha_sid': sid, 'captcha_key':key})

def send(message):
	sdghdyhtyj = 1 / 1
    #api.method('messages.send', {'peer_id': peer_id, 'message': message, "random_id": randint(-2147483648, 2147483648)})
i = firends
captcha_count = 0
added_users = [1]
while True:
    if(i==0): break
    while True:
        print("Получаю список...")
        post = api.method('wall.get', {'owner_id': "-25885216", "count":"1", 'filter':'others'})
        user_list = re.findall("[@][i][d]\\d+", post['items'][0]['text'])
        print("Получил список в {count} чел.".format(count = str(len(user_list))))
        if(len(user_list) > 0):
            print("Получил список в {count} чел.".format(count = str(len(user_list))))
            for user_id in user_list:
                if(i==0): 
                    print("Достигнут лимит накрутки")
                    break
                user_id = int(user_id.split('@id')[1])
                for added_user in added_users:
                    if(user_id == added_user):
                        continue
                print("Добавляю в друзья (http://vk.com/id" + str(user_id) + "/)...")
                try:
                    add_firend(user_id)
                except vk_api.Captcha as e:
                    try:
                        print("ВКонтакте просит капчу, начинаю решать...")
                        send("ВКонтакте просит капчу, начинаю решать...")
                        while True:
                            captcha_count += 1
                            captcha_compl = captcha(e.url)
                            if(captcha_compl == -1):
                                print("Отмена в связи с ошибкой капчи!")
                                break
                            else:
                                try:
                                    add_firend_captcha(user_id, e.sid, captcha_compl)
                                    break
                                except vk_api.Captcha as err:
                                    print("НЕПРАВИЛЬНАЯ КАПЧА!!!")
                                    send("НЕПРАВИЛЬНАЯ КАПЧА!!!")
                                    e = err
                                    continue
                    except:
                        print("Не получилось =(")
                        continue
                except:
                    print("Не получилось =(")
                    continue
                added_users.append(user_id)
                #send("Капча [id" + str(user_id) + "|" + user['first_name'] + " " + user['last_name'] + "]")
                send("Заявка отправлена @id" + str(user_id))
                print("Успешно добавил, выбираю следующего человека")
                i-=1
            if(i==0): break
        else:
            print("Получил пустой список, получаю еще")
            continue
print("Успешно отправлены заявки " + str(firends - i) + " людям.\nРешено капч: " + str(captcha_count) + " шт.\nПримерно потрачено на капчу: " + str((captcha_count * (44 / 1000))) + " руб.")
send("Успешно отправлены заявки " + str(firends - i) + " людям.\nРешено капч: " + str(captcha_count) + " шт.\nПримерно потрачено на капчу: " + str((captcha_count * (44 / 1000))) + " руб.")
input()