class Siswa:
    table="tb_biodata_siswa"
    nis="nis"
    nama="nama"
    jk="jenis_kelamin"
    tempat="tempat_lahir"
    ala="alamat"
    nohpsiswa="no_hp_siswa"
    nohportu="no_hp_orang_tua_siswa"
    idkelas="id_tk"
    thnmasuk="th_masuk"
    tgllahir="tgl_lahir"
    nisn="nisn"
    stat="status"
    gbr="pth"

    def __init__(self):
        self.table = "tb_biodata_siswa"
        self.nis = "nis"
        self.nama = "nama"
        self.jk = "jenis_kelamin"
        self.tempat = "tempat_lahir"
        self.ala = "alamat"
        self.nohpsiswa = "no_hp_siswa"
        self.nohportu = "no_hp_orang_tua_siswa"
        self.idkelas = "id_tk"
        self.thnmasuk = "th_masuk"
        self.tgllahir = "tgl_lahir"
        self.nisn = "nisn"
        self.stat = "status"
        self.gbr = "pth"

    def insertsiswa(self,tb):
        _SQL="INSERT INTO " + tb
        return _SQL



# s=Siswa()
# f=(s.nis,s.nama)
# isi=("559","adem")
# _SQL=s.insertsiswa(s.table,f)+"VALUES"+str(isi)
#
# print(_SQL)



