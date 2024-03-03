from flask import Flask, render_template, request, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

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
    
    # in order to display a products details
    def serialise(self):
        return {"id": self.id,
                "name": self.name,
                "price": self.price,
                "description": self.description,
                "image_name": self.image_name}

class CartForm(FlaskForm):
    cart = IntegerField('Add to cart: ', [DataRequired(), NumberRange(1)])
    submit = SubmitField('Submit')

@app.route('/')
def main_page():
    # If there is no cart initialised for a session, create a shopping cart
    if 'cart' not in session:
        print("New session", flush = True) 
        session['cart'] = []
    
    products = Product.query.all()
    return render_template('index.html', len = len(products), products = products)

@app.route('/product/<int:productId>', methods=['GET','POST'])
def single_product_page(productId):
    
    products = Product.query.all()  
    
    form = CartForm(cart=1)
    
    if form.validate_on_submit():
        # Add the products to cart if an product is added
        session['cart'] += [f'{products[productId].name} - £{products[productId].price} - Quantity: {form.cart.data}']
        
        return render_template('single_product_confirmation.html', product = products[productId], number_for_cart = form.cart.data)
    else:
        return render_template('single_product.html', product = products[productId], form = form)
    
@app.route('/cart')
def cart_page():
    return render_template('cart.html', cart = session['cart'])

if __name__ == '__main__':
    app.run(debug=True)
