import mysql.connector
import json
from datetime import *
import jwt
from flask import *
import re
from functools import wraps
class auth_model():
    def __init__(self):
       
       try:
        
        self.con =  mysql.connector.connect(host = "localhost",user = "root",password ="BROKEN_devil2005",database = "flask_tutorial")
        self.con.autocommit = True
        self.cur = self.con.cursor(dictionary=True)

        print("connection established successfully")
       except:
          print("error occured")
    def auth_token(self,endpoint):
       def inner1(func):
          @wraps(func)
          def inner2(*args):
             authorization  = request.headers.get('authorization')
             
             if re.match(r"^Bearer *([^ ]+) *$", authorization, flags=0):
                token = authorization.split(" ")[1]
                
                print(token)
                try:
                   jwtdecoded = jwt.decode(token,key = "arpit",algorithms="HS256")
                except jwt.ExpiredSignatureError:
                   return make_response({"ERROR": " TOKEN EXPIRED"},401)
                role = jwtdecoded['user']['role_id']

                
                self.cur.execute(f"SELECT roles FROM new_view WHERE endpoint ='{endpoint}'")
                result = self.cur.fetchall()
                
                result = json.loads(result[0]['roles'])
                print(result)
                if len(result)>0:
                   if role in result:
                        
                        return func(*args)
                   else:
                      return make_response({"ERROR":"INVALID ROLE"},402)
                   
                else:
                   return make_response({"ERROR":"UNKNOWN ENDPOINT"},404)
                    
                   
             else:
                return make_response({"ERROR":"INVALID TOKEN"},404)
             
             return "OYE CHALEYA NHI"
            
             
          return inner2
       return inner1