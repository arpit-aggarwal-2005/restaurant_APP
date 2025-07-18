"""
    SQL

       >insert into customer values(null,'john','+91 99999 11111','john@example.com');
       commands:->

     >   create database "name of the database";
      >  show database;
       > use "name of the database";
        >show tables;
       > create table customer(
       cid int primary key auto_increment,
       name text,
       phone text,
       email text
       );
       >describe customer;

"""
import mysql.connector as db

class Customer:
    def __init__(self) -> None:
        self.name=input("enter customer name :")
        self.phone=input("enter customer phont :")
        self.email=input("enter customer email :")

def main():
    customer=Customer()
    print(vars(customer))
    connection=db.connect(user='root',
                          password='BROKEN_devil2005',
                          host='127.0.0.1',
                          database='session13')
    cursor=connection.cursor()
    sql="insert into customer values (null,'{name}','{phone}','{email}');".format_map(vars(customer))
    cursor.execute(sql)
    connection.commit()
if __name__=="__main__" :

    main()

