import mysql.connector
from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime

def addUser(vehicleNumber,password):
    try:
        mycursor.execute("SELECT * FROM users WHERE vehicleNumber=%s",(vehicleNumber,))
        if len(mycursor.fetchone())==0:
            mycursor.execute("Insert into users (VehicleNumber,Password) Values (%s, %s)",(vehicleNumber,password))
            mydb.commit()
            return 1
        else:
            return 0
    except mysql.connector.Error as error:
        print(">>> There was some error adding user...:( "+str(error))
        return -1

def getPassword(vehicleNumber):
    try:
        mycursor.execute("Select password from users where vehiclenumber = %s",(vehicleNumber,))
        password = mycursor.fetchone()
        if password==None:
            return -1
        else:
            return password[0]
    except mysql.connector.Error as error:
        print(">>> There was some error searching for vehicle...:( "+str(error))
        return -1

def getData():
    try:
        mycursor.execute("SELECT * from users")
        return mycursor.fetchall()
    except mysql.connector.Error as error:
        print(">>> There was some error retriving data...:( "+str(error))

def getAvailableSpots(location):
    try:
        mycursor.execute(f"SELECT * FROM {location} WHERE isAvailable=TRUE")
        spots = mycursor.fetchall()
        if len(spots)==0:
            return 0
        else:
            return spots
    except mysql.connector.Error as error:
        print(">>> There was some error finding spot...:( "+ str(error))

def addBooking(vehicleNumber,spotId):
    try:
        mycursor.execute("INSERT INTO bookings (vehicleNumber,parking_spot_id) VALUES (%s,%s)",(vehicleNumber,spotId))
        table=spotId.split('_')[1]
        if table == "RR":
            table = "rr_nagar"
        elif table == "MR":
            table = "magadi_road"
        elif table == "P":
            table = "pattanagere"
        mycursor.execute(f"UPDATE {table} SET isAvailable=FALSE WHERE parking_spot_id='{spotId}'")
        mydb.commit()
        return 1
    except mysql.connector.Error as error:
        print(">>> There was some error booking...:( "+ str(error))
        return -1
    
def makeAvailable(spotId):
    try:
        table=spotId.split('_')[1]
        if table == "RR":
            table = "rr_nagar"
        elif table == "MR":
            table = "magadi_road"
        elif table == "P":
            table = "pattanagere"
        mycursor.execute(f"UPDATE {table} SET isAvailable=TRUE WHERE parking_spot_id='{spotId}'")
        mydb.commit()
        return 1
    except mysql.connector.Error as error:
        print(">>> There was some error booking...:( "+ str(error))
        return -1
    
def checkIfBooked(vehicleNumber):
    try:
        mycursor.execute("SELECT * FROM bookings WHERE vehicleNumber = %s",(vehicleNumber,))
        output=mycursor.fetchone()
        if output == None:
            return 0
        else:
            return output
    except mysql.connector.Error as error:
        print(">>> There was some error checking bookings...:( "+ str(error))
        return -1
def calcCost(bookingId):
    try:
        mycursor.execute(f"UPDATE bookings SET endTime=current_timestamp WHERE bookingId='{bookingId}'")
        mycursor.execute(f"UPDATE bookings SET duration=TIMESTAMPDIFF(minute,startTime, endTime) WHERE bookingId='{bookingId}'")
        mycursor.execute("SELECT TIMESTAMPDIFF(minute,startTime, endTime)*0.167 from bookings where bookingId=%s",(bookingId,))
        return mycursor.fetchone()
    except mysql.connector.Error as error:
        print(">>> There was some error calculating cost...:( "+ str(error))
        return -1

    
app = Flask(__name__)

mydb = mysql.connector.connect(host="localhost",
                               user="root",
                               password="12451245",
                               database="ParkKaro")
