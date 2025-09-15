import mysql.connector
import pandas as pd
from flask import request,jsonify,make_response
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
class special_model():
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
    def recommendation_model(self,cid,data):
        self.cur.execute(f"""SELECT 
    a.oid AS id,
    a.quantity AS quantity,
    b.rating AS rating,
    b.mood_before AS mood_before,
    b.mood_delta AS mood_change,
    c.price AS price,
    c.rid AS rid
FROM 
    (
        SELECT 
            SUM(od.quantity) AS quantity,
            od.orderid AS oid,
            o.rid AS rid
        FROM 
            (SELECT * FROM orders WHERE customer_id = {cid}) o
        JOIN 
            order_dishes od ON o.id = od.orderid
        GROUP BY 
            o.rid, o.id
    ) a
JOIN 
    (
        SELECT 
            AVG((rating + service_rating)/2) AS rating,
            AVG(mood_before) AS mood_before,
            AVG(mood_after - mood_before) AS mood_delta,
            restaurant_id AS rid,
            order_id AS oid
        FROM 
            feedback
        WHERE 
            customer_id = {cid}
        GROUP BY 
            order_id, restaurant_id
    ) b ON a.rid = b.rid AND a.oid = b.oid
JOIN 
    (
        SELECT 
            total_amount AS price,
            id AS orderID,
            rid
        FROM 
            orders
        GROUP BY 
            rid, id
    ) c ON a.rid = c.rid AND a.oid = c.orderID;
""")
        
        result = self.cur.fetchall()
        if(len(result)<2):
            help = 10-len(result)
            return make_response({"message":f"please order more and give pending feedbacks to open this function {help} orders needed with feedbacks "},201)        
        print(type(result))
        columns = ['id', 'quantity', 'rating', 'mood_before', 'mood_change', 'price', 'rid']
        df = pd.DataFrame(result, columns=columns)
        print(df)
        df.drop('id', axis=1, inplace=True)
        
        
        # Assuming df is already created and 'id' is dropped
        # df.drop('id', axis=1, inplace=True)   <-- Already done

        # 1. Separate features and target
        X = df.drop('rid', axis=1)
        y = df['rid']

        # 2. Split into train and test sets (if dataset is very small, skip this)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

        # 3. Create and train the KNN model
        knn = KNeighborsClassifier(n_neighbors=1)
        knn.fit(X_train, y_train)

        # 4. Make predictions
        y_pred = knn.predict(X_test)

       
        accuracy = accuracy_score(y_test, y_pred)
        print("Accuracy:", accuracy)

        prediction = knn.predict(data)



        
        return jsonify(prediction)
    

        