from flask import Flask, render_template, request, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = "top secret password don't tell anyone this"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite3'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

class Item(db.Model):
    __tablename__ = 'items'
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
    cart = IntegerField('Add to cart: ', validators = [DataRequired()])
    submit = SubmitField('Submit')

@app.route('/')
def main_page():
    # If there is no cart initialised for a session, create a shopping cart
    if 'cart' not in session:
        print("New session", flush = True) 
        session['cart'] = []
    
    items = Item.query.all()
    return render_template('index.html', len = len(items), items = items)

@app.route('/item/<int:itemId>', methods=['GET','POST'])
def single_product_page(itemId):
    
    items = Item.query.all()  
    
    form = CartForm()
    if form.validate_on_submit():
        # Add the items to cart if an item is added
        session['cart'] += [f'{items[itemId].name} - £{items[itemId].price} - Quantity: {form.cart.data}']
        
        return render_template('single_item_confirmation.html', item = items[itemId], number_for_cart = form.cart.data)
    else:
        return render_template('single_item.html', item = items[itemId], form = form)
    
@app.route('/cart')
def cart_page():
    return render_template('cart.html', cart = session['cart'])

if __name__ == '__main__':
    app.run(debug=True)

"""<form method="post">
    <input type="number" id="quantity" name="quantity" value = 1 required=""/>
    <button type="submit">Add to Cart</button>
</form>"""