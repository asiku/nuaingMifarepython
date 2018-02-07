from smartcard.System import readers
from smartcard.util import toASCIIString,toASCIIBytes
from Mifare1kMap import Mifare1k



def bacakartu():
    otentikasi = [0xFF, 0x88, 0x00, Mifare1k[0], 0x60, 0x00]
    bacadata = [0xFF, 0xB0, 0x00, Mifare1k[0], 0x10]

    r = readers()
    print "Available readers:", r

    reader = r[0]
    # print "Using:", reader

    connection = reader.createConnection()
    connection.connect()

    data, sw1, sw2 = connection.transmit(otentikasi)
    print data
    print "Select Applet: %02X %02X" % (sw1, sw2)

    data, sw1, sw2 = connection.transmit(bacadata)
    print toASCIIString(data)
    print "Select Applet: %02X %02X" % (sw1, sw2)


def tuliskartu(nis):
    otentikasi = [0xFF, 0x88, 0x00, Mifare1k[0], 0x60, 0x00]

    r = readers()
    print "Available readers:", r

    reader = r[0]
    # print "Using:", reader

    connection = reader.createConnection()
    connection.connect()

    data, sw1, sw2 = connection.transmit(otentikasi)
    print data
    print "Select Applet: %02X %02X" % (sw1, sw2)

    # write
    cmd = [0xFF, 0xD6, 0x00, Mifare1k[0], 0x10]

    # nis = "123456789" + "1234567"
    for s in range(16):
        cmd.append(toASCIIBytes(nis[s])[0])

    data, sw1, sw2 = connection.transmit(cmd)
    print toASCIIString(data)
    print "Select Applet: %02X %02X" % (sw1, sw2)




