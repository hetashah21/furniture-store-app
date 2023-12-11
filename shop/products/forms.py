from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import Form, IntegerField, StringField, TextAreaField, validators

class Addproducts(Form):
    name = StringField('Name', [validators.DataRequired()])
    price = IntegerField('Price', [validators.DataRequired()])
    discount = IntegerField('Discount', default=0)
    stock = IntegerField('Stock', [validators.DataRequired()])
    desc = TextAreaField('Description', [validators.DataRequired()])
    image = FileField('Image', validators=[FileRequired(), FileAllowed(['jpg','png', 'gif', 'jpeg'], 'images only please')])