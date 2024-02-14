from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = "top secret password don't tell anyone this"

items = [
    { "name": "Singer Sewing Machine M2105", "price": 149.99, "description": "Lightweight, beginner sewing maachine with one dial operation and 4 step buttonhole stitching.", "image_filename" : "SingerM1205SewingMachine.jpg"},
    { "name": "Beginner Sewing Kit", "price": 14.99, "description": "Sewing kit containing 12 different thread colours, 1 needle set, 1 seam ripper, 1 thimble, 1 pair of sewing scissors, 40 pins and 1 sewing cushion.", "image_filename" : "BeginnerSewingKit.jpg"},
    { "name": "Fabric Scissors", "price": 15.99, "description": '8" Heavy duty, sharp scissors with a case.', "image_filename" : "Scissors.jpg" },
]

class NumberForCartForm(FlaskForm):
    number_for_cart = IntegerField('Add how many to cart: ', validators = [DataRequired()])
    submit = SubmitField('Submit')

@app.route('/')
def galleryPage():
    return render_template('index.html', len = len(items), items = items)

@app.route('/item/<int:itemId>', methods=['GET','POST'])
def singleProductPage(itemId):
    form = NumberForCartForm()
    if form.validate_on_submit():
        return render_template('SingleItemConfirmation.html', item = items[itemId], number_for_cart = form.number_for_cart.data)
    else:
        return render_template('SingleItem.html', item = items[itemId], form = form)

if __name__ == '__main__':
    app.run(debug=True)
