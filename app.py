from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

# Начальная цена токена в биткойнах
token_price = 0.000001  # Примерная цена в BTC
last_buyer_wallet = "1Cd8nZHAYFH7ZG8aJ1wfhCXhHuxzeRtqoB"  # Стартовый кошелек

def check_transaction_status(wallet_address):
    # Используем API Blockchair для получения информации о кошельке
    url = f'https://api.blockchair.com/bitcoin/dashboards/address/{wallet_address}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        transactions = data['data'][wallet_address]['transactions']

        for transaction in transactions:
            # Получаем сумму транзакции
            amount = transaction['outputs'][0]['value'] / 1e8  # Переводим сатоши в BTC
            if amount >= token_price:  # Проверяем, достаточно ли средств для покупки токена
                return True  # Транзакция найдена и подтверждена
        
        return False  # Транзакция не найдена или сумма недостаточна
    else:
        return False  # Ошибка при получении данных

@app.route('/')
def index():
    return render_template('index.html', price=token_price, wallet_address=last_buyer_wallet)

@app.route('/update')
def update():
    global last_buyer_wallet, token_price
    
    if check_transaction_status(last_buyer_wallet):
        token_price *= 2  # Увеличиваем цену токена
        
    return jsonify({'price': token_price, 'wallet_address': last_buyer_wallet})

if __name__ == '__main__':
    app.run(debug=True)