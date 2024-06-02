from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_KEY = 'c644de4e8719f62eaa36b0a1'
API_URL = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    data = request.get_json()
    amount = data['amount']
    from_currency = data['from_currency']
    to_currency = data['to_currency']

    response = requests.get(f'{API_URL}{from_currency}')
    if response.status_code != 200:
        return jsonify({'error': 'Error fetching conversion rates'}), 400

    rates = response.json().get('conversion_rates', {})
    rate = rates.get(to_currency)

    if rate:
        converted_amount = amount * rate
        return jsonify({'converted_amount': converted_amount})
    else:
        return jsonify({'error': 'Conversion rate not found'}), 400

if __name__ == '__main__':
    app.run(debug=True)
