from binance.client import Client
from flask import Flask, request
import pandas as pd
import requests
import json

app = Flask(__name__)


@app.route("/balance", methods=['GET'])
def main():
    api = str(request.args['Api'])
    secret_key = str(request.args['SecretKey'])

    # QIleDdQJSqnGpaH7JcxVVFF4JUkxl6F5YwqK5lL1aeY7hOSE49P36BGVsenPCkwd
    # MpzFx4NCFSrst5YSI24cNMIYFdhse1fby26kE8LwWjjHAQyRQ5O1SodhAQwRzxFp

    client = Client(api, secret_key)
    account = client.get_account()

    df = pd.DataFrame(account["balances"])
    df["free"] = df["free"].astype(float)
    df = df[df["free"] > 0]

    total = 0
    df = df.reset_index()  # make sure indexes pair with number of rows
    for index, row in df.iterrows():
        if not row['asset'] == "USDT":
            url = requests.get('https://api.binance.com/api/v1/ticker/price?symbol='+row['asset']+'USDT')
            data = url.json()

            if "price" in json.dumps(data):
                total += float(data['price']) * float(row['free'])

    return "$"+str(round(total, 2))


if __name__ == "__main__":
    app.run()
