import sys
import time
import threading
from bluepy.btle import *

class printDots(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        for x in range(3):
            time.sleep(0.5)
            sys.stdout.write('.')
            sys.stdout.flush()
        sys.stdout.write('\n')


class NotificationDelegate(DefaultDelegate):

    """ Subclass of the DefaultDelegate class. Whenever a connected BLE
        peripheral device sends a message it is received as a "notification".

        handleNotification() method is called whenever a notification is
        received, which in this case decodes the message and displays the
        text. The message "d" signals the BLE device is done with its routine.
    """

    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
        try:
            msg = data.decode("utf-8")
            if msg == "d":
                BLE.done = True
        except UnicodeDecodeError:
            print("Notification message not valid utf-8 format")


class BLE:

    """ Class to handle connecting or reconnecting to BLE devices via bluepy.
        While multiple connections via BLE 4.0 is possible the implementation
        was unobtainable within the timeframe of this project without more
        knowledgeable contributor's giudance pointing which way to go with this
        project. A single threaded application is all that is needed however a
        multithreaded end product would have been more satisfying.

        BLE.done is a class boolean that dictates whether the BLE peripheral
        device has notified it has completed its task set by sendMessage()

        newConnect(): handles whichever BLE devices are advertising during
        scanning and filters out BLE devices that are already added to the
        network using the currentCars parameter.

        Connect(): the connect() method tries to connect whether a scanEnry
        class or a MAC address is passed as a parameter. in either case the
        Raspberry Pi tries to connect to the device.

        sendMessage(): once connections ae established communication is reliant
        on the central device receiving update info from the peripheral. When
        the peripheral is finished the necessary code is sent to the central
        device.

        Disconnect(): This method severs the BLE connection to allow for easy
        decoupling between modules until further communication is needed.
    """

    done = False

    def __init__(self, defaultAddr=None, defaultName=None):
        self.chosenCar = None
        self.addr = defaultAddr
        self.name = defaultName
        self.peripheral = None

    def newConnect(self, currentCars):
        sys.stdout.write('Scanning')
        p = printDots()
        p.start()
        scanner = Scanner()
        scan = scanner.scan(2)
        namedDevices = [x for x in scan if x.getValueText(9) is not None
                                        and x.addr not in currentCars]
        while True:
            if not namedDevices:
                print("There are no cars in the area to connect to")
                break
            dictDevices = {}
            for count, device in enumerate(namedDevices, 1):
                dictDevices[count] = device
                devName = device.getValueText(9)
                print("({}) name:     {}".format(count, devName))
                print("{: >8}:   {}".format("MAC", device.addr))
                print("{: >8}:     {} dB\n".format("RSSI", device.rssi))
            userChoice = input("Which car would you like to connect to?")
            if not userChoice:
                break
            if int(userChoice) in dictDevices.keys():
                self.chosenCar = dictDevices[int(userChoice)]
                break
            print("that is not a valid option. Please choose again")
        if self.chosenCar:
            self.Connect(scanEntry=self.chosenCar)
        else:
            print("didn't connect")

    def Connect(self, scanEntry=None, MAC=None):
        sys.stdout.write('Connecting to device')
        p = printDots()
        p.start()
        time.sleep(2)
        if scanEntry:
            self.peripheral = Peripheral(scanEntry)
            self.name = scanEntry.getValueText(9)
            self.addr = scanEntry.addr
        else:
            self.peripheral = Peripheral(MAC)
            self.addr = MAC
        self.peripheral.withDelegate(NotificationDelegate())

    def sendMessage(self, msg):
        BLE.done = False
        msg = msg.encode("utf-8")
        self.peripheral.writeCharacteristic(18, bytes(msg))
        while not BLE.done:
            self.peripheral.waitForNotifications(1)
        print("task complete")

    def Disconnect(self):
        self.peripheral.disconnect()
        print("disconnected from vehicle")

