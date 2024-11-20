from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)


token_price = 0.000001 
last_buyer_wallet = "1Cd8nZHAYFH7ZG8aJ1wfhCXhHuxzeRtqoB" 
def check_transaction_status(wallet_address):
  
    url = f'https://api.blockchair.com/bitcoin/dashboards/address/{wallet_address}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        transactions = data['data'][wallet_address]['transactions']

        for transaction in transactions:
         
            amount = transaction['outputs'][0]['value'] / 1e8
            if amount >= token_price:  
                return True 
        
        return False  
    else:
        return False

@app.route('/')
def index():
    return render_template('index.html', price=token_price, wallet_address=last_buyer_wallet)

@app.route('/update')
def update():
    global last_buyer_wallet, token_price
    
    if check_transaction_status(last_buyer_wallet):
        token_price *= 2 
        
    return jsonify({'price': token_price, 'wallet_address': last_buyer_wallet})

if __name__ == '__main__':
    app.run(debug=True)
