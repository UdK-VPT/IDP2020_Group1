from flask import Flask, render_template, request
latitude = "NaN"
longitude = "NaN"
time_shift = "NaN"
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

@app.route('/user_location.html')
def user_location():
    return render_template("user_location.html")      

@app.route('/input1')
def input1():
    latitude = request.args.get("latitude")
    longitude = request.args.get("longitude")
    time_shift = request.args.get("time_shift")
    
    
   
