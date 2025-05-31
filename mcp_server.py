from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/transfer_funds', methods=['POST'])
def transfer_funds():
    data = request.json
    recipient = data.get('recipient')
    amount = data.get('amount')
    currency = data.get('currency')

    print(f"Processing transfer: {amount} {currency} to {recipient}")

    return jsonify({
        "status": "success",
        "recipient": recipient,
        "amount": amount,
        "currency": currency
    })


if __name__ == '__main__':
    app.run(port=5000)