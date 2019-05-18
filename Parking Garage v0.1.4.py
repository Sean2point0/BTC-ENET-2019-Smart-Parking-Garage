from bluepy.btle import Scanner, DefaultDelegate, Peripheral
import threading
import time

class NotificationDelegate(DefaultDelegate):

    def __init__(self, number, car):
        DefaultDelegate.__init__(self)
        self.number = number
        self.car = car


    def handleNotification(self, cHandle, data):
        try:
            msg = data.decode("utf-8")
            print("Notification recieved:")
            print("From: {}".format(self.car.name))
            print("MAC: {}".format(self.car.MAC))
            print("Msg: {}".format(msg))
            if msg == "d":
                self.car.done = True
        except UnicodeDecodeError:
            print("Notification message not valid utf-8 format")
            

class ConnectionHandlerThread(threading.Thread):

    def __init__(self, connections, connection_index, car):
        threading.Thread.__init__(self)
        self.connections = connections
        self.connection_index = connection_index
        self.car = car

    def run(self):
        connection = self.connections[self.connection_index]
        connection.setDelegate(NotificationDelegate(self.connection_index, self.car))
        connection.writeCharacteristic(18, bytes((input("message to send: ")+"\n").encode("utf-8")))
        while not self.car.disconnect:
            while not self.car.done:
                if connection.waitForNotifications(1):
                    if not self.car.done:
                        connection.writeCharacteristic(18, bytes((input("message to send: ")+"\n").encode("utf-8")))
            time.sleep(2)
            connection.waitForNotifications(0.1)
            

class GarageCarFunctions:
    
    def __init__(self):
        self.options = {"1": self.newCar,
                        "2": self.existingCar,
                        "3": self.userDone}
        self.displayOptions = ["connect to a new car",
                              "connect to an existing car",
                              "stop program"]
        self.parkedCars = {}
        self.connections = []
        self.connection_threads = []
        self.pickOption()

        
    def pickOption(self): 
        while True:
            print("what would you like to do?\n")
            for count, option in enumerate(self.displayOptions, 1):
                print(" ({}) {}".format(count, option))
            userChoice = input()
            if userChoice in self.options.keys():
                break
            print("that is not a valid choice. Please choose again\n")
        self.options[userChoice]()


    def newCar(self):
        chosenCar = None
        print("Scanning...\n")
        scanner = Scanner()
        scan = scanner.scan(2)
        namedDevices = [x for x in scan if x.getValueText(9) != None]
        while True:
            if not namedDevices:
                print("There are no cars in the area to connect to\n")
                break
            dictDevices = {}
            for count, device in enumerate(namedDevices, 1):
                dictDevices[count] = device
                print("({}) name:     {}".format(count, device.getValueText(9)))
                print("    MAC ID:   {}".format(device.addr))
                print("    RSSI:    {} dB\n".format(device.rssi))
            userChoice = input("Which car would you like to connect to?\n")
            if not userChoice:
                break
            if int(userChoice) in dictDevices.keys():
                chosenCar = dictDevices[int(userChoice)]
                break
            print("that is not a valid option. Please choose again\n")
        if chosenCar:    
            self.carConnect(chosenCar)
        else:
            self.pickOption()

    
    def carConnect(self, scanEntry):
        print("Connecting to Car...\n")
        if not scanEntry.addr in self.parkedCars.keys():
            car = self.parkedCars[scanEntry.addr] = CarInfo(scanEntry)
            p = Peripheral(scanEntry)
            self.connections.append(p)
            t = ConnectionHandlerThread(self.connections, len(self.connections)-1, car)
            t.start()
            self.connection_threads.append(t)
        else:
            car = self.parkedCars[scanEntry.addr]
            car.done = False
        print("connected\n")
        while not car.done:
            pass
        print("finished for now\n")
        self.pickOption()

    
    def existingCar(self):
        userChoice = None
        while True:
            choices = {}
            if not self.parkedCars.values():
                print("There are no cars currently parked")
                break
            for count, car in enumerate(self.parkedCars.values(), 1):
                print("({}) name:   {}".format(count, car.name))
                print("    MAC: {}\n".format(car.MAC))
                choices[count] = car
            userChoice = input("which car would you like to connect to?\n")
            if not userChoice or int(userChoice) in choices.keys():
                break
            print("That is not a valid option. please choose again")
        if not userChoice:
            self.pickOption()
        else:
            chosenCar = choices[int(userChoice)].MAC
            self.carConnect(self.parkedCars[chosenCar].scanEntry)
        
    def userDone(self):
        for cars in self.parkedCars.values():
            cars.disconnect = True
        for cars in self.connection_threads:
            cars.join()
        for cars in self.connections:
            cars.disconnect()
        print("done")


class CarInfo:

    def __init__(self, scanEntry):
        self.scanEntry = scanEntry
        self.__name = self.scanEntry.getValueText(9)
        self.__MAC = self.scanEntry.addr
        self.done = False
        self.disconnect = False

    @property
    def name(self):
        return self.__name

    @property
    def MAC(self):
        return self.__MAC

        
def main():
    print("Welcome to Peter's Parking Party Palace!")
    PPPP = GarageCarFunctions()

if __name__ == "__main__":
    main()
