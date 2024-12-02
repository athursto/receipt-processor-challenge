import math
import datetime
import random
import string
from flask import Flask, jsonify, request

app = Flask(__name__)
data_store = {}


def get_store_chars(receipt):
    store_name = receipt.get("retailer", "")
    if not store_name:  # Check if the store_name is blank or None
        print("The retailer name is blank!")
        return
    store_chars = 0
    for letter in store_name:  # One point for every alphanumeric character
        if letter.isalnum():
            store_chars += 1
            # print(f"Adding {letter}, store_chars is {store_chars}")
    return store_chars


def get_round_points(receipt):
    num = receipt.get("total", "")
    if not num:  # Check if target is blank or None
        print("The total is blank!")
        return
    decimal = math.modf(float(num))[0]
    if decimal == .00:  # See if it's a rounded total
        return 50
    return 0


def get_quarter_points(receipt):
    num = receipt.get("total", "")
    if not num:  # Check if target is blank or None
        print("The total is blank!")
        return
    decimal = math.modf(float(num))[0]
    if decimal in (.00, .25, .50, .75):  # Find every total ending in multiple of .25
        return 25
    return 0


def get_points_per_two_items(receipt):
    item_total = receipt.get("items", 0)
    every_two = (len(item_total) // 2) * 5  # Multiply every pair of items by 5
    return every_two


def get_item_description_points(receipt):
    items = receipt.get("items", 0)
    desc_points = 0
    for item in items:  # Loop through items, finding the length of their trimmed names
        if len(item["shortDescription"].strip()) % 3 == 0:
            # print(f"{item['shortDescription']} is a match, with price of {item['price']}")
            desc_points += math.ceil(float(item["price"]) * .2)
    return desc_points


def get_purchase_day_points(receipt):
    date_input = receipt.get("purchaseDate", "")
    if not date_input:
        print("Receipt has no date")
        return
    date_format = '%Y-%m-%d'  # Not accounting for other date formats
    date_stripped = datetime.datetime.strptime(date_input, date_format).day
    if date_stripped % 2 != 0:  # 6 points if date is an odd number
        return 6
    return 0


def get_purchase_time_points(receipt):
    time_input = receipt.get("purchaseTime", "")
    if not time_input:
        print("Receipt has no time")
        return
    time_format = '%H:%M'  # Not accounting for other date formats
    time_stripped = datetime.datetime.strptime(time_input, time_format).time()
    after_time = datetime.time(14, 0, 0)
    before_time = datetime.time(16, 0, 0)
    if time_stripped > after_time and time_stripped < before_time:  # 10 points if after 2 pm and before 4 pm
        return 10
    return 0


# Function that takes in the receipt, then generates all the points
def score_total_receipt(receipt):
    point_total = get_store_chars(receipt) + get_round_points(receipt) + get_quarter_points(receipt) + \
                  get_points_per_two_items(receipt) + get_item_description_points(receipt) + get_purchase_day_points(
        receipt) + \
                  get_purchase_time_points(receipt)
    return point_total


def generate_alphanumeric_key(length):
    alphabet = string.ascii_letters + string.digits #Generates an alphanumeric key to use to save new entries
    return ''.join(random.choice(alphabet) for _ in range(length))


@app.route('/store', methods=['POST'])
def store_object():  # This will be modified to store receipts
    data = request.get_json()
    key = generate_alphanumeric_key(15)
    value = score_total_receipt(data)  # Generates receipt score

    if key is None or value is None:
        return jsonify({'error': 'Missing key or value'}), 400

    data_store[key] = value
    return jsonify({'id': key})


@app.route('/retrieve/<key>', methods=['GET'])
def retrieve_object(key):  # This will retrieve receipts-- the key will be receipt ID
    if key in data_store:
        return jsonify({'value': data_store[key]})
    else:
        return jsonify({'error': 'Key not found'}), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
