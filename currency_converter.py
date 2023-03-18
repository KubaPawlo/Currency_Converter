#code that allows to use the api to get current exchange rates


import json
import datetime
import urllib.request
import os


class RatioObtainer:
    base = None
    target = None

    def __init__(self, base, target):
        self.base = base
        self.target = target

    def was_ratio_saved_today(self):

        try:
            with open('exchange_rates.json') as f:
                data = json.load(f)
        except FileNotFoundError:
            return False


        today = datetime.date.today().strftime("%Y-%m-%d")
        if today in data:
            if self.base in data[today]:
                if self.target in data[today][self.base]:
                    return True
        return False

    def fetch_ratio(self):

        url = f"https://api.exchangerate.host/latest?base={self.base}&symbols={self.target}"
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read())


        with open('exchange_rates.json') as f:
            exchange_rates = json.load(f)

        today = datetime.date.today().strftime("%Y-%m-%d")
        if today not in exchange_rates:
            exchange_rates[today] = {}
        if self.base not in exchange_rates[today]:
            exchange_rates[today][self.base] = {}
        exchange_rates[today][self.base][self.target] = data['rates'][self.target]

        with open('exchange_rates.json', 'w') as f:
            json.dump(exchange_rates, f)

    def get_saved_ratio(self):

        try:
            with open('exchange_rates.json') as f:
                data = json.load(f)
        except FileNotFoundError:
            return None


        today = datetime.date.today().strftime("%Y-%m-%d")
        if today in data:
            if self.base in data[today]:
                if self.target in data[today][self.base]:
                    return data[today][self.base][self.target]
        return None

    def get_matched_ratio_value(self):
        return self.get_saved_ratio() or self.fetch_ratio()


ratio_obtainer = RatioObtainer('USD', 'CZK')


if not os.path.isfile('exchange_rates.json'):
    with open('exchange_rates.json', 'w') as f:
        json.dump({}, f)

ratio = ratio_obtainer.get_matched_ratio_value()


data = {'USD': {'CZK': ratio}}

print(data)