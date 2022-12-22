from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re


app = Flask(__name__)


# app.secret_key = '12345'


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'toor'
app.config['MYSQL_DB'] = 'hostus'


mysql = MySQL(app)


@app.route('/')
@app.route('/index/', strict_slashes=False)
def index():
    """ Display home page and all the hostels"""
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM Hostel')
    hostel = cursor.fetchone()
    return render_template("Index.html", hostel=hostel)


@app.route('/login/', strict_slashes=False, methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'Username' in request.form and 'Password' in request.form:
        Username = request.form['Username']
        Password = request.form['Password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM User WHERE Username = % s AND Password = % s', (Username, Password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['Owner_id'] = account['Owner_id']
            session['Username'] = account['Username']
            msg = 'Logged in successfully !'
            return render_template('Profile.html', msg=msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('Login.html', msg=msg)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'Owner_name' in request.form and 'Email' in request.form and 'Phone_no' in request.form and 'Username' in request.form and 'Password' in request.form:
        Owner_name = request.form['Owner_name']
        Email = request.form['Email']
        Phone_no = request.form['Phone_no']
        Username = request.form['Username']
        Password = request.form['Password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM User WHERE username = % s', (Username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', Email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', Username):
            msg = 'name must contain only characters and numbers !'
        else:
            cursor.execute('INSERT INTO User VALUES (NULL, % s, % s, % s, % s, % s)',
                           (Owner_name, Email, Phone_no, Username, Password, ))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('Signup.html', msg=msg)


# @app.route("/manage")
# def manage():
#     if 'loggedin' in session:
#         return render_template("Profile.html")
#     return redirect(url_for('login'))


@app.route("/profile")
def profile():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM User WHERE id = % s', (session['id'], ))
        account = cursor.fetchone()
        return render_template("Profile.html", account=account)
    return redirect(url_for('login'))


@app.route("/update", methods=['GET', 'POST'])
def update():
    msg = ''
    if 'loggedin' in session:
        if request.method == 'POST' and 'Owner_name' in request.form and 'Email' in request.form and 'Phone_no' in request.form and 'Username' in request.form and 'Password' in request.form:
            Owner_name = request.form['Owner_name']
            Email = request.form['Email']
            Phone_no = request.form['Phone_no']
            Username = request.form['Username']
            Password = request.form['Password']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                'SELECT * FROM User WHERE username = % s', (Username, ))
            account = cursor.fetchone()
            if account:
                msg = 'Account already exists !'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', Email):
                msg = 'Invalid email address !'
            elif not re.match(r'[A-Za-z0-9]+', Username):
                msg = 'name must contain only characters and numbers !'
            else:
                cursor.execute('UPDATE User SET  Owner_name =% s, Email =% s, Phone_no =% s, Username =% s, Password =% s', (
                    Owner_name, Email, Phone_no, Username, Password, (session['id'], ), ))
                mysql.connection.commit()
                msg = 'You have successfully updated !'
        elif request.method == 'POST':
            msg = 'Please fill out the form !'
        return render_template("Update.html", msg=msg)
    return redirect(url_for('login'))


@app.route('/about')
def about():
    """ Display About page"""
    return render_template("About.html")


@app.route('/contact')
def contact():
    """ Display Contact page"""
    return render_template("Contact.html")


@app.route('/index/<Hostel_id>')
def hostel():
    """ Display hostel page for the requested hostel at home page"""
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM Hostel WHERE Hostel_id = % s', (session['Hostel_id'], ))
    hostel = cursor.fetchone()
    return render_template("Hostel.html", hostel=hostel)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
