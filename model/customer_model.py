import mysql.connector
from flask import jsonify,make_response,request
from datetime import datetime, timedelta
import jwt

class customer_model():
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
            print("✅ MySQL connection established (restaurant_db)")
        except:
            print("❌ Error connecting to MySQL")

    def customer_addone_model(self, data):
        query = "INSERT INTO customers (name, email, phone, password) VALUES (%s, %s, %s, %s)"
        values = (
            data.get("name"),
            data.get("email"),
            data.get("phone"),
            data.get("password")  
        )
        self.cur.execute(query, values)
        return make_response({"message": "Customer created successfully"}, 201)

    def customer_login_model(self, data):
        query = f"""
            SELECT id, name, email, phone, avatar
            FROM customers
            WHERE email = '{data['email']}' AND password = '{data['password']}'
        """
        self.cur.execute(query)
        details = self.cur.fetchall()
        
        if not details:
            return make_response({"message": "Invalid login"}, 401)

        customer_data = details[0]
        exp_time = int((datetime.now() + timedelta(minutes=15)).timestamp())

        payload = {
            "customer": customer_data,
            "exp": exp_time
        }

        token = jwt.encode(payload=payload, key="arpit", algorithm="HS256")
        return make_response({"token": token}, 200)

    def customer_getall_model(self):
        self.cur.execute("SELECT * FROM customers")
        result = self.cur.fetchall()
        if result:
            res = make_response({"payload": result}, 200)
            res.headers["Access-Control-Allow-Origin"] = '*'
            return res
        return make_response({"message": "No customers found"}, 204)

    def customer_delete_model(self, id):
        self.cur.execute(f"DELETE FROM customers WHERE id = {id}")
        if self.cur.rowcount > 0:
            return make_response({"message": "Customer deleted successfully"}, 200)
        return make_response({"message": f"No customer with id = {id} found"}, 204)

    def customer_update_model(self, data):
        query = """
            UPDATE customers
            SET name=%s, email=%s, phone=%s, password=%s
            WHERE id = %s
        """
        values = (
            data.get("name"),
            data.get("email"),
            data.get("phone"),
            data.get("password"),
            int(data.get("id"))
        )
        self.cur.execute(query, values)
        if self.cur.rowcount > 0:
            return make_response({"message": "Customer updated successfully"}, 201)
        return make_response({"message": "Nothing to update"}, 202)

    def customer_patch_model(self, id, data):
        query = "UPDATE customers SET "
        for key in data:
            query += f"{key}='{data[key]}', "
        query = query.rstrip(', ') + f" WHERE id = {id}"
        self.cur.execute(query)
        if self.cur.rowcount > 0:
            return make_response({"message": "Customer updated successfully"}, 200)
        return make_response({"message": "Nothing to update"}, 202)

    def customer_upload_avatar(self, id, filename):
        self.cur.execute(f"UPDATE customers SET avatar = '{filename}' WHERE id = {id}")
        if self.cur.rowcount > 0:
            return make_response({"message": "Avatar uploaded"}, 200)
        return make_response({"message": "Upload failed"}, 202)

    def customer_pagination_model(self, limit, page):
        limit = int(limit)
        page = int(page)
        start = (limit * page) - limit
        query = f"SELECT * FROM customers LIMIT {start}, {limit}"
        self.cur.execute(query)
        result = self.cur.fetchall()
        if result:
            return make_response({"payload": result}, 200)
        return make_response({"message": "No data found"}, 204)
