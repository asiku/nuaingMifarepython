from flask import Flask,render_template,request


app=Flask(__name__)

@app.route('/')
def home():
    return "dashboard"

@app.route('/loginusr')
def login_user():
    return render_template('login.html',the_title="Silahkan login dulu!")

@app.route('/loginusr',methods=['POST'])
def cek_login():
    user_n=request.form['user_n']
    lgn = request.form['lgn']
    return user_n + lgn

app.run(debug=True)
