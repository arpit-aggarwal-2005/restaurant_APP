import mysql.connector
from flask import make_response

class dish_model():
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
            print("✅ MySQL connected for dish_model")
        except Exception as e:
            print("❌ DB connection error in dish_model:", e)

    # Add a new dish
    def add_dish(self, data):
        query = "INSERT INTO dishes (name, price, description, menu_id) VALUES (%s, %s, %s, %s)"
        values = (
            data.get("name"),
            data.get("price"),
            data.get("description"),
            data.get("menu_id")
        )
        self.cur.execute(query, values)
        return make_response({"message": "Dish added successfully"}, 201)

    # Get all dishes
    def get_all_dishes(self):
        self.cur.execute("SELECT * FROM dishes")
        result = self.cur.fetchall()
        if result:
            return make_response({"payload": result}, 200)
        return make_response({"message": "No dishes found"}, 204)

    # Get dishes by menu ID - API response
    def get_dishes_by_menu(self, menu_id):
        menu_id = int(menu_id)
        self.cur.execute("SELECT * FROM dishes WHERE menu_id = %s", (menu_id,))
        result = self.cur.fetchall()
        if self.cur.rowcount > 0:
            return result
        else:
            return make_response({"MESSAGE":"NO DISHES :("})
        
    def update_dish(self, data):
        try:
            query = """
                UPDATE dishes 
                SET name = %s, price = %s, description = %s, menu_id = %s 
                WHERE id = %s
            """
            values = (
                data.get("name"),
                data.get("price"),
                data.get("description"),
                int(data.get("menu_id")),
                int(data.get("id"))
            )
            self.cur.execute(query, values)
            if self.cur.rowcount > 0:
                return make_response({"message": "Dish updated"}, 200)
            return make_response({"message": "Nothing to update"}, 202)
        except Exception as e:
            return make_response({"error": str(e)}, 400)

    def delete_dish(self, id):
        try:
            id = int(id)
        except ValueError:
            return make_response({"message": "Invalid ID"}, 400)

        self.cur.execute("DELETE FROM dishes WHERE id = %s", (id,))
        if self.cur.rowcount > 0:
            return make_response({"message": "Dish deleted"}, 200)
        return make_response({"message": "Dish not found"}, 204)

    def patch_dish(self, id, data):
        try:
            id = int(id)
        except ValueError:
            return make_response({"message": "Invalid ID"}, 400)

        if not data:
            return make_response({"message": "No data provided to patch"}, 400)

        query = "UPDATE dishes SET "
        values = []
        for key in data:
            query += f"{key} = %s, "
            values.append(data[key])
        query = query.rstrip(', ') + " WHERE id = %s"
        values.append(id)

        self.cur.execute(query, tuple(values))
        if self.cur.rowcount > 0:
            return make_response({"message": "Dish patched successfully"}, 200)
        return make_response({"message": "Nothing to patch"}, 202)
    def get_all_dishes_by_restaurant_id(self, restaurant_id):
        try:
            restaurant_id = int(restaurant_id)
        except ValueError:
            return make_response({"message": "Invalid restaurant ID"}, 400)

        # Step 1: Get all menu IDs from this restaurant
        self.cur.execute(f"SELECT id, title FROM menus WHERE restaurant_id = {restaurant_id}")
        menus = self.cur.fetchall()

        if not menus:
            return make_response({"message": "No menus found for this restaurant"}, 204)

        final_output = []
        for menu in menus:
            menu_id = menu["id"]
            self.cur.execute(f"SELECT * FROM dishes WHERE menu_id = {menu_id}")
            dishes = self.cur.fetchall()
            final_output.append({
                "menu_id": menu_id,
                "menu_title": menu["title"],
                "dishes": dishes
            })

        return make_response({"restaurant_id": restaurant_id, "menus_with_dishes": final_output}, 200)



            
            
        