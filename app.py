import mysql.connector
from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)

locationVal =[]

@app.route('/',methods=['POST','GET'])
def index():
    if request.method == 'POST':
        locationVal.append(request.form['location']) # id of input 
        try:
            return redirect('/login')
        except:
            return "There was an issue finding your spot..:("
    else:
        return render_template("index.html",loca = locationVal)
    
@app.route('/login',methods=['POST','GET'])
def login():
    return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True)

mydb = mysql.connector.connect(host="localhost",
                               user="root",
                               password="12451245",
                               database="ParkKaro")
mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE IF NOT EXISTS ParkKaro")
mycursor.execute("show databases")
