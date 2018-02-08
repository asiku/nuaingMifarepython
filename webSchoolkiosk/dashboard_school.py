from flask import Flask,render_template,request,redirect,session,flash,url_for
from DBCon import UseDatabase,ConError,UsernameLogErr,SQLError
from cekcok import ceksess
# from datetime import timedelta
from helper_crud import Siswa
import os
from tulis_tag import tulis_kartu
from tulisk import tuliskartu
# import base64

from werkzeug.utils import secure_filename

app=Flask(__name__)

tbl=Siswa()

dbconfig = {'host': '127.0.0.1',
'user': 'root',
'passwd': '',
'db': 'db_sms_broadcast_sekolah', }

UPLOAD_FOLDER = os.path.basename('gbrsiswa')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload_file', methods=['GET','POST'])
def upload_file():

    if request.method == 'POST':
        # check if the post request has the file part

        if 'file' not in request.files:
            flash('Anda belum Mengupload Foto Jika Lupa bisa di Edit di Tab Update','foto')
            return redirect(request.url)
        file = request.files['file']
        if request.form['nis'] != None:

            # if file.filename == '':
            #    img=base64.b64encode(file.read())

            # pth=os.path.dirname(os.path.realpath(__file__))
            # savedatasiswa(pth+'/'+os.path.join(app.config['UPLOAD_FOLDER']) + '/' + file.filename)
            bs64=request.form['imgpth']
            savedatasiswa(bs64)
            if request.form['radio-group1']=="ya":

               if tulis_kartu()=="Tap":
                  print("kartu tap")
                  tuliskartu(request.form['nis'])
               else:
                  print("kartu untap")
                  flash("Kartu Belum di Tap",'kartu')

        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('Anda belum Mengupload Foto Jika Lupa bisa di Edit di Tab Update','foto')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect('/inputsiswa')


    return redirect('/inputsiswa')

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

# @app.route('/savesiswa')
# @ceksess
def savedatasiswa(fname):
    with UseDatabase(dbconfig) as cursor:
        f=(tbl.nis,tbl.nama,tbl.jk
           ,tbl.tempat,
           tbl.ala,tbl.nohpsiswa,tbl.nohportu
           ,tbl.idkelas,tbl.thnmasuk,tbl.tgllahir,tbl.nisn,tbl.stat
           ,tbl.gbr
           )
        # isi=("909","adem","L")
        isi = (
            str(request.form['nis']),
            str(request.form['nama']),
             str(request.form['jenis_kelamin']),
            str(request.form['tempat']),
            str(request.form['alamat']),
            str(request.form['nohpsiswa']),
            str(request.form['nohportu']),
            str(request.form['kelas']),
            str(request.form['tahun_masuk']),
            str(request.form['tgl_lahir']),
            str(request.form['nisn']),
            str(request.form['status'])
            , str(fname)
        )
        _SQL=tbl.insertsiswa(tbl.table)+str(f).replace("'","")+"VALUES"+str(isi)
        cursor.execute(_SQL)
    # return "oke"

@app.route('/inputsiswa')
@ceksess
def inputdatasiswa():
    with UseDatabase(dbconfig) as cursor:
        # _SQL = """SELECT * FRom tb_biodata_siswa where nis=%s and Date(tgl_absen)=%s"""
        _SQL = """SELECT * FRom tb_biodata_siswa"""
        cursor.execute(_SQL)
        contents = cursor.fetchall()
        # print("biodata",contents)
        _SQL = """SELECT * FRom tb_kelas"""
        cursor.execute(_SQL)
        contentskelas = cursor.fetchall()
        _SQL = """SELECT * FRom tb_status"""
        cursor.execute(_SQL)
        contentsstatus = cursor.fetchall()

    return render_template('inputdatasiswa.html',the_title="Input Data Siswa!",
                           rows=contents,rowskelas=contentskelas,rowsstatus=contentsstatus)

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
    app.run(host='0.0.0.0',debug=True)
