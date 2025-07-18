from arpit_restaurantAPP import app
from flask import request,jsonify,make_response

from model.order_model import order_model

orders = order_model()

@app.route("/orders/place/<int:rid>/<int:customer_id>", methods=["POST"])
def place_order_controller(rid, customer_id):
    try:
        data = request.get_json()
        if not data:
            return make_response({"message": "Missing JSON data"}, 400)

        
        return orders.place_order(customer_id, rid, data)

    except Exception as e:
        return make_response({"error": str(e)}, 500)
@app.route("/orders/<order_id>", methods=["GET"])
def get_order_by_id(order_id):
    return orders.get_order_by_id(order_id)

@app.route("/orders/customer/<customer_id>", methods=["GET"])
def get_orders_by_customer(customer_id):
    return orders.get_orders_by_customer(customer_id)


@app.route("/orders/restaurant/<int:restaurant_id>", methods=["GET"])
def get_orders_by_restaurant_controller(restaurant_id):

    return orders.get_orders_by_restaurant(restaurant_id)

@app.route('/orders/bulk', methods=['POST'])
def create_bulk_orders():
    orderss = request.get_json()
    
    return orders.bulk_place_orders(orderss)


