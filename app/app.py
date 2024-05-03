from flask import Flask, render_template, redirect, url_for, jsonify, request, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError, Regexp
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

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
    def serialize(self):
        return {"id": self.id,
                "name": self.name,
                "price": self.price,
                "description": self.description,
                "image_name": self.image_name,
                "environmental_rating": self.environmental_rating,
                "environmental_description": self.environmental_description}

class CartForm(FlaskForm):
    cart = IntegerField('Quantity: ', [DataRequired(), NumberRange(min=1)], render_kw={"type": "number", "min": "1"})
    submit = SubmitField('Add to Cart')
    
class CheckoutForm(FlaskForm):  
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=50)])
    card_number = StringField('Card Number', validators=[DataRequired(), Length(min=16, max=19, message='Invalid card number length'), Regexp(r'^(\d{4})([\s-])?(\d{4})\2?(\d{4})\2?(\d{4})$', message = "Invalid format. Please use no spaces, hyphens (-) or spaces")])
    expiration_date = StringField('Expiration Date', validators=[DataRequired(), Regexp(r'^\d{1,2}/\d{2,4}$', message='Invalid format. Please enter the date in the format MM/YYYY.')])
    cvv = StringField('CVV', validators=[DataRequired(), Regexp(r'^\d{3}$', message= "Invalid CVV. Should be 3 numerical digits")])
    submit = SubmitField('Submit')
    
    def validate_expiration_date(form, field):
        date_str = field.data
        # Extract month and year from the date string
        try:
            month, year = map(int, date_str.split('/'))
        except ValueError: 
            raise ValidationError('Invalid date. must be numerical values.')
        
        # Check if the month is between 1 and 12
        if not 1 <= month <= 12:
            raise ValidationError('Invalid month. Please enter a month between 01 and 12.')
        
        # If year is two digits, make 4
        current_year = datetime.now().year
        
        if 10 <= year <= 99:
            year = int(str(current_year // 100) + str(year))
        
        # Check if the date is later than the current date
        current_date = datetime.now()
        if year < current_date.year or (year == current_date.year and month < current_date.month):
            raise ValidationError('Expiration date must be in the future.')


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

@app.route('/get_description/<int:product_id>')
def get_description(product_id):
    # Retrieve the product description from the database or wherever it's stored
    product = Product.query.get_or_404(product_id)
    return jsonify({'description': product.description})

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
    return render_template('single_product.html', product=product, form=form)
    
@app.route('/cart')
def cart_page():
    cart = session.get('cart', [])
    products = Product.query.all()
    total_cost = calculate_total_cost(session['cart'], products)
    
    products_in_cart = []
    for item in cart:
        product_id = item["product_id"]
        product = Product.query.get(product_id)
        if product:
            products_in_cart.append({"product": product, "quantity": item["quantity"]})
    return render_template('cart.html', cart=products_in_cart, total_cost = total_cost)

@app.route('/clear_cart', methods=['POST'])
def clear_cart():
    session.pop('cart', None)
    session['cart'] = []
    return redirect(url_for('cart_page'))

@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    index = int(request.form['product_id'])
    if 'cart' in session:
        del session['cart'][index]
        session.modified = True
    return redirect(url_for('cart_page'))

@app.route('/reduce_quantity', methods=['POST'])
def reduce_quantity():
    index = int(request.form['product_id'])
    if 'cart' in session:
        session['cart'][index]['quantity'] -= 1
        if session['cart'][index]['quantity'] <= 0:
            del session['cart'][index]
        session.modified = True
    return redirect(url_for('cart_page'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout_page():
    form = CheckoutForm()
    if form.validate_on_submit():
        # Clear the cart
        session.pop('cart', None)
        session['cart'] = []
        return render_template('checkout_complete.html')
    return render_template('checkout.html', form=form)

def calculate_total_cost(cart, products):
    total_cost = 0
    for item in cart:
        product_id = item['product_id']
        # Find the product with the matching ID
        product = next((p for p in products if p.id == product_id), None)
        if product:
            total_cost += product.price * item['quantity']
    return total_cost

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
