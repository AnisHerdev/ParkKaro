lse

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