import utils
import os
import time

if not os.path.isfile('database.txt'):
    create = utils.generate_database()
    now = create[0]
    donate_name = create[1]
    donate_count = 0
    donate_need = create[2]
    if len(donate_name) + (len(str(donate_need))*2) + 6 >= 50:
        print("Статус не поместиться! Сократите имя!")
        os.remove("database.txt")
        os.remove("operations.txt")
        exit()
else:
    with open("database.txt", "r", encoding='UTF-8') as file:
        read = file.readlines()
        now = float(read[0].replace("\n", ""))
        donate_name = read[1].replace("\n", "")
        donate_count = int(read[2].replace("\n", ""))
        donate_need = int(read[3].replace("\n", ""))

import lolz_market
client = lolz_market.LolzMarket("")  # В КОВЫЧКАХ ВАШ LOLZ API TOKEN
while True:
    transactions = client.get_new_transactions()
    for i in transactions:
        donate_count += i
    if int(donate_count) >= int(donate_need):
        client.set_title(f"{donate_name} - Собрано")
    else:
        client.set_title(f"{donate_name} - [{donate_count}/{donate_need}]")
    time.sleep(10)
