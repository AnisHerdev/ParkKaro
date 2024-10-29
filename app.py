import mysql.connector
from flask import Flask, render_template, url_for, request, redirect

def addUser(vehicleNumber,password):
    try:
        mycursor.execute(f"Insert into users (VehicleNumber,Password) Values ('{vehicleNumber}','{password}')")
        mydb.commit()
    except:
        print(">>> There was some error adding user...:(")
def getPassword(vehicleNumber):
    try:
        mycursor.execute(f"Select password from users where vehiclenumber = '{vehicleNumber}'")
        return mycursor.fetchall()
    except:
        print(">>> There was some error searching for vehicle...:(")

def getData():
    try:
        mycursor.execute("SELECT * from users")
        return mycursor.fetchall()
    except:
        print(">>> There was some error retriving data...:(")


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
print(getPassword('Suman')[0][0])
isLoggedin = False

@app.route('/',methods=['POST','GET'])
def index():
    global isLoggedin
    if isLoggedin == False:
        return redirect('/signUp')
    if request.method == 'POST':
        try:
            return redirect('/')
        except:
            return "There was an issue finding your spot..:("
    else:
        return render_template("index.html",loca = getData())
    
@app.route('/signIn',methods=['POST','GET'])
def signIN():
    if request.method == 'POST':
        global isLoggedin
        pw = getPassword(request.form['vehicleNumber'])[0][0] # name of input 
        givenPw = request.form['password']
        print(f'{"="*8} {pw} {"="*8}')
        print(f'{"="*8} {givenPw} {"="*8}')
        if pw == givenPw:
            print("Correct password")
            isLoggedin=True
            return redirect('/')
        else:
            return render_template('signIN.html', comment = 'Wrong password...:)')
    else:
        return render_template('signIN.html',)
    
@app.route('/signUp',methods=['POST','GET'])
def signUp():
    if request.method == 'POST':
        global isLoggedin
        addUser(request.form['vehicleNumber'],request.form['password']) # name of input 
        print(getData())
        isLoggedin=True
        return redirect('/')
    else:
        return render_template('signUp.html') 

    
@app.route("/logout")
def logout():
    global isLoggedin
    isLoggedin=False
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
    mycursor.close()
    mydb.close()    
        

