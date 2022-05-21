import sqlite3


#database="C:/Users/Karim/Desktop/solution/website_files/website/Users.db"
database= r"C:\Users\khale\Desktop\FYP2\website_files\website\Users.db"
conn=sqlite3.connect(database)

c=conn.cursor()

#sql2="""INSERT INTO items(id,Item_name,Expiry,notfication_date,Category,user_id)VALUES(10,'popcorn','2023-06-04','2022-05-02','food',6)"""
sql2="""INSERT INTO items(id,Barcode,item_name,Category)VALUES(2,"b'3038351293809'","spaghetti","food")"""
c.execute(sql2)
conn.commit()
###sql1="""DELETE FROM inventory where id=1"""
#c.execute(sql1)
#conn.commit()