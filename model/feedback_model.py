import mysql.connector
from flask import make_response,request
from datetime import datetime

class FeedbackModel:
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
            print("✅ MySQL connected for feedback_model")
        except Exception as e:
            print("❌ DB connection error in feedback_model:", e)

    def add_feedback(self):
        try:
            # Use form or JSON depending on content type
            data = request.form if request.form else request.get_json()

            order_id = data.get("order_id")
            restaurant_id = data.get("restaurant_id")
            customer_id = data.get("customer_id")
            dish_id = data.get("dish_id")  # optional

            if not all([order_id, restaurant_id, customer_id]):
                return make_response({"error": "Required fields: order_id, restaurant_id, customer_id"}, 400)

            order_id = int(order_id)
            restaurant_id = int(restaurant_id)
            customer_id = int(customer_id)

            # Optional ratings and fields
            rating = float(data.get("rating", 0))
            taste_rating = float(data.get("taste_rating", 0))
            service_rating = float(data.get("service_rating", 0))
            mood_before = int(data.get("mood_before", ""))
            mood_after = int(data.get("mood_after", ""))
            comment = data.get("comment", "")

            query = """
                INSERT INTO feedback (
                    order_id, restaurant_id, customer_id, dish_id, rating,
                    taste_rating, service_rating, mood_before, mood_after, comment
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                order_id, restaurant_id, customer_id, dish_id, rating,
                taste_rating, service_rating, mood_before, mood_after, comment
            )
            self.cur.execute(query, values)

            # Update dish rating if present
            if dish_id:
                self.cur.execute("SELECT AVG(taste_rating) AS avg_taste FROM feedback WHERE dish_id = %s", (dish_id,))
                avg_taste = self.cur.fetchone()["avg_taste"]
                self.cur.execute("UPDATE dishes SET rating = %s WHERE id = %s", (avg_taste, dish_id))

            # Update restaurant rating
            self.cur.execute("""
                SELECT AVG((taste_rating + service_rating)/2) AS avg_res_rating
                FROM feedback
                WHERE restaurant_id = %s
            """, (restaurant_id,))
            avg_res_rating = self.cur.fetchone()["avg_res_rating"]
            self.cur.execute("UPDATE restaurants SET rating = %s WHERE id = %s", (avg_res_rating, restaurant_id))

            return make_response({"message": "Feedback submitted successfully"}, 201)

        except Exception as e:
            return make_response({"error": str(e)}, 500)
    def get_feedback_by_restaurant(self, restaurant_id):
        try:
            restaurant_id = int(restaurant_id)
        except ValueError:
            return make_response({"error": "Invalid restaurant ID"}, 400)

        query = """
            SELECT 
                f.id AS feedback_id,
                f.order_id,
                f.customer_id,
                f.dish_id,
                f.rating,
                f.taste_rating,
                f.service_rating,
                f.mood_before,
                f.mood_after,
                f.comment,
                c.name AS customer_name,
                d.name AS dish_name
            FROM feedback f
            LEFT JOIN customers c ON f.customer_id = c.id
            LEFT JOIN dishes d ON f.dish_id = d.id
            WHERE f.restaurant_id = %s
            ORDER BY f.id DESC
        """
        self.cur.execute(query, (restaurant_id,))
        results = self.cur.fetchall()

        if results:
            return make_response({"restaurant_id": restaurant_id, "feedbacks": results}, 200)
        return make_response({"message": "No feedback found for this restaurant"}, 204)

