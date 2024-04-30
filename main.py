from flask import Flask, render_template, redirect, url_for, request, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

products = [
    { "name": "Singer Sewing Machine M2105", "price": 149.99, "description": "Lightweight, beginner sewing machine with one dial operation and 4 step buttonhole stitching.", "image_filename" : "SingerM1205SewingMachine.jpg", "environmental_rating": "6/10","environmental_description": "Sewing machines have environmental impacts as electronic devices, in that they do use electricity, as well as them adding to e-waste if not disposed of correctly. They are also made of plastics and polymers, so they should be disposed of with the proper care. However, moving to making your own clothes for yourself or friends is far better than participating in fast fashion, as well as being."},
    { "name": "Beginner Sewing Kit", "price": 14.99, "description": "Sewing kit containing 12 different thread colours, 1 needle set, 1 seam ripper, 1 thimble, 1 pair of sewing scissors, 40 pins and 1 sewing cushion.", "image_filename" : "BeginnerSewingKit.jpg", "environmental_rating": "4/10", "environmental_description": "This kit has a lot of little plastic parts and some aspects that may not be used, so it can be environmentally wasteful, so make sure that the aspects of this kit are necessary for your project. Take the proper care to recycling plastic parts. The overall environmental impact is poor due to the large amount of plastic involved."},
    { "name": "Fabric Scissors", "price": 15.99, "description": '8" Heavy duty, sharp scissors with a case.', "image_filename" : "Scissors.jpg" , "environmental_rating": "8/10", "environmental_description": "These scissors should last a long time, which is why we give a 10-year warranty for repairs. Look to sharpen these before seeking a replacement, and when disposing keep note of local metal and sharp handling policies. The making of these use a large amount of energy and water, so it is in the best interest of the environment to keep them functioning through repair and sharpening rather than to replace them. Make sure to only use this on fabric for best longevity – use on paper can cause bluntness."},
    { "name": "Simplicity Vintage Jiffy Dress Sewing Pattern S9594", "price": 10.99, "description": "Vintage dress sewing pattern. For sizes 6 -14. ", "image_filename" : "simplicity-sewing-pattern-s9594-jiffy-dress.webp", "environmental_rating": "9/10", "environmental_description": "Sewing patterns are made from paper, usually thin, tissue paper, as the Simplicity Vintage Jiffy Dress Sewing Papper S9594 is. This has a low environmental impact, however mass production of paper can cause issues with deforestation, so when disposing of this item make sure to recycle appropriately. Making your own clothes can also be beneficial for the environment, as we move into a period where fast fashion is more criticised for its negative environmental impact. "}
]


app = Flask(__name__)
app.config['SECRET_KEY'] = "top secret password don't tell anyone this"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite3'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), index=True, unique=True)
    price = db.Column(db.Float)
    description = db.Column(db.Text)
    image_name = db.Column(db.String(60))
    environmental_rating = db.Column(db.String(5))
    environmental_description = db.Column(db.String(600))
    
    # in order to display a products details
    def serialise(self):
        return {"id": self.id,
                "name": self.name,
                "price": self.price,
                "description": self.description,
                "image_name": self.image_name,
                "environmental_impact": self.environmental_impact}

class CartForm(FlaskForm):
    cart = IntegerField('Quantity: ', [DataRequired(), NumberRange(min=1)], render_kw={"type": "number", "min": "1"})
    submit = SubmitField('Add to Cart')

@app.route('/')
def main_page():
    sort_by = request.args.get('sort_by')
    
    # If there is no cart initialised for a session, create a shopping cart
    if 'cart' not in session:
        print("New session", flush = True) 
        session['cart'] = []
    
    products = Product.query.all()
    
    if sort_by == 'name':
        products = sorted(products, key=lambda x: x.name)
    elif sort_by == 'price':
        products = sorted(products, key=lambda x: x.price)
    elif sort_by == 'environmental_rating':
        products = sorted(products, key=lambda x: x.environmental_rating, reverse=True)
    
    form = CartForm()
    
    return render_template('main.html', len = len(products), products = products, form = form)

@app.route('/product/<int:product_id>', methods=['GET','POST'])
def single_product_page(product_id):
    product = Product.query.get_or_404(product_id)
    
    form = CartForm()
    
    if form.validate_on_submit():
        quantity = form.cart.data
        
        item_in_cart = False
        for item in session['cart']:
            if item["product_id"] == product_id:
                item["quantity"] += quantity
                item_in_cart = True
                break
        if not item_in_cart:
            session['cart'].append({"product_id": product_id, "quantity": quantity})
        # Explicitly update the session object
        session.modified = True
        return render_template('single_product_confirmation.html', product=product, quantity=quantity)
    else:
        return render_template('single_product.html', product=product, form=form)
    
@app.route('/cart')
def cart_page():
    cart = session.get('cart', [])
    print(cart)
    total_cost = calculate_total_cost(session['cart'], products)
    
    products_in_cart = []
    for item in cart:
        product_id = item["product_id"]
        product = Product.query.get(product_id)
        if product:
            products_in_cart.append({"product": product, "quantity": item["quantity"]})
    return render_template('cart.html', cart=products_in_cart, total_cost = total_cost)

@app.route('/checkout')
def checkout_page():
    return render_template('checkout.html')

@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    index = int(request.form['index'])
    if 'cart' in session:
        del session['cart'][index]
        session.modified = True
    return redirect(url_for('cart_page'))

@app.route('/reduce_quantity', methods=['POST'])
def reduce_quantity():
    index = int(request.form['index'])
    if 'cart' in session:
        session['cart'][index]['quantity'] -= 1
        if session['cart'][index]['quantity'] <= 0:
            del session['cart'][index]
        session.modified = True
    return redirect(url_for('cart_page'))

def calculate_total_cost(cart, products):
    total_cost = 0
    for item in cart:
        total_cost += products[item['product_id']]["price"] * item['quantity']
    return total_cost

if __name__ == '__main__':

    ## Currently a bug where cannot run the program using a db created in database file: must fix.
    with app.app_context():
        db.drop_all()
        db.create_all()
        
        # enumerate to manually set indexes to index at 0
        for index, product in enumerate(products):
            new_product = Product(id=index, name = product["name"], price = product["price"], description = product["description"], image_name = product["image_filename"], environmental_rating = product["environmental_rating"], environmental_description = product["environmental_description"])
            db.session.add(new_product)
            
        db.session.commit()
        
        app.run(debug=True)
