from smartcard.System import readers
from Mifare1kMap import Mifare1k
from smartcard.util import toASCIIString
import smartcard.Exceptions
import binascii

r=readers()
print "Available readers:", r

reader = r[0]
# print "Using:", reader

connection = reader.createConnection()
connection.connect()


def BacadataMifare1k(blok):
    cmd=[0xFF, 0xB0, 0x00, blok, 0x10]
    data, sw1, sw2 = connection.transmit(cmd)
    print "Select Applet: %02X %02X" % (sw1, sw2)
    print data
    return data


def sendApdu(cmd):
  try:

    data, sw1, sw2 = connection.transmit(cmd)
    print "Select Applet: %02X %02X" % (sw1, sw2)
    if hex(sw1) ==hex(144):
        print "otentikasi sukses"
    else:
        print "Gagal"
  except Exception , msg:
      print "" + msg
  return data


def otentikasi_mifare1k(blok):

    cmd=[0xFF, 0x88, 0x00, Mifare1k[3], 0x60, 0x00]
    sendApdu(cmd)

def ResultMifar1k():
    # b=""
    otentikasi_mifare1k(Mifare1k[0])
    BacadataMifare1k(Mifare1k[0])
    # for i in Mifare1k:
    #     otentikasi_mifare1k(i)
    #     b = b + BacadataMifare1k(i)
    #     print (i)
    # return b

print ResultMifar1k()

# otentikasi_mifare1k(Mifare1k[0])

# public void otentkasi_mifare1k(byte blok){
#     String otk = send(new byte[]{(byte) 0xFF,
#             (byte) 0x88, (byte) 0x00, blok, (byte) 0x60, (byte) 0x00}, cardChannel);
#         if (otk.equals("9000")) {
#             System.out.println("sukses Authentikasi");
#             lbl_stat_otentik.setText("Berhasil Di Otentikasi");
#         } else {
#             System.out.println("gagal Authentikasi");
#             lbl_stat_otentik.setText("Gagal Otentikasi Device Tidak Bisa Baca dan Write Code:" + otk);
#         }
#     }