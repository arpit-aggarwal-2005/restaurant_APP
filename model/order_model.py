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
                password="ARPIT@#aggarwal2005",
                database="restaurant_db"
            )
            self.con.autocommit = True
            self.cur = self.con.cursor(dictionary=True)
            print("✅ MySQL connected for order_model")
        except Exception as e:
            print("❌ DB connection error in order_model:", e)

    def place_order(self, customer_id, rid, data):
        try:
            dishes = data.get("dishIDs")
            quantity = data.get("quantity")

            if not dishes or not quantity or len(dishes) != len(quantity):
                return make_response({"error": "Invalid order data"}, 400)

            # Map dish IDs to their corresponding quantities
            quantities = {dishes[i]: quantity[i] for i in range(len(dishes))}

            # Use parameterized query for IN clause
            format_strings = ','.join(['%s'] * len(dishes))

            self.cur.execute(
                f"SELECT id, price FROM dishes WHERE id IN ({format_strings})",
                tuple(dishes)
            )
            result = self.cur.fetchall()

            if len(result) != len(dishes):
                return make_response({"error": "Some dishes not found"}, 400)

            # Calculate total amount
            total_amount = 0
            for row in result:
                dish_id = row["id"]
                price = row["price"]
                qty = quantities[dish_id]
                total_amount += price * qty

            ordered_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Insert into orders table
            self.cur.execute("""
                INSERT INTO orders (customer_id, rid, total_amount, ordered_at)
                VALUES (%s, %s, %s, %s)
            """, (customer_id, rid, total_amount, ordered_at))
            
            order_id = self.cur.lastrowid

            # Insert into order_dishes table
            for i in range(len(dishes)):
                self.cur.execute("""
                    INSERT INTO order_dishes (dish_ids, orderid, quantity)
                    VALUES (%s, %s, %s)
                """, (dishes[i], order_id, quantity[i]))

            return make_response({
                "message": "Order placed successfully",
                "order_id": order_id,
                "total_amount": total_amount
            }, 201)

        except Exception as e:
            return make_response({"error": str(e)}, 500)

    def get_order_by_id(self, order_id):
        order_id = int(order_id)
        print(order_id)
        print()
        self.cur.execute(f"SELECT * FROM orders WHERE id = {order_id}")
        result = self.cur.fetchone()
        self.cur.execute(f"SELECT dish_ids AS DISH , quantity FROM order_dishes WHERE orderid = {order_id}")
        result2 = self.cur.fetchall()
        if self.cur.rowcount>0:
            return make_response({"payload": result,
                                  "dishes":result2}, 200)
        return make_response({"message": "Order not found"}, 404)

    def get_order_by_cid(self, cid):
        try:
            cid = int(cid)

            # Get all orders of the customer
            self.cur.execute("SELECT * FROM orders WHERE customer_id = %s", (cid,))
            orders = self.cur.fetchall()

            if not orders:
                return make_response({"message": "No orders found for this customer"}, 404)

            all_data = []

            for order in orders:
                # Get dishes for the current order
                self.cur.execute("SELECT dish_ids, quantity FROM order_dishes WHERE orderid = %s", (order['id'],))
                dishes = self.cur.fetchall()

                all_data.append({
                    "dishes": dishes,
                    "order": order
                    
                })

            return make_response({"orders": all_data}, 200)

        except Exception as e:
            return make_response({"error": str(e)}, 500)




    def get_order_by_rid(self, cid):
        try:
            cid = int(cid)

            # Get all orders of the customer
            self.cur.execute("SELECT * FROM orders WHERE rid = %s", (cid,))
            orders = self.cur.fetchall()

            if not orders:
                return make_response({"message": "No orders found for this customer"}, 404)

            all_data = []

            for order in orders:
                # Get dishes for the current order
                self.cur.execute("SELECT dish_ids, quantity FROM order_dishes WHERE orderid = %s", (order['id'],))
                dishes = self.cur.fetchall()

                all_data.append({
                    "dishes": dishes,
                    "order": order
                    
                })

            return make_response({"orders": all_data}, 200)

        except Exception as e:
            return make_response({"error": str(e)}, 500)