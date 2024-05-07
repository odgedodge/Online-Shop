from app import app, db, Product, ProductVariation, Review

#Blank template: { "name": "", "price": 0, "description": "", "image_filename": "", "environmental_rating": "", "environmental_description": "", "variations": []}

products = [
    { "name": "Singer Sewing Machine M2105", "price": 149.99, "description": "Lightweight, beginner sewing machine with one dial operation and 4 step buttonhole stitching.", "image_filename" : "SingerM1205SewingMachine.jpg", "environmental_rating": "6/10","environmental_description": "Sewing machines have environmental impacts as electronic devices, in that they do use electricity, as well as them adding to e-waste if not disposed of correctly. They are also made of plastics and polymers, so they should be disposed of with the proper care. However, moving to making your own clothes for yourself or friends is far better than participating in fast fashion, as well as being.", "variations": []},
    { "name": "Beginner Sewing Kit", "price": 14.99, "description": "Sewing kit containing 12 different thread colours, 1 needle set, 1 seam ripper, 1 thimble, 1 pair of sewing scissors, 40 pins and 1 sewing cushion.", "image_filename" : "BeginnerSewingKit.jpg", "environmental_rating": "4/10", "environmental_description": "This kit has a lot of little plastic parts and some aspects that may not be used, so it can be environmentally wasteful, so make sure that the aspects of this kit are necessary for your project. Take the proper care to recycling plastic parts. The overall environmental impact is poor due to the large amount of plastic involved.", "variations": []},
    { "name": "Fabric Scissors", "price": 15.99, "description": '8" Heavy duty, sharp scissors with a case.', "image_filename" : "Scissors.jpg" , "environmental_rating": "8/10", "environmental_description": "These scissors should last a long time, which is why we give a 10-year warranty for repairs. Look to sharpen these before seeking a replacement, and when disposing keep note of local metal and sharp handling policies. The making of these use a large amount of energy and water, so it is in the best interest of the environment to keep them functioning through repair and sharpening rather than to replace them. Make sure to only use this on fabric for best longevity - use on paper can cause bluntness.", "variations": []},
    { "name": "Simplicity Vintage Jiffy Dress Sewing Pattern S9594", "price": 10.99, "description": "Vintage dress sewing pattern. For sizes 6 -14. ", "image_filename" : "simplicity-sewing-pattern-s9594-jiffy-dress.webp", "environmental_rating": "9/10", "environmental_description": "Sewing patterns are made from paper, usually thin, tissue paper, as the Simplicity Vintage Jiffy Dress Sewing Papper S9594 is. This has a low environmental impact, however mass production of paper can cause issues with deforestation, so when disposing of this item make sure to recycle appropriately. Making your own clothes can also be beneficial for the environment, as we move into a period where fast fashion is more criticised for its negative environmental impact.", "variations": []},
    { "name": "Cutting Mat", "price": 9.99, "description": "A3 Cutting mat (20 x 45 x .3 cm)", "image_filename": "cutting_mat.jpg", "environmental_rating": "4/10", "environmental_description": "Rubber cutting mat, long lifespan. Synthetic, so poor environmental sustainability, and the production of rubber as whole has poor impacts on natural habitats due to deforestation. This rubber is not biodegradable. Overall, a poor sustainability rating.", "variations": []},
    { "name": "Fabric Measuring Tape", "price": 4.99, "description": "300cm fabric measuring tape – inch and cm dual sided", "image_filename": "fabric_measuring_tape.jpg", "environmental_rating": "6/10", "environmental_description": "Despite the name fabric – this is made of plastic. The type is recyclable but with a limit as it is difficult to recycle. Look to avoid replacing this, and when disposing take care to ensure that it has the best chances of being recycled", "variations": []},
    { "name": "Rotary Cutter", "price": 6.99, "description": "Rotary cutter (45mm) – Used for cutting fabric flat. Make sure to use with cutting mat", "image_filename": "rotary_cutter.jpg", "environmental_rating": "6/10", "environmental_description": "The materials consist of metal, which is recyclable; however primary material is plastic, poor recyclability but long lifespan. Look to sharpen over disposal.", "variations": []},
    { "name": "Sewing Needles", "price": 3.99, "description": "30 pieces straight hand sewing needles – assorted sizes", "image_filename": "sewing_needles.jpg", "environmental_rating": "8/10", "environmental_description": "Solely metal, recyclable and disposable with care. Sharp objects – take care. Environmentally friendly", "variations": []},
    { "name": "Sewing Pins", "price": 8.99, "description": "1200 Straight sewing pins with various colour heads", "image_filename": "sewing_pins.jpg", "environmental_rating": "7/10", "environmental_description": "This contains lots of little metal pieces, so make sure to be careful. Pieces are sharp so ensure to take proper care during disposal. Overall, this is pretty environmentally friendly, as very few people will lose or break amount of pins here, so no need for repurchase and/or frequent reproduction", "variations": []},
    { "name": "Sewing Machine Needles", "price": 7.99, "description": "Singer sewing machine needles – 10 pieces. Size 90/14", "image_filename": "singer_machine_needles.jpg", "environmental_rating": "8/10", "environmental_description": "Metal sewing needles, recyclable. Take care in disposal, as they are sharp, especially when broken", "variations": []},
    { "name": "Tailor's Chalk", "price": 4.49, "description": "Tailors chalk for marking fabric – 4 pieces, white, yellow, red and blue", "image_filename": "tailors_chalk.webp", "environmental_rating": "8/10", "environmental_description": "Chalk, biodegradable, however, uses large amounts of water during production. Overall, mostly environmentally friendly", "variations": []},
    { "name": "Cotton Fabric", "price": 7.99, "description": "Cotton Fabric priced per metre. Multiple quantities will be cut as one large sheet. 60 inch width. ", "image_filename": "blue_cotton_fabric.jpg", "environmental_rating": "7/10", "environmental_description": "Cotton fabric has a large water requirement for its making, but if treated correctly will last a long time, and will be more easily reused and last longer than polyester and plastic made fabric. Overall it has a good environmental rating. ", 
        "variations": [
            {"color": "white", "image_name": "white_cotton_fabric.jpg"},
            {"color": "black", "image_name": "black_cotton_fabric.jpg"},
            {"color": "blue", "image_name": "blue_cotton_fabric.jpg"},
            {"color": "red", "image_name": "red_cotton_fabric.jpg"},
            {"color": "green", "image_name": "green_cotton_fabric.jpg"}
        ]},
    { "name": "Polyester Thread", "price": 4.99, "description": "100% Polyester Gutermann Sew-all Thread, 250m", "image_filename": "blue_thread.webp", "environmental_rating": "8/10", "environmental_description": "Polyester thread is plastic, so it is more difficult to recycle, but the nature of thread makes it environmentally sustainable overall. However, it could contribute to microplastics", 
        "variations": [
            {"color": "white", "image_name": "white_thread.webp"},
            {"color": "black", "image_name": "black_thread.webp"},
            {"color": "blue", "image_name": "blue_thread.webp"},
            {"color": "red", "image_name": "red_thread.webp"},
            {"color": "green", "image_name": "green_thread.webp"}
        ]}
]


with app.app_context():
    db.create_all()
    
    # enumerate to manually set indexes to index at 0
    for index, product in enumerate(products):
        new_product = Product(id=index, name = product["name"], price = product["price"], description = product["description"], image_name = product["image_filename"], environmental_rating = product["environmental_rating"], environmental_description = product["environmental_description"])
        db.session.add(new_product)
        db.session.commit()
            # Add variations for the current product
        for variation_data in product.get("variations", []):
            new_variation = ProductVariation(product=new_product, color=variation_data["color"], image_name=variation_data["image_name"])
            db.session.add(new_variation)
            db.session.commit()
    
    