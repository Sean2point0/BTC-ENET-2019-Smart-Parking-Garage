import csv
import random
import serial
import sys
import getpass
from collections import OrderedDict
from bluepy.btle import Scanner, DefaultDelegate, Peripheral
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

allParkingSpots = OrderedDict()
userDict = OrderedDict()
SMSCarriers = OrderedDict()

class NotificationDelegate(DefaultDelegate):

    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
        try:
            msg = data.decode("utf-8")
            print("Notification recieved:")
            print("Msg: {}".format(msg))
            if msg == "d":
                BLE.done = True
        except UnicodeDecodeError:
            print("Notification message not valid utf-8 format")

class BLE:

    done = False

    def __init__(self, defaultAddr = None, defaultName = None):
        self.chosenCar = None
        self.addr = defaultAddr
        self.name = defaultName
        self.peripheral = None

    def newConnect(self):
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
                print("{: >8}:   {}".format("MAC", device.addr))
                print("{: >8}:     {} dB\n".format("RSSI", device.rssi))
            userChoice = input("Which car would you like to connect to?\n")
            if not userChoice:
                break
            if int(userChoice) in dictDevices.keys():
                self.chosenCar = dictDevices[int(userChoice)]
                break
            print("that is not a valid option. Please choose again\n")
        if self.chosenCar:
            self.Connect(scanEntry = self.chosenCar)
        else:
            print("didn't connect\n")

    def Connect(self, scanEntry = None, MAC = None):
        print("Connecting to Car...\n")
        if scanEntry:
            self.peripheral = Peripheral(scanEntry)
            self.name, self.addr = scanEntry.getValueText(9), scanEntry.addr
        else:
            self.peripheral = Peripheral(MAC)
            BLE.done = False
        self.peripheral.withDelegate(NotificationDelegate())
        print("connected\n")

    def sendMessage(self):
        msg = (input("message to send: ")+"\n").encode("utf-8")
        self.peripheral.writeCharacteristic(18, bytes(msg))
        while not BLE.done:
            self.peripheral.waitForNotifications(1)
        print("task complete\n")


    def Disconnect(self):
        self.peripheral.disconnect()
        print("disconnected\n")
    

class parkingSpot:

    allowedAttributes = []

    def __init__(self, dictAttributes):
        for key, value in dictAttributes.items():
            if key is not None and value is not None:
                setattr(self, key, value)

    def dictforcsv(self):
        dictSpot = {}
        for attr in parkingSpot.allowedAttributes:
            dictSpot[attr] = getattr(self, attr, "0")
        return dictSpot
    
    def __str__(self):
        string = ""
        for key in parkingSpot.allowedAttributes:
            if key in self.__dict__:
                string += "\n{: <12}: {}".format(key, getattr(self, key, "0"))
        return string


def arduinoCom():

    """function for RPi to communicate serially with Arduino"""

    ser = serial.Serial('/dev/ttyACM0')
    while 1:
        n = input('Enter a number of times for the led to flash: ')
        ser.write(n)


def checkIn():

    """function for selecting parking location and receiving
       location password"""
    print("\nCheck-in selected")
    car = BLE(defaultAddr = "0", defaultName = "0")
    car.newConnect()
    if car.addr != "0":
        carAttr = ["0", car.name, car.addr, datetime.datetime.now(), "0"]
        dictCar = dict(zip(parkingSpot.allowedAttributes, carAttr))
        newCar = parkingSpot(dictCar)
        while True:
            print("vacant locations: ")
            for key, value in allParkingSpots.items():
                if value.MAC == '0':
                    print(key)
            selectSpot = input("Please select a location: ")
            if selectSpot in allParkingSpots.keys() and int(allParkingSpots[selectSpot].MAC) == 0:
                print("\nYou have selected location number {}.".format(selectSpot))
                car.sendMessage()
                print("Generating parking pass...")
                newCar.Spot = selectSpot
                newCar.Confirmation = str(random.randint(10000000, 99999999))
                print("Your confirmation number is {}.".format(newCar.Confirmation))
                allParkingSpots[selectSpot] = newCar
                saveLoc()
                if queryYesNo("Would you like an email or text confirmation? "):
                    sendConfirmation(newCar.Confirmation)
                break
            print("\nInvalid. Parking location is occupied or non-existant.")
        car.Disconnect()

