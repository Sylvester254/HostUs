#!/usr/bin/python3
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors


app = Flask(__name__)


# app.secret_key = '12345'


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'toor'
app.config['MYSQL_DB'] = 'hostus'


mysql = MySQL(app)


@app.route('/index')
def index():
    """ Display home page and all the hostels"""
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM Hostel')
    hostel = cursor.fetchone()
    return render_template("Index.html", hostel=hostel)