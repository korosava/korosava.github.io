from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow
import os
from forms import *

# init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 0

# init db
db = SQLAlchemy(app)
# init ma
ma = Marshmallow(app)


# product 
class Product(db.Model):
	id = db.Column(db.Integer, primary_key=1)
	name = db.Column(db.String(100), unique=1)
	desc = db.Column(db.String(200))
	price = db.Column(db.Float)
	qty = db.Column(db.Integer)

	def __init__(self, name, desc, price, qty):
		self.name = name
		self.desc = desc
		self.price = price
		self.qty  = qty

# product schema
class ProductSchema(ma.Schema):
	class Meta:
		fields = ('id', 'name', 'desc', 'price', 'qty')

#init schema
product_schema = ProductSchema(strict=1)
products_schema = ProductSchema(many=1, strict=1)


@app.route('/')
def index():
	return render_template('home.html')


#<=================_JSON_===================>
# create Product
@app.route('/product', methods = ['GET','POST'])
def add_product():
	if request.method == 'POST':
		name = request.form.get('name')
		desc = request.form.get('desc')
		price = request.form.get('price')
		qty = request.form.get('qty')

		new_product = Product(name, desc, price, qty)
		db.session.add(new_product)
		db.session.commit()
		return product_schema.jsonify(new_product)
	return render_template('home.html', todo='add')


# get all products
@app.route('/products', methods=['GET'])
def get_products():
	all_products = Product.query.all()
	res = products_schema.dump(all_products)
	return jsonify((res.data))


# get product by id
@app.route('/productbyid', methods=['POST', 'GET'])
def get_product_by_id():
	if  request.method == 'POST':
		id = request.form.get('id')
		product = Product.query.get(id)
		return product_schema.jsonify(product)
	return render_template('home.html', todo='getbyid')


# update Product
@app.route('/update', methods = ['GET', 'POST'])
def update_product():
	if  request.method == 'POST':
		id = request.form.get('id')
		product = Product.query.get(id)
		product.name = request.form.get('name')
		product.desc = request.form.get('desc')
		product.price = request.form.get('price')
		product.qty = request.form.get('qty')
		db.session.commit()
		return product_schema.jsonify(product)
	return render_template('home.html', todo='update')


# delete product by id
@app.route('/delete', methods=['GET', 'POST'])
def delete_product():
	if  request.method == 'POST':
		id = request.form.get('id')
		product = Product.query.get(id)
		db.session.delete(product)
		db.session.commit()
		return product_schema.jsonify(product)
	return render_template('home.html', todo='delete')



# run server
if __name__ == '__main__':
	app.run(debug=True)