def checkOut():

    """function to prompt for location password to retrieve vehicle
       and vacate location"""

    print("\nCheck-out selected.")
    selectCar = input("Please enter confirmation number to retrieve vehicle: ")
    for key, value in allParkingSpots.items():
        if selectCar == value.Confirmation:
            currentCar = allParkingSpots[key]
            print("\nRetrieving vehicle from location {}.".format(key))
            car = BLE(defaultAddr = "0", defaultName = "0")
            car.Connect(MAC = currentCar.MAC)
            car.sendMessage()
            blankSpot = [key, "0", "0", "0", "0", "0"]
            dictBlankSpot = dict(zip(parkingSpot.allowedAttributes, blankSpot))
            allParkingSpots[key] = parkingSpot(dictBlankSpot)
            print("Location {} is now vacant.".format(key))
            car.Disconnect()
            saveLoc()
            break
    else:
        print("Parking pass is invalid.")

def currentCars():
    print("\nCurrent Customer Vehicles:")
    for spot, carInfo in allParkingSpots.items():
        print(str(carInfo))


def saveLoc():
    fileLoc = '/home/pi/Documents/ENET_Capstone/parking_database.csv'
    with open(fileLoc, newline='', mode='w') as outfile:
        fn = parkingSpot.allowedAttributes
        writer = csv.DictWriter(outfile, fieldnames = fn)
        writer.writeheader()
        for Spot in allParkingSpots.values():
            writer.writerow(Spot.dictforcsv())


def sendConfirmation(ConfirmationNum):

    """Sends the ConfirmationNum to the user-provided
       mobile number or email via STMP"""

    garageEmail = "petersparkingpalace@gmail.com"

    if not SMSCarriers:
        carrierInfo = [["AT&T", "txt.att.net"],
                       ["Sprint", "messaging.sprintpcs.com"],
                       ["T-Mobile", "tmomail.net"],
                       ["Verizon", "vtext.com"],
                       ["Other", ""]]
        for count, carrier in enumerate(carrierInfo, 1):
            SMSCarriers[str(count)] = carrier

    if queryYesNo("Will this email be sent to a mobile device?"):
        mobile = True
        while True:
            phoneNum = input("Enter phone number: ")
            if len(phoneNum) == 10:
                if queryYesNo("You entered {}.\n".format(phoneNum) +
                              "Is this correct?"):
                    break
            else:
                print("That is not a valid number." +
                      "Please provide a 10 digit number")

        while True:
            for count, carrier in enumerate(SMSCarriers.values(), 1):
                print("({}) {}".format(count, carrier[0]))
            phoneCarrier = input("Choose a carrier: ")
            if phoneCarrier in SMSCarriers.keys():
                if SMSCarriers[phoneCarrier][0] == "T-Mobile":
                    phoneNum = "1" + phoneNum
                break
            print("That is not a valid choice")

        if phoneCarrier != "5":
            emailDomain = SMSCarriers[phoneCarrier][1]
            customerEmail = "{}@{}".format(phoneNum, emailDomain)
        else:
            customerEmail = ""
    else:
        mobile = False
        while True:
            customerEmail = input("Enter email address: ")
            if queryYesNo("You entered {}.\n".format(customerEmail) +
                          "Is this correct?"):
                break

    if len(customerEmail) > 0:
        if queryYesNo("Ready to send. Confirm?"):
            msg = MIMEMultipart()
            msg["From"] = garageEmail
            msg["To"] = customerEmail
            if mobile:
                # whitespace after confirmationNum as SMS cuts off last 2 chars
                body = "Thank you for choosing Peter's Parking Palace.\n" +\
                       "Confirmation number: {}  ".format(ConfirmationNum)
            else:
                msg["Subject"] = "Peter's Parking Palace Confirmation"
                body = "Thank you for choosing Peter's Parking Palace.\n" +\
                       "Confirmation Number: {}".format(ConfirmationNum)
            msg.attach(MIMEText(body, "plain"))
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo
            server.starttls()
            try:
                password = getpass.getpass("enter email password: ")
                server.login(garageEmail, password)
                server.sendmail(garageEmail, customerEmail, msg.as_string())
                server.quit()
                print("email sent\n")
            except Exception as e:
                print("Something went wrong")
                print(e)
        else:
            print("email not sent\n")
    else:
        print("We are unable to send a message to that address/carrier")


def resendConfirmation():
    currentCars = [car for car in allParkingSpots.values() if car.MAC != "0"]
    if currentCars:
        while True:
            for car in currentCars:
                print(str(car))
            chosenCar = input("choose a car to resend confirmation email to: ")
            if chosenCar in allParkingSpots.keys() and allParkingSpots[chosenCar].MAC != "0":
                break
            if not queryYesNo("That is not a valid option. continue? "):
                chosenCar = ""
                break
        if chosenCar:
            sendConfirmation(allParkingSpots[chosenCar].Confirmation)
    else:
        print("There are no cars currently parked")


