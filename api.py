from lib import *
from flask import Flask, request

app = Flask(__name__)

SHOPIFY_ORDERS = "Shopify Orders File"
PAYU_TRANSACTIONS = "PayU Transactions File"
ABANDONED_CART = "Shopify Abandoned Cart File"


@app.route('/')
def index():
    return "sambar stories"


@app.route('/process', methods=['POST'])
def process():
    request_json = request.get_json()
    print(request_json)
    responses = request_json["responses"]

    shopify_orders = ""
    payu_trans = ""
    abandoned_carts = ""

    for response in responses:
        if(response["title"] == SHOPIFY_ORDERS):
            shopify_orders = response["response"]

        if(response["title"] == PAYU_TRANSACTIONS):
            payu_trans = response["response"]

        if(response["title"] == ABANDONED_CART):
            abandoned_carts = response["response"]

    return process_inputs(get_csv_file_from_url(payu_trans), get_csv_file_from_url(shopify_orders),
                          get_csv_file_from_url(abandoned_carts))
