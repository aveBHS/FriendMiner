# -*- coding: utf-8 -*-
import vk_api
import time
from vk_api.longpoll import VkLongPoll, VkEventType
from random import randint
import os
from PIL import Image
import urllib.request
import requests

print("BHS VK FirendRequetCleaner v1.0\n-----------------------")
token = input("Токен пользователя: ")
api = vk_api.VkApi(token=token)

def del_firend(id):
    api.method('friends.delete', {'user_id': id})

def captcha(url):
    urllib.request.urlretrieve(url, "./Captcha/captcha.jfif")
    Image.open("./Captcha/captcha.jfif").save("./Captcha/captcha.png")

    key = "f18cca4cadb1c07bd6b528a476e144f1"
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

def del_firend_captcha(id, sid, key):
    api.method('friends.delete', {'user_id': id, 'captcha_sid': sid, 'captcha_key':key})

def send(message):
	sdghdyhtyj = 1 / 1
    #api.method('messages.send', {'peer_id': peer_id, 'message': message, "random_id": randint(-2147483648, 2147483648)})
captcha_count = 0
firends = 0
users = api.method('friends.getRequests', {'out': 1})['items']
for user in users:
    user_name = api.method('users.get', {'user_id': user, 'name_case':"dat"})[0]
    print("Удаляю из друзей " + user_name['first_name'] + " " + user_name['last_name'])
    try:
        del_firend(user)
    except vk_api.Captcha as e:
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
                    del_firend_captcha(user, e.sid, captcha_compl)
                    break
                except vk_api.Captcha as err:
                    print("НЕПРАВИЛЬНАЯ КАПЧА!!!")
                    send("НЕПРАВИЛЬНАЯ КАПЧА!!!")
                    e = err
                    continue
    firends += 1
print("Успешно отменены заявки " + str(firends) + " людям.\nРешено капч: " + str(captcha_count) + " шт.\nПримерно потрачено на капчу: " + str((captcha_count * (44 / 1000))) + " руб.")
send("Успешно отменены заявки " + str(firends) + " людям.\nРешено капч: " + str(captcha_count) + " шт.\nПримерно потрачено на капчу: " + str((captcha_count * (44 / 1000))) + " руб.")
input()