def menu():

    """ Displays the menu options for the program"""

    options = ["check in",
               "check out",
               "create user",
               "delete user",
               "resend confirmation",
               "check current vehicles",
               "log out"]
    print("\n===================| MENU |====================")
    print("|                                             |")
    for count, option in enumerate(options, 1):
        print("|  Press [{}] to {: <30s}|".format(count, option))
    print("|                                             |")
    print("===============================================")


def queryYesNo(question):

    """Ask a yes/no question via input() and return their answer.
    "question" is a string that is presented to the user.
    The "answer" return value is True for "yes" or False for "no".
    """

    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}

    while True:
        sys.stdout.write(question + "[y/n]")
        choice = input().lower()
        if choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


def logOut():
    print("logging out...")


def startRoutine():

    """Handles all input choices from the parking attendant for parking
       garage functions and operations"""

    dictChoices = {"1": checkIn,
                   "2": checkOut,
                   "3": createUser,
                   "4": deleteUser,
                   "5": resendConfirmation,
                   "6": currentCars,
                   "7": logOut}
    numSpotsFull = [car for car in allParkingSpots.values() if car.MAC != "0"]
    if len(numSpotsFull) == len(allParkingSpots):
        print("\nNO VACANCY: Check-in currently unavailable.")
        vacancy = False
    else:
        vacancy = True

    menu()
    userChoice = input("\nPlease make a selection from the MENU: ")
    if userChoice in dictChoices.keys():
        if dictChoices[userChoice] == checkIn and not vacancy:
            print("\nAll parking spots are full")
        else:
            dictChoices[userChoice]()
    else:
        print("that is not a valid option")
    if dictChoices[userChoice] != logOut:
        if queryYesNo("\nContinue?"):
            startRoutine()
        else:
            logOut()


def createUser():

    """Adds an authorized user to the database"""

    username = None
    print("\n'Create user' selected.")
    username = input("Enter your new username: ")
    password = getpass.getpass("Enter your new password (input is hidden): ")
    userDict[username] = password
    print(userDict)
    if queryYesNo("\nCreate another user?"):
        createUser()
    else:
        saveUsers()


def deleteUser():

    """Deletes an authorized user from the database"""

    username = None
    print("\n'Delete user' selected.")
    username = input("Enter username to delete: ")
    userDict.pop(username, None)
    print(username + "'s account has been deleted.")
    saveUsers()


def saveUsers():

    """Updates csv file of valid users"""

    fileLoc = '/home/pi/Documents/ENET_Capstone/users.csv'
    writeUsers = csv.writer(open(fileLoc, newline='', mode='w'))
    for key, value in userDict.items():
        writeUsers.writerow([key, value])


def main():

    """Start of program. Initializes information from CSV files to dictionaries
       on first run."""

    loginAttempts = 3

    if not allParkingSpots:
        fileLoc = '/home/pi/Documents/ENET_Capstone/parking_database.csv'
        with open(fileLoc, newline='', mode='r') as infile:
            reader = csv.DictReader(infile)
            parkingSpot.allowedAttributes = reader.fieldnames
            for count, rows in enumerate(reader, 1):
                allParkingSpots[str(count)] = parkingSpot(rows)
    if not userDict:
        fileLoc = '/home/pi/Documents/ENET_Capstone/users.csv'
        with open(fileLoc, newline='', mode='r') as userInfile:
            userReader = csv.reader(userInfile)
            for rows in userReader:
                userDict[rows[0]] = rows[1]
    for a in  allParkingSpots.keys():
        spot = allParkingSpots[a]
        print(spot.Spot, spot.Confirmation)
    print(userDict)

    if userDict:
        while loginAttempts > 0:
            username = input("Username: ")
            password = getpass.getpass()
            if username in userDict.keys() and userDict[username] == password:
                startRoutine()
                break
            else:
                loginAttempts -= 1
                print("invalid username or password.\n" +
                      "{} tries remaining".format(loginAttempts))
        if loginAttempts > 0:
            if queryYesNo("Would you like to log in as a different user? "):
                main()
        else:
            print("You have exceeded the maximum number of login attempts.")
    else:
        startRoutine()
    print("exiting program...")


if __name__ == "__main__":
    print("Welcome to Peter's Parking Party Palace")
    main()
