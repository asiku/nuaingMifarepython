from DBCon import UseDatabase,ConError,UsernameLogErr,SQLError
from datetime import date,datetime


dbconfig = {'host': '127.0.0.1',
'user': 'root',
'passwd': '',
'db': 'db_sms_broadcast_sekolah', }

def InsertPresensi(nis):
    with UseDatabase(dbconfig) as cursor:
        tgl = date.today()

        id = tgl.strftime('%Y-%m-%d') + "-" + nis

        _SQL = """SELECT * FRom tb_absensi where nis=%s and Date(tgl_absen)=%s"""
        cursor.execute(_SQL, (nis,tgl,))
        contents = cursor.fetchone()
        print(contents)

        if contents == None:
            _SQL = """INSERT INTO tb_absensi(id_absensi,nis,terlambat,hadir) VALUES (%s,%s,%s,%s)"""
            cursor.execute(_SQL, (id,nis,jamtelat(),1,))

        # elif contents[0] == nis:
        #     _SQL = """DELETE FRom tb_cknf"""
        #     cursor.execute(_SQL)
        #     _SQL = """INSERT INTO tb_cknf(nis) VALUES (%s)"""
        #     cursor.execute(_SQL, (nis,))


def InsertTap(nis):
    with UseDatabase(dbconfig) as cursor:

        # _SQL="""SELECT * FRom tb_cknf where nis=%s"""
        _SQL = """SELECT COUNT(*) AS tot FRom tb_cknf"""
        cursor.execute(_SQL)
        contents = cursor.fetchone()
        print (contents[0])
        if  contents[0]==0:
            _SQL = """INSERT INTO tb_cknf(nis) VALUES (%s)"""
            cursor.execute(_SQL, (nis,))

        elif contents[0]==1:
            print ("tess")
            _SQL = """DELETE FRom tb_cknf"""
            cursor.execute(_SQL)
            _SQL = """INSERT INTO tb_cknf(nis) VALUES (%s)"""
            cursor.execute(_SQL, (nis,))

def jamtelat():
    with UseDatabase(dbconfig) as cursor:
        tgl=date.today()
        # '%m/%d/%Y'
        b=tgl.strftime('%Y-%m-%d')+" 08:00:00"
        t=datetime.today()
        _SQL="""SELECT TIMEDIFF(%s, %s)AS telat"""
        cursor.execute(_SQL,(t,b,))
        contents = cursor.fetchone()
        return contents[0]



# print('We start off in:', __name__)

if __name__ == '__main__':
    # pass
    # InsertPresensi('1234567890123456')
    InsertTap('1234567890123456')
