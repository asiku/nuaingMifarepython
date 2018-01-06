from __future__ import print_function
from time import sleep

from smartcard.CardConnectionObserver import ConsoleCardConnectionObserver
from smartcard.CardMonitoring import CardMonitor, CardObserver
from smartcard.util import toHexString
from Mifare1kMap import Mifare1k
from smartcard.util import toASCIIString


# a simple card observer that prints inserted/removed cards
class PrintObserver(CardObserver):
    """A simple card observer that is notified
    when cards are inserted/removed from the system and
    prints the list of cards
    """

    def __init__(self):
        self.observer = ConsoleCardConnectionObserver()
        self.getbaca=""
        self.getTap=""




    def update(self, observable, actions):
        (addedcards, removedcards) = actions
        for card in addedcards:
            # print("+Inserted: ", toHexString(card.atr))

            card.connection = card.createConnection()
            card.connection.connect()
            card.connection.addObserver(self.observer)
            cmdott = [0xFF, 0x88, 0x00, Mifare1k[0], 0x60, 0x00]
            cmdbaca = [0xFF, 0xB0, 0x00, Mifare1k[0], 0x10]
            response, sw1, sw2 = card.connection.transmit(cmdott)
            # print("Select Ott: %02X %02X" % (sw1, sw2))
            if hex(sw1) == hex(144):
                # apdu = GET_RESPONSE + [sw2]
                data, sw1, sw2 = card.connection.transmit(cmdbaca)
                # print("Select Baca: %02X %02X" % (sw1, sw2))
                if hex(sw1) == hex(144):
                    self.getbaca=toASCIIString(data)
                    self.getTap = "TP"
                    # print(self.getbaca)
                    # print (toASCIIString(data))

        for card in removedcards:
            self.getTap = ""
            print("-Removed: ", toHexString(card.atr))

#

def ResultMifar1k():


    cardmonitor = CardMonitor()
    cardobserver = PrintObserver()

    cardmonitor.addObserver(cardobserver)
    sleep(1)
    # if cardobserver.getbaca!="":
    # print("Tes baca", cardobserver.getbaca)
    # cardobserver.getbaca = ""

        # while True:
        #     sleep(1)

        # don't forget to remove observer, or the
        # monitor will poll forever...
    cardmonitor.deleteObserver(cardobserver)

    import sys
    if 'win32' == sys.platform:
        print('press Enter to continue')
        sys.stdin.read(6000)

    return  cardobserver.getbaca


if __name__ == '__main__':
    ResultMifar1k()