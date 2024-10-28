import mysql.connector
from flask import Flask, render_template, url_for, request, redirect

def addUser(vehicleNumber,password):
    try:
        mycursor.execute(f"Insert into users (VehicleNumber,Password) Values ({vehicleNumber},{password})")
        mydb.commit()
    except:
        print(">>> There was some error adding user...:(")

app = Flask(__name__)

mydb = mysql.connector.connect(host="localhost",
                               user="root",
                               password="12451245",
                               database="ParkKaro")
mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE IF NOT EXISTS ParkKaro")
mycursor.execute("""CREATE TABLE IF NOT EXISTS Users (
                 VehicleNumber VARCHAR(20) PRIMARY KEY,
                 Password VARCHAR(20))""")

mycursor.execute("Select * from users")
locationVal = mycursor.fetchall()
print(locationVal)




@app.route('/',methods=['POST','GET'])
def index():
    if request.method == 'POST':
        addUser(request.form['vehicleNumber'],request.form['password']) # name of input 
        print(locationVal)
        try:
            return redirect('/')
        except:
            return "There was an issue finding your spot..:("
    else:
        return render_template("index.html",loca = locationVal)
    
@app.route('/login',methods=['POST','GET'])
def login():
    return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True)
    mycursor.close()
    mydb.close()    
        

