# BotStudWork

Автор: Хамаза Степан

## Описание
Основная работа бота - оповещать о новых заказах на сайте https://studwork.org/
Все сообщения приходят в один основной канал.

## Требования
* Python >=3.9.9
* Основные модули из `requirements.txt`

## Подробности
Файл `bot.py`(основной) - отвечает за запуск бота и отправку сообщений в канал с определенным `channel_id`.

Файл `get_data.py` - здесь написано самое интересное, реализация парсинга сайта, добавление всех `id` заказов в БД (возвращает список сообщений, которые нужно отправить).

Файл `handlers.py` - реализует две функции. В качестве параметра принимает фрагмент `html`-страницы, возвращает информацию о значкаих и времени сдачи.

Файл `message.py` - собирает одно целое сообщение из списка данных о заказе.

## Пример сообщения
![image](https://user-images.githubusercontent.com/102313283/205484801-5e686d0b-9727-48b6-b686-47a3e5bdadcb.png)