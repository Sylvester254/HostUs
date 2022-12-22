#!/usr/bin/python3
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL


app = Flask(__name__)


# app.secret_key = '12345'

@app.route('/contact')
def contact():
    """ Display Contact page"""
    return render_template("Contact.html")