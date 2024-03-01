import sqlite3

def add_item(crsr, conn, item): #item is a list
    print("INSERT INTO items VALUES(" + str(item[0]) + ', "' + item[1] + '", "' +  item[2] + '", ' +  str(item[3]) + ', "' + item[4] + '");')
    crsr.execute("INSERT INTO items VALUES(" + str(item[0]) + ', "' + item[1] + '", "' +  item[2] + '", ' +  str(item[3]) + ', "' + item[4] + '");')
    conn.commit()
    
def delete_item(crsr, conn, item_id):
    crsr.execute("DELETE FROM items WHERE itemId =" + item_id + ";")
    conn.commit()
    
conn = sqlite3.connect('items.db')
crsr = conn.cursor()

# command = """CREATE TABLE items( 
#     itemId INT PRIMARY KEY NOT NULL,
#     name VARCHAR(40) NOT NULL,
#     description VARCHAR(120) NOT NULL,
#     price FLOAT NOT NULL,
#     imageName VARCHAR(40)
#    );"""

# crsr.execute(command)

item1 = [0, "Singer Sewing Machine M2105", "Lightweight, beginner sewing maachine with one dial operation and 4 step buttonhole stitching." , 149.99, "SingerM1205SewingMachine.jpg"]
item2 = [1, "Beginner Sewing Kit", "Sewing kit containing 12 different thread colours, 1 needle set, 1 seam ripper, 1 thimble, 1 pair of sewing scissors, 40 pins and 1 sewing cushion.", 14.99, "BeginnerSewingKit.jpg"]
item3 = [2, "Fabric Scissors", '8 inch Heavy duty, sharp scissors with a case.', 15.99, "Scissors.jpg"]

add_item(crsr, conn, item1)
add_item(crsr, conn, item2)
add_item(crsr, conn, item3)

conn.commit()

