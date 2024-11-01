import mysql.connector
from flask import Flask, render_template, url_for, request, redirect

def addUser(vehicleNumber,password):
    try:
        mycursor.execute("Insert into users (VehicleNumber,Password) Values (%s, %s)",vehicleNumber,password)
        mydb.commit()
    except mysql.connector.Error as error:
        print(">>> There was some error adding user...:( "+str(error))

def getPassword(vehicleNumber):
    try:
        mycursor.execute("Select password from users where vehiclenumber = %s",(vehicleNumber,))
        return mycursor.fetchall()[0][0]
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
        return mycursor.fetchall()
    except mysql.connector.Error as error:
        print(">>> There was some error finding spot...:( "+ str(error))

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

mycursor.execute("Select * from users")
locationVal = mycursor.fetchall()
print(locationVal)
# print(getPassword('Sumans'))
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
        return render_template("index.html") #,loca = getData()

@app.route('/<location>')
def showAvailableSpots(location):
    print(location)
    return render_template("index.html", availableSpots=getAvailableSpots(location))

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        global isLoggedin
        pw = getPassword(request.form['vehicleNumber']) # name of input 
        givenPw = request.form['password']
        print(f'{"="*8} {pw} {"="*8}')
        print(f'{"="*8} {givenPw} {"="*8}')
        if pw == givenPw:
            print("Correct password")
            isLoggedin=True
            return redirect('/')
        elif pw == -1:
            return render_template('login.html', comment = 'Create your account by signing up...:)')
        else:
            return render_template('login.html', comment = 'Wrong password...:)')
    else:
        return render_template('login.html',)
    
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