from flask import Flask,render_template,request,redirect,session
from DBCon import UseDatabase,ConError,UsernameLogErr,SQLError
from cekcok import ceksess
from datetime import timedelta

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

@app.route('/logout')
def exit():
    session.pop('cekcok_login')
    return redirect('/loginusr')

# @app.before_request
# def make_session_permanent():
#     session.permanent = True
#     app.permanent_session_lifetime = timedelta(minutes=30)

@app.route('/inputsiswa')
@ceksess
def inputdatasiswa():
    with UseDatabase(dbconfig) as cursor:
        # _SQL = """SELECT * FRom tb_biodata_siswa where nis=%s and Date(tgl_absen)=%s"""
        _SQL = """SELECT * FRom tb_biodata_siswa"""
        cursor.execute(_SQL)
        contents = cursor.fetchall()
        print("biodata",contents)
    return render_template('inputdatasiswa.html',the_title="Input Data Siswa!",rows=contents)

@app.route('/caridatasiswa')
@ceksess
def caridatasiswa():
    return render_template('caridatasiswa.html',the_title="Cari Data Siswa!")

@app.route('/inputkelas')
@ceksess
def inputkelas():

    return render_template('inputkelas.html',the_title="Input Kelas")

@app.route('/statistiksiswa')
@ceksess
def statistiksiswa():
    return render_template('statistiksiswa.html',the_title="Statistik Siswa")

@app.route('/dashboard_sch')
@ceksess
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
                session['cekcok_login']=True
                return redirect('/dashboard_sch')
            else:
                return render_template('login.html', the_title="login dulu!", salah="Password salah!")
        else:
            return render_template('login.html', the_title="login dulu!", salah="Password salah!")

app.secret_key="simamaingsimamaung"

if __name__=='__main__':
    app.run(debug=True)
