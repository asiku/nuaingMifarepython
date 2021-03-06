from flask import Flask,render_template,request,redirect,session,flash,jsonify,url_for
from DBCon import UseDatabase,ConError,UsernameLogErr,SQLError
from cekcok import ceksess
# from datetime import timedelta
from helper_crud import Siswa
import os
from tulis_tag import tulis_kartu
from tulisk import tuliskartu
# import base64
from datetime import datetime
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
@ceksess
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

            print("tgllahir:"+request.form['tgl_lahir'])
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
        # try:
            f=(tbl.nis,tbl.nama,tbl.jk
               ,tbl.tempat,
               tbl.ala,tbl.nohpsiswa,tbl.nohportu
               ,tbl.idkelas,tbl.thnmasuk,tbl.tgllahir,tbl.nisn,tbl.stat
               ,tbl.gbr
               )
            # isi=("909","adem","L")
            # tglh = datetime.strptime(request.form['tgl_lahir'], '%Y-%m-%d')
            tglh=datetime.strptime(request.form['tgl_lahir'], '%d/%m/%Y')
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
                # str('1990/01/02'),
                str(tglh),
                str(request.form['nisn']),
                str(request.form['status'])
                , str(fname)
            )
            _SQL=tbl.insertsiswa(tbl.table)+str(f).replace("'","")+"VALUES"+str(isi)
            cursor.execute(_SQL)
        # except SQLError:
        #     pass

    # return "oke"


@app.route('/upload_fileedit', methods=['GET','POST'])
@ceksess
def upload_fileedit():

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

            editbio(bs64)

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

def editbio(img):

    with UseDatabase(dbconfig) as cursor:

            _SQL="UPDATE "+tbl.table+" SET "+ tbl.nama+"=%s,"+ tbl.jk+"=%s," \
                 + tbl.tempat+"=%s,"+ tbl.ala+"=%s,"+ tbl.nohpsiswa+"=%s,"\
                 + tbl.nohportu+"=%s,"+ tbl.idkelas+"=%s,"+ tbl.thnmasuk+"=%s,"\
                 + tbl.tgllahir+"=%s,"+ tbl.nisn+"=%s,"\
                 + tbl.stat+"=%s,"+ tbl.gbr+"=%s" + " WHERE  "+tbl.nis+"=%s"

            cursor.execute(_SQL, (request.form['nama'],request.form['jenis_kelamin'],
                                  request.form['tempat'],request.form['alamat']
                                  , request.form['nohpsiswa']
                                  , request.form['nohportu'],request.form['kelas']
                                  , request.form['tahun_masuk'],request.form['tgl_lahir']
                                  , request.form['nisn'], request.form['status']
                                  , request.form['nis'],img,))
    return redirect('/inputsiswa')

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
                           rows=contents,rowskelas=contentskelas,rowsstatus=contentsstatus,jalur=request.url_rule,tb=1)

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

@app.route('/caritb_nis/<cr>')
@ceksess
def caritbnis(cr):
    with UseDatabase(dbconfig) as cursor:
        _SQL="""select * from  tb_biodata_siswa where nis like %s or nama like %s"""
        cursor.execute(_SQL,("%" + cr + "%","%" + cr + "%",))
        contents = cursor.fetchall()
        tb_biodict=[]
        for c in contents:
            bio={ 'nis':c [0],'nama':c[1] }
            tb_biodict.append(bio)

    return jsonify(tb_biodict)

@app.route('/carialltb_nis')
@ceksess
def carialltbnis():
    with UseDatabase(dbconfig) as cursor:
        _SQL="""select * from  tb_biodata_siswa"""
        cursor.execute(_SQL)
        contents = cursor.fetchall()
        tb_biodict=[]
        for c in contents:
            bio={ 'nis':c [0],'nama':c[1] }
            tb_biodict.append(bio)

    return jsonify(tb_biodict)

@app.route('/cari_nisedit/<cr>')
@ceksess
def carinisedit(cr):
    with UseDatabase(dbconfig) as cursor:
        # _SQL="""select * from  tb_biodata_siswa where nis like %s"""
        # cursor.execute(_SQL,("%" + cr + "%",))

        _SQL = """select * from  tb_biodata_siswa where nis=%s"""
        cursor.execute(_SQL, (cr,))
        contents = cursor.fetchall()
        print(contents)
        tb_biodict = []
        for c in contents:
            tgl=c[9]
                # date,datetime.strftime('%Y-%m-%d')

            bio = {'nis': c[0], 'nama': c[1], 'jk': c[2], 'tlahir': c[3], 'alamat': c[4]
                , 'nohpsis': c[5], 'noportu': c[6], 'kelas': c[7], 'tmasuk': c[8]
               , 'tgllahir': tgl.strftime('%d-%m-%Y'), 'nisn': c[10],
                   'stat': c[11], 'img': c[12]}
            tb_biodict.append(bio)

    return jsonify(tb_biodict)

@app.route('/cari_nis/<cr>')
@ceksess
def carinis(cr):
    with UseDatabase(dbconfig) as cursor:
        # _SQL="""select * from  tb_biodata_siswa where nis like %s"""
        # cursor.execute(_SQL,("%" + cr + "%",))

        _SQL = """select * from  tb_biodata_siswa where nis=%s"""
        cursor.execute(_SQL, (cr,))
        contents = cursor.fetchone()
        print(contents)
        if contents != None:
           return jsonify({'result':'Mohon maaf Nis tersebut sudah Ada!'})
        else:
           return jsonify({'result':'ok'})



@app.route('/delsis/<rw>')
@ceksess
def delsiswa(rw):

    with UseDatabase(dbconfig) as cursor:
        _SQL = """delete from  tb_biodata_siswa where nis=%s"""
        cursor.execute(_SQL, (rw,))

    with UseDatabase(dbconfig) as cursor:
        # _SQL = """SELECT * FRom tb_biodata_siswa where nis=%s and Date(tgl_absen)=%s"""
        _SQL = """SELECT * FRom tb_biodata_siswa"""
        cursor.execute(_SQL)
        contents = cursor.fetchall()
        _SQL = """SELECT * FRom tb_kelas"""
        cursor.execute(_SQL)
        contentskelas = cursor.fetchall()
        _SQL = """SELECT * FRom tb_status"""
        cursor.execute(_SQL)
        contentsstatus = cursor.fetchall()
    return render_template('inputdatasiswa.html', the_title="Input Data Siswa!",
                           rows=contents,rowskelas=contentskelas,rowsstatus=contentsstatus,tb=2)

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

@app.errorhandler(500)
def handle_bad_request(e):
    rule = request.url_rule
    if 'upload_file' in rule.rule:
        flash("Data Tidak Tersimpan. Untuk mencari Data Tersimpan bisa di Check di Update siswa!", 'db')
        return redirect('/inputsiswa')
    elif 'statistiksiswa' in rule.rule:
        return redirect('/statistiksiswa')
    elif 'caridatasiswa' in rule.rule:
        return redirect('/caridatasiswa')
    elif 'inputkelas' in rule.rule:
        return redirect('/inputkelas')
    else:
        return 'Bad Request :( '

if __name__=='__main__':
    app.run(host='0.0.0.0',debug=True)
