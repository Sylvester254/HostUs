#!/usr/bin/python3
from flask import Flask, render_template, request, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors


app = Flask(__name__)


# app.secret_key = '12345'


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'toor'
app.config['MYSQL_DB'] = 'hostus'


mysql = MySQL(app)


@app.route('/index/<Hostel_id>')
def hostel():
    """ Display hostel page for the requested hostel at home page"""
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM Hostel WHERE Hostel_id = % s', (session['Hostel_id'], ))
    hostel = cursor.fetchone()
    return render_template("Hostel.html", hostel=hostel)