from main import app, db, Product

products = [
    { "name": "Singer Sewing Machine M2105", "price": 149.99, "description": "Lightweight, beginner sewing machine with one dial operation and 4 step buttonhole stitching.", "image_filename" : "SingerM1205SewingMachine.jpg", "environmental_impact": "Sewing machines have environmental impacts as electronic devices, in that they do use electricity, as well as them adding to e-waste if not disposed of correctly. They are also made of plastics and polymers, so they should be disposed of with the proper care. However, moving to making your own clothes for yourself or friends is far better than participating in fast fashion, as well as being.   "},
    { "name": "Beginner Sewing Kit", "price": 14.99, "description": "Sewing kit containing 12 different thread colours, 1 needle set, 1 seam ripper, 1 thimble, 1 pair of sewing scissors, 40 pins and 1 sewing cushion.", "image_filename" : "BeginnerSewingKit.jpg",  "environmental_impact": "This kit has a lot of little plastic parts and some aspects that may not be used, so it can be environmentally wasteful, so make sure that the aspects of this kit are necessary for your project. Take the proper care to recycling plastic parts. The overall environmental impact is poor due to the large amount of plastic involved."},
    { "name": "Fabric Scissors", "price": 15.99, "description": '8" Heavy duty, sharp scissors with a case.', "image_filename" : "Scissors.jpg" ,  "environmental_impact": "These scissors should last a long time, which is why we give a 10-year warranty for repairs. Look to sharpen these before seeking a replacement, and when disposing keep note of local metal and sharp handling policies. The making of these use a large amount of energy and water, so it is in the best interest of the environment to keep them functioning through repair and sharpening rather than to replace them. Make sure to only use this on fabric for best longevity – use on paper can cause bluntness."},
    { "name": "Simplicity Vintage Jiffy Dress Sewing Pattern S9594", "price": 10.99, "description": "Vintage dress sewing pattern. For sizes 6 -14. ", "image_filename" : "simplicity-sewing-pattern-s9594-jiffy-dress.webp",  "environmental_impact": "Sewing patterns are made from paper, usually thin, tissue paper, as the Simplicity Vintage Jiffy Dress Sewing Papper S9594 is. This has a low environmental impact, however mass production of paper can cause issues with deforestation, so when disposing of this item make sure to recycle appropriately. Making your own clothes can also be beneficial for the environment, as we move into a period where fast fashion is more criticised for its negative environmental impact. "}
]


with app.app_context():
    db.create_all()
    
    for product in products:
        new_product = Product(name = product["name"], price = product["price"], description = product["description"], image_name = product["image_filename"])
        db.session.add(new_product)
        
    db.session.commit()
    
    