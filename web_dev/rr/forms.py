from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class ProductAddForm(FlaskForm):
	prod_name = StringField("name", validators=[DataRequired(), Length(min=1, max=32)])
	prod_desc = StringField("description", validators=[DataRequired(), Length(min=1, max=32)])
	prod_price = StringField("price", validators=[DataRequired(), Length(min=1, max=32)])
	prod_qty = StringField("quality", validators=[DataRequired(), Length(min=1, max=32)])
	submit = SubmitField('send product')

class ProductUpdateForm(FlaskForm):
	prod_id = StringField("name", validators=[DataRequired(), Length(min=1, max=32)])
	new_desc = StringField("description", validators=[DataRequired(), Length(min=1, max=32)])
	new_price = StringField("price", validators=[DataRequired(), Length(min=1, max=32)])
	new_qty = StringField("quality", validators=[DataRequired(), Length(min=1, max=32)])
	submit = SubmitField('update product')

class ProductdeleteForm(FlaskForm):
	prod_id = StringField("name", validators=[DataRequired(), Length(min=1, max=32)])
	submit = SubmitField('delete product')

class ProductGetByIdForm(FlaskForm):
	prod_id = StringField("name", validators=[DataRequired(), Length(min=1, max=32)])
	submit = SubmitField('get product')

