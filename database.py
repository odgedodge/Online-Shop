from main import app, db, Product

products = [
    { "name": "Singer Sewing Machine M2105", "price": 149.99, "description": "Lightweight, beginner sewing machine with one dial operation and 4 step buttonhole stitching.", "image_filename" : "SingerM1205SewingMachine.jpg"},
    { "name": "Beginner Sewing Kit", "price": 14.99, "description": "Sewing kit containing 12 different thread colours, 1 needle set, 1 seam ripper, 1 thimble, 1 pair of sewing scissors, 40 pins and 1 sewing cushion.", "image_filename" : "BeginnerSewingKit.jpg"},
    { "name": "Fabric Scissors", "price": 15.99, "description": '8" Heavy duty, sharp scissors with a case.', "image_filename" : "Scissors.jpg" },
]
with app.app_context():
    db.create_all()
    
    for product in products:
        new_product = Product(name = product["name"], price = product["price"], description = product["description"], image_name = product["image_filename"])
        db.session.add(new_product)
        
    db.session.commit()
    
    