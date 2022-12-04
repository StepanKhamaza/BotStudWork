def get_message(data):
    return f"Значки: {data[0]}\n\n" \
           f"Темы: {data[1]}\n\n" \
           f"Типы работ:\n{data[2]}\n" \
           f"Статус: {data[3]}\n\n" \
           f"Пользователь: {data[4]}\n\n" \
           f"Выложено: {data[5]}\n\n" \
           f"Срок сдачи: {data[6]}\n{data[7]}"