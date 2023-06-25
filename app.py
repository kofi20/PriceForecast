from flask import Flask, render_template, url_for, flash, redirect
from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SubmitField,SelectField,DateField
from wtforms.validators import DataRequired, email_validator, Length, EqualTo
from datetime import datetime

from flask_mysqldb import MySQL

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = "CTKDANTE"
app.config['MY_SQL HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "dante"
app.config['MYSQL_DB'] = "users_db"

db = MySQL(app)

# creating the form class
class signupForm(FlaskForm):
    firstName = StringField('Enter Name', validators=[DataRequired(), Length(min=2, max=50)])
    secondName = StringField(validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Enter email', validators=[DataRequired()])
    phoneNumber = StringField('Enter Number', validators=[DataRequired(), Length(min=10, max=13)])
    password = PasswordField('Enter password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm passord', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


#creating another for class for user input
class user_input(FlaskForm):
    commodity = SelectField('Choose commodity To foreast', choices=[('sg', 'Sugar'),
                 ('mz', 'Maize'), ('rc', 'Rice'), ('bn', 'Beans')])
    
    forecasted_date = SelectField('Choose Month in which to forecast', choices=[('Jan', 'January'),
    ('Feb', 'Febuary'), ('Mar', 'March'), ('Apr', 'April'), ('May', 'May'), ('Jun', 'June'), 
    ('Jul', 'July'), ('Aug', 'August'), ('Sep', 'September'), ('Oct', 'October'), ('Nov', 'November'), ('Dec', 'December')])
    submit = SubmitField('Forecast')
    


@app.route('/')
def index():
    return render_template('index.html')
   

@app.route('/index.html')
def index1():
    return render_template('index.html')

#signup route
@app.route('/sign_up.html', methods=['GET', 'POST'])
def sign_up():
    
    form = signupForm()

    if form.validate_on_submit():
        print("Form validation successful")
        firstName = form.firstName.data
        secondName = form.secondName.data
        email = form.email.data
        phoneNumber =form.phoneNumber.data
        password = form.password.data
        password2 = form.confirm_password.data
        date_added = datetime.utcnow()
        

        cur = db.connection.cursor()
        cur.execute(" INSERT INTO user_info (FirstName, SecondName, email, phoneNumber,password, date_added ) VALUES (%s,%s,%s,%s,%s,%s)", (firstName, secondName, email, phoneNumber, password,date_added ))
        db.connection.commit()
        cur.close()
        return redirect(url_for('trends'))
        
    else: flash(form.errors)


        
           
    
    return render_template('sign_up.html',  
    form = form)

@app.route('/dashboard.html', methods = ['GET', 'POST']) 
def dashboard():
    form = user_input()
    # logic for choosing date
    

    return render_template('dashboard.html', form = form)


#Trends route
@app.route('/trends.html')
def trends():
    return render_template('trends.html')

#'About us' Route
@app.route('/about.html')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True)

