from flask import Flask, render_template, flash, redirect, session, url_for, logging, request
from data import Articles
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt

app = Flask(__name__)
app.config['MySQL_HOST'] = 'localhost'
app.config['MySQL_USER'] = 'root'
app.config['MySQL_PASSWORD'] = '214r'
app.config['MySQL_DB'] = 'myflaskapp'
app.config['MySQL_CURSOR'] = 'DictCursor'

# init mysql
mysql = MySQL(app)

# 2 VIDEO 29:24

Articles1 = Articles()

@app.route('/')
def index():
	return render_template('home.html')

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/articles')
def articles():
	return render_template('articles.html', articles=Articles1)

@app.route('/article/<string:id>')
def article(id):
	return render_template('article.html', id=id)


class RegisterForm(Form):
	name = StringField('Name', [validators.Length(min=1, max=50)])
	username = StringField('Username', [validators.Length(min=4, max=25)])
	email = StringField('Email', [validators.Length(min=6, max=50)])
	password = PasswordField('Password', [validators.DataRequired(), validators.EqualTo('confirm', message='passwords dont match')])
	confirm = PasswordField('Confirm Password')


@app.route('/register', methods=['GET','POST'])
def register():
	form = RegisterForm(request.form)
	if request.method == 'POST' and form.validate():
		name = form.name.data
		email = form.email.data
		username = form.username.data
		password = sha256_crypt.encrypt(str(form.password.data))

		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO users(name,email,username,password) VALUES (%s,%s,%s,%s)", (name, email, username, password))
		mysql.connection.commit()
		cur.close()
		flash('u are now registred and can log in', 'success')
		redirect(url_for('index'))
		return render_template('register.html')

	return render_template('register.html', form=form)



if __name__ == '__main__':
	app.run(debug = 1)
