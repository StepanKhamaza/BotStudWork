import time
import requests
import logging

from bs4 import BeautifulSoup
from pymongo import MongoClient

from config import headers
from config import port

from handlers import get_badges
from handlers import get_deadline

from message import get_message

client = MongoClient('localhost', port)
db = client.OrdersID
posts = db.posts
logging.basicConfig(filename='app.log', filemode='w',level=logging.INFO)

def get_messages():
    result = []
    for page in range(1, 1000):
        orders_url = f"https://studwork.org/orders?page={page}"
        try:
            full_page = requests.get(orders_url, headers=headers)
        except requests.exceptions.RequestException as e:
            logging.exception(e)
            break

        soup = BeautifulSoup(full_page.content, 'html.parser')
        get_orders = soup.findAll('div', class_='order-list__items')
        get_orders_empty = soup.findAll('div', class_='order-list__empty')

        completed_status = False
        if not get_orders or get_orders_empty:
            break
        for order in get_orders[0]:
            status = order.find('div', class_='order-item__status').text.replace('\n', '').strip()
            if status == 'Выполнен':
                completed_status = True
                break

            badges = get_badges(order)
            link = f"https://studwork.org{order.find('a').get('href')}"
            topic = order.find('div', class_='order-item__heading').find('a').text.strip()

            all_essentials = order.find_all('li', class_='essential__item')
            id = int(all_essentials[0].text.strip()[2:])
            if posts.find_one({'id': id}) != None:
                if badges == 'Обычный':
                    completed_status = True
                    break
            logging.info(id)
            essentials = ''
            for i in range(1, len(all_essentials)):
                essentials += f"{all_essentials[i].text.strip()}\n"

            user_name = order.find('div', class_='user-link user-info__item user-info__item_user'). \
                text.replace('\n', '').strip()
            time_started = order.find('div', class_='date time-span__item_started'). \
                text.replace('\n', '').strip()
            deadline = get_deadline(order)

            posts.insert_one({'id': id})
            result.append(get_message([badges, topic, essentials, status, user_name, time_started, deadline, link]))

        if completed_status:
            break
    return result