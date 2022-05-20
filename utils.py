import time


def generate_database():
    print("[Создание сбора средств]")
    now = time.time()
    donate_name = input("Введите название сбора: ")
    donate_need = input("Введите сколько нужно собрать: ")
    with open("database.txt", "w", encoding='UTF-8') as file:
        file.write(str(now) + "\n" + donate_name + "\n0\n" + donate_need)
        file.close()
    open('operations.txt', 'w').close()
    return now, donate_name, donate_need
