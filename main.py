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

class NumberForCartForm(FlaskForm):
    number_for_cart = IntegerField('Add how many to cart: ', validators = [DataRequired()])
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
    
    form = NumberForCartForm()
    if form.validate_on_submit():
        # Add the items to cart if an item is added
        for i in range(form.number_for_cart.data):
            session['cart'] += [items[itemId]]
        return render_template('SingleItemConfirmation.html', item = items[itemId], number_for_cart = form.number_for_cart.data, cart = session['cart'])
    else:
        return render_template('SingleItem.html', item = items[itemId], form = form)

if __name__ == '__main__':
    app.run(debug=True)