mycursor = mydb.cursor()
# mycursor.execute("CREATE DATABASE IF NOT EXISTS ParkKaro")
# mycursor.execute("""CREATE TABLE IF NOT EXISTS Users (
#                  VehicleNumber VARCHAR(20) PRIMARY KEY,
#                  Password VARCHAR(20))""")
# mycursor.execute("""CREATE TABLE IF NOT EXISTS rr_nagar (
#     parking_spot_id VARCHAR(10) PRIMARY KEY,
#     isAvailable BOOLEAN NOT NULL
# );""")
# mycursor.execute("""CREATE TABLE IF NOT EXISTS magdi_road (
#     parking_spot_id VARCHAR(10) PRIMARY KEY,
#     isAvailable BOOLEAN NOT NULL
# );""")
# mycursor.execute("""CREATE TABLE IF NOT EXISTS pattanagere (
#     parking_spot_id VARCHAR(10) PRIMARY KEY,
#     isAvailable BOOLEAN NOT NULL
# );""")
# mycursor.execute("""INSERT INTO rr_nagar (parking_spot_id, isAvailable) VALUES
# ('5a_MR', FALSE),
# ('4a_MR', TRUE);""")
# mycursor.execute("""
# INSERT INTO pattanagere (parking_spot_id, isAvailable) VALUES
# ('5b_MR', FALSE);""")
# mycursor.execute("""
# INSERT INTO magdi_road (parking_spot_id, isAvailable) VALUES
# ('5c_MR', TRUE);""")

# mycursor.execute("Select * from users")
# locationVal = mycursor.fetchall()
# print(locationVal)
# print(getPassword('Sumans'))
# print(addUser('herdev','roti'))
# print(getData())
loggedInVehicle = None

@app.route('/',methods=['POST','GET'])
def index():
    global loggedInVehicle
    if loggedInVehicle == None:
        return redirect('/login')
    if checkIfBooked(loggedInVehicle):
        return redirect('/checkout')
    if request.method == 'POST':
        try:
            return redirect('/')
        except:
            return "There was an issue finding your spot..:("
    else:
        return render_template("index.html") #,loca = getData()



@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        global loggedInVehicle
        pw = getPassword(request.form['vehicleNumber']) # name of input 
        givenPw = request.form['password']
        if pw == givenPw:
            print("Correct password")
            loggedInVehicle= request.form['vehicleNumber']
            if checkIfBooked(loggedInVehicle):
                return redirect('/checkout')
            else:
                return redirect('/')
        elif pw == -1:
            return render_template('login.html', comment = 'Create your account by signing up...:)')
        else:
            return render_template('login.html', comment = 'Wrong password...:)')
    else:
        return render_template('login.html',)
    
@app.route('/<location>')
def showAvailableSpots(location):
    return render_template("index.html", availableSpots=getAvailableSpots(location))

@app.route('/signUp',methods=['POST','GET'])
def signUp():
    if request.method == 'POST':
        global loggedInVehicle
        code=addUser(request.form['vehicleNumber'],request.form['password']) # name of input 
        if code ==1:
            loggedInVehicle= request.form['vehicleNumber']
            return redirect('/')
        elif code ==0:
            return render_template('signUp.html',comment="Account already exists...")
    else:
        return render_template('signUp.html') 

    
@app.route("/logout")
def logout():
    global loggedInVehicle
    loggedInVehicle=None
    return redirect('/')

@app.route("/book/<spotId>",methods=['POST','GET'])
def booking(spotId):
    if request.method == 'POST':
        addBooking(loggedInVehicle,spotId)
        
        return f"Booking Confirmed for vehicle {loggedInVehicle}\nParking Spot: {spotId}"
    loc = spotId.split("_")[1]
    if loc == "RR":
        loc = "Rajarajeshwari Nagar"
    elif loc == "MR":
        loc = "Magadi Road"
    elif loc == "P":
        loc = "Pattanagere"

    return render_template("book.html",location=loc,date = datetime.now().date(), time = datetime.now().time(),spot_id = spotId)
    
@app.route("/checkout",methods=['POST','GET'])
def checkout():
    global loggedInVehicle
    data = checkIfBooked(loggedInVehicle)
    if request.method == 'POST':
        makeAvailable(data[2])
        return "Thank you come back again"
    loc = data[2].split('_')[1]
    if loc == "RR":
        loc = "Rajarajeshwari Nagar"
    elif loc == "MR":
        loc = "Magadi Road"
    elif loc == "P":
        loc = "Pattanagere"
    return render_template("checkout.html",bookingId=data[0],vehicle_number=data[1],parking_spot=data[2],location=loc,duration=data[4],cost=calcCost(data[0]))

if __name__ == "__main__":
    app.run(debug=True)
    # print(checkIfBooked('Suman')[2].split('_')[1])
    mycursor.close()
    mydb.close()    