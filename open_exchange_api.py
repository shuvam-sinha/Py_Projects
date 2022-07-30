import requests
from cachetools import cached, TTLCache


class ApiLibrary:
    url_lastest = "https://openexchangerates.org/api/latest.json"
    url_historical = "https://openexchangerates.org/api/historical/"
    url_currencies = "https://openexchangerates.org/api/currencies.json"
    url_time_series = "https://openexchangerates.org/api/time-series.json"
    url_convert = "https://openexchangerates.org/api/convert/"
    url_ohlc = "https://openexchangerates.org/api/ohlc.json"
    url_usage = "https://openexchangerates.org/api/usage.json"



    def __init__(self, app_id):
        self.app_id = app_id

    @property
    @cached(cache=TTLCache(maxsize=2, ttl=900))
    def latest(self):
        data = requests.get(f"{self.url_lastest}?app_id={self.app_id}")
        return data.json()['rates']

    @cached(cache=TTLCache(maxsize=10, ttl=900))
    def historical(self, date):
        data = requests.get(f"{self.url_historical}{date}.json?app_id={self.app_id}")
        return data.json()['rates']

    def get_data(self, date):
        if date is None:
            return self.latest
        else:
            return self.historical(date)

    def convert(self, amount, output_currency, date):
        all_currencies = self.get_data(date)
        final = amount * all_currencies[output_currency]
        return final

    def print_exchange_rate(self, amount, output_currency, date=None):
        final_amount = self.convert(amount, output_currency, date)
        if date is None:
            print("Current: USD " + str(amount) + " = " + output_currency + " " + str(final_amount))
        else:
            print("On " + date + ": USD " + str(amount) + " = " + output_currency + " " + str(final_amount))

    #currencies
    @cached(cache=TTLCache(maxsize=10, ttl=900))
    def currencies(self):
        data = requests.get(self.url_currencies)
        return data.json()

    def get_currencies(self, input_currency):
        full_data = self.currencies()
        country = full_data[input_currency]
        return country

    def print_currencies(self, input_currency):
        getdata = self.get_currencies(input_currency)
        print(f"The country for {input_currency} is {getdata}")


    #time series
    @cached(cache=TTLCache(maxsize=10, ttl=900))
    def time_series(self, start_date, end_date, base_currency, symbol):
        url = f"{self.url_time_series}?app_id={self.app_id}&start={start_date}&end={end_date}&base={base_currency}&symbols={symbol}"
        print(url)
        data = requests.get(url)
        return data.json()['rates']

    def print_rates_time_series(self, start_date, end_date, base_currency, symbol):
        dates_and_rates = self.time_series(start_date, end_date, base_currency, symbol)
        dates = dates_and_rates.keys()
        counter = 0
        for tokens in dates_and_rates:
            date = dates[counter]
            currency = dates_and_rates[date]
            rate = currency[symbol]
            print(f"On {date}, the value of 1 {base_currency} was equal to {rate} {symbol}")

    #convert
    @cached(cache=TTLCache(maxsize=10, ttl=900))
    def convert_api(self, starting_amount, from_currency, to_currency):
        url = f"{self.url_convert}{starting_amount}/{from_currency}/{to_currency}?app_id={self.app_id}"
        print (url)
        data = requests.get(f"{self.url_convert}{starting_amount}/{from_currency}/{to_currency}app_id={self.app_id}")
        return data.json()

    def convert_amount(self, starting_amount, from_currency, to_currency):
        all_data = self.convert_api(starting_amount, from_currency, to_currency)
        response = all_data["response"]
        return response

    def print_response(self, starting_amount, from_currency, to_currency):
        final_amount = self.convert_amount(starting_amount, from_currency, to_currency)
        print(f"{starting_amount} {from_currency} is equal to {final_amount} {to_currency}")

    #ohlc
    @cached(cache=TTLCache(maxsize=10, ttl=900))
    def ohlc(self, start_time, period, symbols, base):
        data = requests.get(f"{self.url_ohlc}?app_id{self.app_id}&start_time={start_time}&period={period}&base={base}&symbols={symbols}")
        return data.json()["rates"]

    def print_rates(self,start_time, period, symbols, base, which_rate):
        rates = self.ohlc(start_time, period, symbols, base)
        token = rates[symbols]
        final_rate = token[which_rate]
        print (f"For {base}, the comparable {which_rate} {symbols} rate is {final_rate}")

    #usage
    @cached(cache=TTLCache(maxsize=10, ttl=900))
    def usage(self):
        data = requests.get(f"{self.url_usage}?app_id={self.app_id}")
        if "data1" in data.json():
            return data.json()["data1"]
        else:
            return None

    def get_account_plan(self):
        usage = self.usage()
        if usage is not None:
            if "plan" in usage and "name" in usage["plan"]:
                return usage["plan"]["name"]
            else:
                return None
        else:
            return None

    def get_usage(self):
        # user_usage = self.usage()["usage"]
        usage = self.usage()
        if usage is not None:
            if "requests" in usage["usage"] and "requests_quota" in usage["usage"] and "requests_remaining" in usage["usage"]:
                request = usage["usage"]["requests"]
                requests_quota = usage["usage"]["requests_quota"]
                requests_remaining = usage["usage"]["requests_remaining"]
                return request, requests_quota, requests_remaining
            else:
                return None
        else:
            return None

    def print_user_status(self):
        user_plan = self.get_account_plan()
        # user_requests, user_requests_quota, user_requests_remaining = self.get_usage()
        token = self.get_usage()
        if token is None:
            print ("Data unavailable")
        else:
            user_requests, user_requests_quota, user_requests_remaining = token
            print (f"You are on a {user_plan}. \nYour number of requests is {user_requests}. \nYour quota of requests is {user_requests_quota}. \nYour number of remaining requests is {user_requests_remaining}")
