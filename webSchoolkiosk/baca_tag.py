from __future__ import print_function
from time import sleep

from smartcard.CardConnectionObserver import ConsoleCardConnectionObserver
from smartcard.CardMonitoring import CardMonitor, CardObserver
from smartcard.util import toHexString
from Mifare1kMap import Mifare1k
from smartcard.util import toASCIIString
# from TestDunder import InsertPresensi,InsertTap,UpdateTap

# a simple card observer that prints inserted/removed cards
class PrintObserver(CardObserver):
    """A simple card observer that is notified
    when cards are inserted/removed from the system and
    prints the list of cards
    """

    def __init__(self):
        self.observer = ConsoleCardConnectionObserver()



    def update(self, observable, actions):
        (addedcards, removedcards) = actions
        for card in addedcards:
            self.flagk = "Tap"
            print("+Inserted: ", toHexString(card.atr))
            card.connection = card.createConnection()
            card.connection.connect()
            card.connection.addObserver(self.observer)
            cmdott = [0xFF, 0x88, 0x00, Mifare1k[0], 0x60, 0x00]
            cmdbaca = [0xFF, 0xB0, 0x00, Mifare1k[0], 0x10]
            response, sw1, sw2 = card.connection.transmit(cmdott)
            print("Select Ott: %02X %02X" % (sw1, sw2))
            if hex(sw1) == hex(144):
                # apdu = GET_RESPONSE + [sw2]
                data, sw1, sw2 = card.connection.transmit(cmdbaca)
                print("Select Baca: %02X %02X" % (sw1, sw2))
                if hex(sw1) == hex(144):
                    # InsertPresensi(toASCIIString(data))
                    # InsertTap(toASCIIString(data))
                    # UpdateTap("tap")
                    print (toASCIIString(data))

        for card in removedcards:
            # UpdateTap("remove")
            self.flagk = "Tap"
            print("-Removed: ", toHexString(card.atr))

# if __name__ == '__main__':
def baca_kartu():
    print("Insert or remove a smartcard in the system.")
    # print("This program will exit in 10 seconds")
    print("")
    cardmonitor = CardMonitor()
    cardobserver = PrintObserver()
    cardmonitor.addObserver(cardobserver)

    # while True:
    sleep(1)

    # don't forget to remove observer, or the
    # monitor will poll forever...
    cardmonitor.deleteObserver(cardobserver)

    import sys
    if 'win32' == sys.platform:
        print('press Enter to continue')
        sys.stdin.read(6000)