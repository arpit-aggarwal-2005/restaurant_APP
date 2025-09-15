import mysql.connector
from flask import make_response,jsonify

class restaurant_model():
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
            print("✅ MySQL connection established (restaurant_model)")
        except:
            print("❌ Error connecting to MySQL (restaurant_model)")

    # Add a restaurant (requires owner_id)
    def add_restaurant(self, data):
        query = "INSERT INTO restaurants (name, cuisine, location, owner_id) VALUES (%s, %s, %s, %s)"
        values = (
            data.get("name"),
            data.get("cuisine"),
            data.get("location"),
            data.get("owner_id")  # Must be an existing customer ID
        )
        self.cur.execute(query, values)
        return make_response({"message": "Restaurant added successfully"}, 201)

    # Get all restaurants
    def get_all_restaurants(self):
        self.cur.execute("SELECT * FROM restaurants")
        result = self.cur.fetchall()
        if result:
            return make_response({"payload": result}, 200)
        return make_response({"message": "No restaurants found"}, 204)

    # Get all restaurants owned by a customer
    def get_restaurants_by_owner(self, owner_id):
        self.cur.execute(f"SELECT * FROM restaurants WHERE owner_id = {owner_id}")
        result = self.cur.fetchall()
        if result:
            return make_response({"payload": result}, 200)
        return make_response({"message": f"No restaurants found for owner {owner_id}"}, 204)

    # Update full restaurant (name, cuisine, location, and owner_id if needed)
    def update_restaurant(self, data):
        query = """
            UPDATE restaurants 
            SET name=%s, cuisine=%s, location=%s, owner_id=%s 
            WHERE id=%s
        """
        values = (
            data.get("name"),
            data.get("cuisine"),
            data.get("location"),
            data.get("owner_id"),
            int(data.get("id"))
        )
        self.cur.execute(query, values)
        if self.cur.rowcount > 0:
            return make_response({"message": "Restaurant updated"}, 200)
        return make_response({"message": "Nothing to update"}, 202)

    # Delete restaurant
    def delete_restaurant(self, id):
        self.cur.execute(f"DELETE FROM restaurants WHERE id = {id}")
        if self.cur.rowcount > 0:
            return make_response({"message": "Restaurant deleted"}, 200)
        return make_response({"message": f"No restaurant found with id = {id}"}, 204)

    # Patch restaurant fields (partial update)
    def patch_restaurant(self, id, data):
        query = "UPDATE restaurants SET "
        for key in data:
            query += f"{key}='{data[key]}', "
        query = query.rstrip(', ') + f" WHERE id = {id}"
        self.cur.execute(query)
        if self.cur.rowcount > 0:
            return make_response({"message": "Restaurant partially updated"}, 200)
        return make_response({"message": "Nothing to update"}, 202)
    def get_report_model(self,restaurant_id):
    
        self.cur.execute(f"""
            SELECT 
                AVG(mood_after - mood_before) AS avg_mood_change,
                AVG(service_rating) AS avg_service,
                AVG(taste_rating) AS avg_taste,
                (
                    AVG(mood_after - mood_before) + 
                    AVG(service_rating) + 
                    AVG(taste_rating)
                ) AS total_score
            FROM feedback
            WHERE restaurant_id = {restaurant_id};
        """)
        progress = self.cur.fetchone()
        self.cur.execute(f"""SELECT COUNT(*) + 1 AS 'rank'
FROM (
    SELECT 
        restaurant_id,
        AVG(mood_after - mood_before) + AVG(service_rating) + AVG(taste_rating) AS total_score
    FROM feedback
    GROUP BY restaurant_id
) AS sub
WHERE sub.total_score > (
    SELECT 
        AVG(mood_after - mood_before) + AVG(service_rating) + AVG(taste_rating)
    FROM feedback
    WHERE restaurant_id = {restaurant_id}
);

        """)

        rank  = self.cur.fetchall()
        


        # Get top-rated dish
        self.cur.execute(f"""
        SELECT d.id, d.name, d.rating
FROM dishes d
JOIN menus m ON d.menu_id = m.id
JOIN restaurants r ON m.restaurant_id = r.id
WHERE r.id = {restaurant_id}
ORDER BY d.rating DESC;

    """)
    
        dishes = self.cur.fetchall()
    

        # dish_list = [ 
        # {
        #     'dish_id': dish[0],
        #     'dish_name': dish[1],
        #     'rating': dish[2]
        # }for dish in dishes ]
           
        

        

        return jsonify({
            'restaurant_id': restaurant_id,
            'progress_report': progress,
            'dishes': dishes,
            'rank':rank
        })
