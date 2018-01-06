from smartcard.System import readers
from smartcard.util import toASCIIString

from flask import Flask
app = Flask(__name__)

otentikasi=[0xFF,0x88,0x00,0x08,0x60,0x00]
bacadata=[0xFF, 0xB0, 0x00, 0x08, 0x10]

@app.route('/')
def hello():
    r = readers()
    # print "Available readers:", r

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
    return toASCIIString(data)

app.run()