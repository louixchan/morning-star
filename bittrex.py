import pandas as pd
import json
import requests
import datetime
import sys

address = "https://bittrex.com/Api/v2.0/pub/market/GetTicks?"
# https://bittrex.com/Api/v2.0/pub/market/GetTicks?marketName=BTC-WAVES&tickInterval=thirtyMin&_=1499127220008
def fetch_bittrex_data(marketName, tickInterval, startDateTime):

    print("Fetching", marketName, "...")

    timestamp = int(startDateTime.timestamp())

    data = {
        "marketName": marketName,
        "tickInterval": tickInterval,
        "_": timestamp
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36',
    }

    s = requests.session()

    req = requests.Request("GET", address, data=data, headers=headers)

    prepped = req.prepare()
    response = s.send(prepped)

    sys.stdout = open("data/" + marketName + ".json", "a+")
    output = json.loads(str(response.content)[2:-1])
    # print(json.load(str(response.content[1:])))
    print(json.dumps(output, indent=4))
    sys.stdout = sys.__stdout__

    s.close()