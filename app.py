from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/index.html')
def indexone():
    return render_template("index.html")

@app.route('/locations.html')
def locations():
    return render_template("locations.html")

@app.route('/buildings.html')
def buildings():
    return render_template("buildings.html")

@app.route('/contact.html')
def contact():
    return render_template("contact.html")        

@app.route('/creators.html')
def creators():
    return render_template("creators.html")

@app.route('/data.html')
def data():
    return render_template("data.html")

@app.route('/rooms.html')
def rooms():
    return render_template("rooms.html")        