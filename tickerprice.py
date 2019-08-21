# command line program to fetch current WTI price
import argparse
import time
import requests
import json
import datetime

parser = argparse.ArgumentParser(description="Get current stock price from yahoo finance.", prog=('Ticker Price Fetcher'))

parser.add_argument("ticker", type=str, help='Ticker to look up on yahoo finance.')
parser.add_argument("-loop", default=60, type=int, help='set refresh rate for ticker price in seconds (default: 60 seconds)')

args = parser.parse_args()

ticker = str(args.ticker).upper()

try:
    prices = []
    update_number = 0

    print(f"Searching for {ticker} on Yahoo Finance...")
    while True:
        update_number += 1
        print(f"Update #{update_number}")
        soup = requests.get(f'https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?region=US&lang=en-US&includePrePost=false&interval=2m&range=1d&corsDomain=finance.yahoo.com&.tsrc=finance')

        json_response = json.loads(soup.text)
        dict_response = dict(json_response['chart']['result'][0]['meta'])

        current_price = dict_response['regularMarketPrice']
        time_taken = datetime.datetime.now().strftime("%b %d %Y %H:%M:%S")

        prices.append(current_price)

        try:
            last_change = round(((current_price-prices[-2])/prices[-2])*100, 2)
            print(f'{time_taken} - {ticker} @ ${current_price} - moved {last_change}%')
        except IndexError:
            print(f'{time_taken} - {ticker} @ ${current_price}')

        time.sleep(args.loop)

except KeyboardInterrupt:
    pass