import mysql.connector
from flask import make_response,request,jsonify
from datetime import datetime
import json

class order_model():
    def __init__(self):
        try:
            self.con = mysql.connector.connect(
                host="localhost",
                user="root",
                password="BROKEN_devil2005",
                database="restaurant_db"
            )
            self.con.autocommit = True
            self.cur = self.con.cursor(dictionary=True)
            print("✅ MySQL connected for order_model")
        except Exception as e:
            print("❌ DB connection error in order_model:", e)

    def place_order(self, customer_id, rid, data):
        try:
            dishes = data.get("dishes")
            if not dishes:
                return make_response({"message": "Missing dish list"}, 400)

            dish_ids = [item["id"] for item in dishes]
            quantities = {item["id"]: item["quantity"] for item in dishes}

            # Fetch dish prices
            format_strings = ','.join(['%s'] * len(dish_ids))
            self.cur.execute(f"SELECT id, price FROM dishes WHERE id IN ({format_strings})", tuple(dish_ids))
            result = self.cur.fetchall()

            if len(result) != len(dish_ids):
                return make_response({"message": "Some dishes not found"}, 400)

            # Calculate total
            total_amount = 0
            for row in result:
                dish_id = row["id"]
                price = row["price"]
                qty = quantities.get(dish_id, 1)
                total_amount += price * qty

            ordered_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Save order as JSON (dish_id and qty)
            order_json = json.dumps(dishes)

            self.cur.execute("""
                INSERT INTO orders (customer_id, rid, dish_ids, total_amount, ordered_at)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                customer_id,
                rid,
                order_json,
                total_amount,
                ordered_at
            ))

            return make_response({
                "message": "Order placed successfully",
                "total_amount": total_amount
            }, 201)

        except Exception as e:
            return make_response({"error": str(e)}, 500)

    def get_order_by_id(self, order_id):
        order_id = int(order_id)
        self.cur.execute(f"SELECT * FROM orders WHERE id = {order_id}")
        result = self.cur.fetchone()
        if self.cur.rowcount>0:
            return make_response({"payload": result}, 200)
        return make_response({"message": "Order not found"}, 404)

    def get_orders_by_customer(self, customer_id):
        customer_id = int(customer_id)
        self.cur.execute(f"SELECT * FROM orders WHERE customer_id = {customer_id}")
        result = self.cur.fetchall()
        if self.cur.rowcount>0:
            return make_response({"payload": result}, 200)
        return make_response({"message": "No orders found"}, 204)
    def get_orders_by_restaurant(self,rid):
        self.cur.execute(f"SELECT * FROM orders WHERE rid = {rid}")
        result = self.cur.fetchall()
        if self.cur.rowcount>0:
            return jsonify(result)
    def bulk_place_orders(self, orders_list):
        try:
            results = []

            for order_data in orders_list:
                customer_id = order_data["customer_id"]
                rid = order_data["restaurant_id"]
                dishes = order_data.get("dishes")

                if not dishes:
                    results.append({"customer_id": customer_id, "status": "error", "message": "Missing dish list"})
                    continue

                dish_ids = [item["id"] for item in dishes]
                quantities = {item["id"]: item["quantity"] for item in dishes}

                # Prepare format string for SQL IN clause
                format_strings = ','.join(['%s'] * len(dish_ids))
                self.cur.execute(
                    f"SELECT id, price FROM dishes WHERE id IN ({format_strings})", tuple(dish_ids)
                )
                result = self.cur.fetchall()

                if len(result) != len(dish_ids):
                    results.append({
                        "customer_id": customer_id,
                        "status": "error",
                        "message": "Some dish IDs not found"
                    })
                    continue

                # Calculate total
                total_amount = 0
                for row in result:
                    dish_id = row["id"]
                    price = row["price"]
                    qty = quantities.get(dish_id, 1)
                    total_amount += price * qty

                ordered_at = order_data.get("timestamp")
                if not ordered_at:
                    ordered_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                order_json = json.dumps(dishes)

                # Insert order
                self.cur.execute("""
                    INSERT INTO orders (customer_id, rid, dish_ids, total_amount, ordered_at)
                    VALUES (%s, %s, %s, %s, %s)
                """, (customer_id, rid, order_json, total_amount, ordered_at))

                results.append({
                    "customer_id": customer_id,
                    "status": "success",
                    "total_amount": total_amount
                })

            
            return make_response(results, 201)

        except Exception as e:
            
            return make_response({"message": "Bulk insert failed", "error": str(e)}, 500)

        
