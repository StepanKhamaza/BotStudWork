import telebot
import requests
import time
from datetime import datetime
from bs4 import BeautifulSoup
from pymongo import MongoClient

def Time_int(time_started, k):
    time_int = 0
    if not k:
        now = datetime.now()
        year = str(now.year)
        month = str(now.month)
        if (now.month < 10):
            month = '0' + month
        day = str(now.day)
        if (now.day < 10):
            day = '0' + day
        hour = str(now.hour)
        if (now.hour < 10):
            hour = '0' + hour
        minute = str(now.minute)
        if (now.minute < 10):
            minute = '0' + minute

        time_int = int(year + month + day + hour + minute)
    else:
        dt = {'Янв': '1', 'Фев': '2', 'Мар': '3', 'Апр': '4', 'Мая': '5', 'Июн': '6', 'Июл': '7', 'Авг': '8', 'Сен': '9', 'Окт': '10', 'Ноя': '11', 'Дек': '12'}
        for i in dt:
            if i in time_started:
                now = datetime.now()
                year = str(now.year)
                month = dt[i]
                if (len(month) < 2):
                    month = '0' + month
                day = time_started[:2].strip()
                if (len(day) < 2):
                    day = '0' + day
                hour = time_started[-5] + time_started[-4]
                minute = time_started[-2] + time_started[-1]
                time_int = int(year + month + day + hour + minute)
                break

    return time_int

Token = 'Your bot token'
bot = telebot.TeleBot(Token)
@bot.message_handler(content_types='text')
def start_message(message):
    bot.send_message(12345, message) # The first parameter you channel id


headers = {'User-Agent': 'Your User-Agent'}
client = MongoClient('localhost', 27017)
db = client.OrdersID
posts = db.posts
Time = 0

while (True):
    Data = []
    for page in range(1, 1000):
        OrdersUrl = 'https://studwork.org/orders?page=' + str(page)
        FullPage = requests.get(OrdersUrl, headers=headers)
        Soup = BeautifulSoup(FullPage.content, 'html.parser')
        GetOrders = Soup.findAll('div', class_='order-list__items')
        GetOrdersEmpty = Soup.findAll('div', class_='order-list__empty')
        if not len(GetOrders) or len(GetOrdersEmpty):
            break

        ok = True
        for order in GetOrders[0]:
            def Badges():
                res = ''
                premium_status = order.find(class_='order-item-badges__badge order-item-badges__badge_premium')
                urgent_status = order.find(class_='order-item-badges__badge order-item-badges__badge_urgent')
                if (premium_status == None and urgent_status == None):
                    res = 'Обычный'
                elif urgent_status == None:
                    res = 'Premium'
                elif premium_status == None:
                    res = 'Срочный'
                else:
                    res = 'Premium, Срочный'
                return res
            def Deadline():
                res = order.find('div', class_='date time-span__item_ok')
                if res == None:
                    res = 'Не указана'
                else:
                    res = res.text.replace('\n', '').strip()
                return res
            badges = Badges()
            dlink = order.find('a').get('href')
            link = 'https://studwork.org' + dlink
            id = int(dlink[7:14])
            topic = order.find('div', class_='order-item__heading').find('span').text
            essential = order.find('ul', class_='essential').text.replace('\n', '').strip()
            status = order.find('div', class_='order-item__status').text.replace('\n', '').strip()
            if status == 'Выполнен':
                ok = False
                break
            user_name = order.find('div', class_='user-link user-info__item user-info__item_user').text.replace('\n', '').strip()
            time_started = order.find('div', class_='date time-span__item_started').text.replace('\n', '').strip()
            deadline = Deadline()
            time_int = Time_int(time_started, 1)

            if posts.find_one({'id': id}) != None:
                if badges == 'Обычный':
                    ok = False
                    break
            else:
                posts.insert_one({'id': id})
                Data.append([badges, topic, essential, status, user_name, time_started, deadline, link, time_int])

        if not ok:
            break

    max_Time = 0
    cnt_messages = 0
    for i in Data:
        max_Time = max(max_Time, i[-1])
        message = ''
        message += 'Значки: '
        for j in i[0]:
            message += str(j)
        message += '\n\n'

        message += 'Темы: '
        for j in i[1]:
            message += str(j)
        message += '\n\n'

        message += 'Типы работ: '
        for j in i[2]:
            message += str(j)
        message += '\n\n'

        message += 'Статус: '
        for j in i[3]:
            message += str(j)
        message += '\n\n'

        message += 'Пользователь: '
        for j in i[4]:
            message += str(j)
        message += '\n\n'

        message += 'Выложено: '
        for j in i[5]:
            message += str(j)
        message += '\n\n'

        message += 'Срок сдачи: '
        for j in i[6]:
            message += str(j)

        message += '\n'
        message += str(i[7])
        start_message(message)
        cnt_messages += 1
        if (cnt_messages % 30 == 0):
            time.sleep(1)

    Time = max(Time, max_Time)

bot.infinity_polling()