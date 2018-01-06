from smartcard.System import readers
from smartcard.util import toASCIIString
from Mifare1kMap import Mifare1k
import smartcard.Exceptions

def Baca(blok):
   try:
        r = readers()
        print "Available readers:", r

        reader = r[0]

        connection = reader.createConnection()
        connection.connect()

        cmdott = [0xFF, 0x88, 0x00, blok, 0x60, 0x00]
        cmd = [0xFF, 0xB0, 0x00, blok, 0x10]

        dataott, sw1, sw2 = connection.transmit(cmdott)
        # print "Select Applet: %02X %02X" % (sw1, sw2)
        if hex(sw1)==hex(144):
           print "Ott Sukses"
        else:
           print "Ott Gagal"

        data, sw1, sw2 = connection.transmit(cmd)
        if hex(sw1) == hex(144):
            print "Baca Sukses"
        else:
            print "Baca Gagal"


   except smartcard.Exceptions.CardConnectionException as inst:
    print "Kartu Tidak di Temukan, Mohon Untuk Men Tap Kartu Pada Reader! "
   except:
    print "Ada Error/NFC Reader Belum Terhubung!"

   return toASCIIString(data)


def ResultMifar1k():
    l=[Mifare1k[0]]
    b=""
    for i in l:
       b=b+ Baca(i)

    return b


# print ResultMifar1k()