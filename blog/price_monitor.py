from datetime import datetime
import time

from tabulate import tabulate
import requests

class MonitorPrice:
    def __init__(self, url, trip_msg):
        self.url = url
        self.trip_msg = trip_msg

    def get_price(self):
        r = requests.post(self.url, data=self.trip_msg)
        price_data = r.json()
        return price_data

    def filt_price_by_date(self, price_data, min_date, max_date):
        date_ls, price_ls = [], []
        for i in list(price_data['data'].values()):
            if i:
                data = i[0]
        for date, price in data.items():
            if int(min_date) <= int(date) <= int(max_date):
                date_ls.append(date)
                price_ls.append(price)
        return date_ls, price_ls

    def monitor_price(self, sleep, min_date, max_date):
        while 1:
            data = self.get_price()
            date, price = self.filt_price_by_date(data, min_date, max_date)
            date.append('Lowest Price')
            price.append(min(price))
            break
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S'), tabulate([price], headers=date, tablefmt='html')

if __name__ == '__main__':
    MonitorAirPrice = type('MonitorAirPrice', (MonitorPrice,), {})
    air_url = 'https://flights.ctrip.com/itinerary/api/12808/lowestPrice'
    trip_msg = {"flightWay":"Oneway","dcity":"CTU","acity":"BJS","army":False}

    monitor_air_price = MonitorAirPrice(air_url, trip_msg)
    print(monitor_air_price.monitor_price(60*10, '20190701', '20190707'))

