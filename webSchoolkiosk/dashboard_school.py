from flask import Flask,render_template,request,redirect
from DBCon import UseDatabase,ConError,UsernameLogErr,SQLError

app=Flask(__name__)


dbconfig = {'host': '127.0.0.1',
'user': 'root',
'passwd': '',
'db': 'db_sms_broadcast_sekolah', }

@app.route('/')
def home():
    return "dashboard"

@app.route('/loginusr')
def login_user():
    return render_template('login.html',the_title="login dulu!")


@app.route('/dashboard_sch')
def dashboard():
    return render_template('dashboard_sch.html',the_title="Dashboard!")

@app.route('/loginusr',methods=['POST'])
def cek_login():
    user_n=request.form['user_n']
    lgn = request.form['lgn']

    with UseDatabase(dbconfig) as cursor:
        _SQL = """select *, CAST(AES_DECRYPT(pass, '456') AS CHAR(255)) 
        xcd from tb_usx_l where 
        username=%s"""
        cursor.execute(_SQL, (user_n,))
        contents = cursor.fetchone()
        print(contents)
        if contents!=None:
            if contents[3] == lgn:
                return redirect('/dashboard_sch')
            else:
                return render_template('login.html', the_title="login dulu!", salah="Password salah!")
        else:
            return render_template('login.html', the_title="login dulu!", salah="Password salah!")


if __name__=='__main__':
    app.run(debug=True)
