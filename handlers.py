from datetime import datetime

def get_badges(order):
    result = 'Premium, Срочный'
    premium_status = order.find(class_='order-item-badges__badge order-item-badges__badge_premium')
    urgent_status = order.find(class_='order-item-badges__badge order-item-badges__badge_urgent')

    if premium_status == None and urgent_status == None:
        result = 'Обычный'
    elif urgent_status == None:
        result = 'Premium'
    elif premium_status == None:
        result = 'Срочный'

    return result

def get_deadline(order):
    result = order.find('div', class_='date time-span__item_ok')
    if not result:
        result = "Не указана"
    else:
        result = result.text.replace('\n', '').strip()

    return result