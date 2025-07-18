import mysql.connector
from flask import make_response

class menu_model():
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
            print("✅ MySQL connected for menu_model")
        except Exception as e:
            print("❌ DB connection error:", e)

    # Add a menu
    def add_menu(self, data):
        query = "INSERT INTO menus (title, restaurant_id) VALUES (%s, %s)"
        values = (
            data.get("title"),
            data.get("restaurant_id")
        )
        self.cur.execute(query, values)
        return make_response({"message": "Menu added successfully"}, 201)

    # Get all menus
    def get_all_menus(self):
        self.cur.execute("SELECT * FROM menus")
        result = self.cur.fetchall()
        if result:
            return make_response({"payload": result}, 200)
        return make_response({"message": "No menus found"}, 204)

    # Get menus by restaurant (returns response)
    def get_menus_by_restaurant(self, rid):
        rid = int(rid)

        self.cur.execute(f"SELECT * FROM menus WHERE restaurant_id = {rid}")
        result = self.cur.fetchall()
        if self.cur.rowcount>0:
            return make_response({"payload": result}, 200)
        return make_response({"message": "No menus for given restaurant"}, 204)

    # Get menus by restaurant (returns raw data)
    
    # Update menu
    def update_menu(self, data):
        query = "UPDATE menus SET title = %s, restaurant_id = %s WHERE id = %s"
        values = (
            data.get("title"),
            data.get("restaurant_id"),
            data.get("id")
        )
        self.cur.execute(query, values)
        if self.cur.rowcount > 0:
            return make_response({"message": "Menu updated"}, 200)
        return make_response({"message": "Nothing to update"}, 202)

    # Delete menu
    def delete_menu(self, id):
        self.cur.execute("DELETE FROM menus WHERE id = %s", (id))
        if self.cur.rowcount > 0:
            return make_response({"message": "Menu deleted"}, 200)
        return make_response({"message": "Menu not found"}, 204)

    # Patch menu
    def patch_menu(self, id, data):
        query = "UPDATE menus SET "
        for key in data:
            query += f"{key}='{data[key]}', "
        query = query.rstrip(', ') + f" WHERE id = {id}"
        self.cur.execute(query)
        if self.cur.rowcount > 0:
            return make_response({"message": "Menu patched"}, 200)
        return make_response({"message": "Nothing to patch"}, 202)
