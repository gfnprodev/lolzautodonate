import requests
import time


class LolzMarket:
    def __init__(self, token: str):
        self.session = requests.session()
        self.session.headers = {'Authorization': 'Bearer ' + token}
        self.user_id = self.get_user()['user_id']
        self.all_payments = {}
        self.last_payment = None
        self.operations = []
        self.get_operations()

        with open('database.txt', 'r') as file:
            self.payment_time = float(file.readlines()[0].replace("\n", ""))
            file.close()

    def get_operations(self):
        with open('operations.txt', 'r', encoding='UTF-8') as file:
            for i in file.readlines():
                self.operations.append(int(i.replace("\n", "")))
            file.close()

    def get_user(self):
        response = self.session.get('https://api.lolz.guru/market/me').json()
        return response['user']

    def get_donates(self):
        n = 1
        while True:
            api_link = f'https://api.lolz.guru/market/user/{self.user_id}/payments?type=income&operation_id_lt={self.last_payment}'
            response = self.session.get(api_link).json()
            payments = response['payments']
            for payment in payments.values():
                if payment['operation_type'] == 'receiving_money':
                    if payment['operation_date'] >= self.payment_time:
                        self.all_payments[payment['operation_id']] = payment['incoming_sum']
            if response["hasNextPage"]:
                self.last_payment = response["lastOperationId"]
            else:
                break
            time.sleep(3)
            n += 1
        return self.all_payments

    def set_title(self, title: str):
        data = {'user_title': title}
        api_link = f"https://api.lolz.guru/users/{self.user_id}"
        response = self.session.put(api_link, data=data).json()

        return response

    def get_new_transactions(self):
        new_transactions = []
        donates = self.get_donates()
        f = open('operations.txt', 'a', encoding='UTF-8')
        for i in donates:
            if int(i) not in self.operations:
                self.operations.append(int(i))
                f.write(str(i) + "\n")
                new_transactions.append(int(donates[i]))
        f.close()
        return new_transactions
