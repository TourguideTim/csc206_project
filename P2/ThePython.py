#https://www.youtube.com/watch?v=4yaG-jFfePc&list=PLCC34OHNcOtolz2Vd9ZSeSXWc8Bq23yEz&index=2 helped me in here
import flask import Flask, render_template
app = flask(__name__)
@app.route('/user/<name>')
def user(name):
    return render_template("purchasing.html")
def user(name):
    return render_template("Selling.html")
def user(name):
    return render_template("Loginscreen.html")
def user(name):
    return render_template("PurchasingBuick.html")
def user(name):
    return render_template("landingPage.html")
    