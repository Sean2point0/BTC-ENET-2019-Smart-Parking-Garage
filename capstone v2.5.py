import csv
from random import randint
import serial
import getpass
import smtplib
from math import ceil

from BLE import *
import LCDandKeypad
from parkingSpot import parkingSpot
from queryYesNo import queryYesNo

from collections import OrderedDict
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

allParkingSpots = OrderedDict()
userDict = OrderedDict()
SMSCarriers = OrderedDict()


def arduinoCom(spot):

    """function for RPi to communicate serially with Arduino"""

    ser = serial.Serial('/dev/ttyACM0', 9600)
    ser.write(bytes(spot.encode("utf-8")))

def checkIn():

    """ function for selecting parking location and receiving
        location password
    """

    print("\nCheck-in selected")
    try:
        car = BLE(defaultAddr="0", defaultName="0")
        parkedCars = allParkingSpots.values()
        currentCars = [car.MAC for car in parkedCars if car.MAC != "0"]
        car.newConnect(currentCars)
    except Exception as e:
        print("something went wrong: ", e)
    if car.addr != "0":
        print("connected\n")
        carAttr = ["0", car.name, car.addr, str(datetime.now()), "0"]
        dictCar = dict(zip(parkingSpot.allowedAttributes, carAttr))
        newCar = parkingSpot(dictCar)
        while True:
            print("vacant locations: ")
            for key, value in allParkingSpots.items():
                if value.MAC == '0':
                    print(key)
            selectSpot = input("Please select a location: ")
            currentSpot = allParkingSpots[selectSpot]
            if selectSpot in allParkingSpots.keys() and currentSpot.MAC == "0":
                print("You have selected location {}.".format(selectSpot))
                arduinoCom(selectSpot)
                car.sendMessage('g')
                print("Generating parking pass...")
                newCar.Spot = selectSpot
                rand = newCar.Confirmation = str(randint(10000000, 99999999))
                print("Your confirmation number is {}.".format(rand))
                LCDandKeypad.entranceWrite("Confirmation #:", str(rand))
                allParkingSpots[selectSpot] = newCar
                saveCustomerInfo()
                if queryYesNo("Would you like an email or text confirmation? "):
                    sendConfirmation(newCar.Confirmation)
                break
            print("\nInvalid. Parking location is occupied or non-existant.")
        car.Disconnect()
        del car


def checkOut():

    """ function to prompt for location password to retrieve vehicle
        and vacate location
    """

    leave = "abcdef"
    print("\nCheck-out selected.")
    parkedCars = allParkingSpots.values()
    currentCars = [car.MAC for car in parkedCars if car.MAC != "0"]
    if currentCars:
        print("please have customer enter in their confirmation number")
        selectCar = LCDandKeypad.exit()
        for key, value in allParkingSpots.items():
            if selectCar == value.Confirmation:
                LCDandKeypad.exitWrite("retrieving car")
                currentCar = allParkingSpots[key]
                car = BLE(defaultAddr="0", defaultName="0")
                try:
                    car.Connect(MAC=currentCar.MAC)
                except Exception as e:
                    print("something went wrong: ", e)
                    break
                if car.addr != "0":
                    print("connected\n")
                    totalPrice = getPrice(currentCar.StartTime)
                    print("Customer total is ${:.2f}".format(totalPrice))
                    LCDandKeypad.exitWrite("Amount owed:",
                                           "${:.2f}".format(totalPrice))
                    if not queryYesNo("Has the customer paid? "):
                        LCDandKeypad.exitWrite("NO $ NO CAR")
                        print("Customer must pay to retrieve vehicle")
                        break
                    try:
                        print("\nRetrieving vehicle from location {}.".format(key))
                        arduinoCom(leave[int(key)-1])
                        car.sendMessage('b')
                        arduinoCom('x')
                        car.sendMessage('g')
                    except Exception as e:
                        print("something went wrong:", e)
                    blankSpot = [key, "0", "0", "0", "0", "0"]
                    dictBlankSpot = dict(zip(parkingSpot.allowedAttributes, blankSpot))
                    allParkingSpots[key] = parkingSpot(dictBlankSpot)
                    print("Location {} is now vacant.".format(key))
                    car.Disconnect()
                    del car
                    saveCustomerInfo()
                    break
                else:
                    print("couldn't connect to device")
                    break
        else:
            print("Parking pass is invalid")
            LCDandKeypad.exitWrite("Parking pass",  "is invalid")
    else:
        print("There are currently no cars parked")

def currentCars():

    """ Prints the information for every parking spot
        in the garage
    """

    currentCars = [car for car in allParkingSpots.values() if car.MAC != '0']
    if currentCars:
        print("\nCurrent Customer Vehicles:")
        for car in currentCars:
            print(str(car))
    else:
        print("There are no cars currently parked")


def saveCustomerInfo():

    """ Updates csv file holding customer information whenever
        a customer finishes either checking in or checking out
    """

    fileLoc = '/home/pi/Documents/ENET_Capstone/parking_database.csv'
    with open(fileLoc, newline='', mode='w') as outfile:
        fn = parkingSpot.allowedAttributes
        writer = csv.DictWriter(outfile, fieldnames=fn)
        writer.writeheader()
        for Spot in allParkingSpots.values():
            writer.writerow(Spot.attributesToDict())


def sendConfirmation(ConfirmationNum):

    """ Sends the ConfirmationNum to the user-provided
        mobile number or email via STMP
    """

    garageEmail = "petersparkingpalace@gmail.com"

    if not SMSCarriers:
        carrierInfo = [["AT&T", "txt.att.net"],
                       ["Sprint", "messaging.sprintpcs.com"],
                       ["T-Mobile", "tmomail.net"],
                       ["Verizon", "vtext.com"],
                       ["Other", ""]]
        for count, carrier in enumerate(carrierInfo, 1):
            SMSCarriers[str(count)] = carrier

    if queryYesNo("Will this email be sent to a mobile device? "):
        mobile = True
        while True:
            phoneNum = input("Enter phone number: ")
            if len(phoneNum) == 10:
                if queryYesNo("You entered {}.\n".format(phoneNum) +
                              "Is this correct? "):
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
                          "Is this correct? "):
                break

    if len(customerEmail) > 0:
        if queryYesNo("Ready to send. Confirm? "):
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

    """ pulls up all the current cars parked in the garage and passes the chosen
        car's confirmation number to sendConfirmation()
    """

    currentCars = [car for car in allParkingSpots.values() if car.MAC != "0"]
    if currentCars:
        while True:
            for car in currentCars:
                print(str(car))
            chosenCar = input("choose a customer: ")
            if chosenCar in allParkingSpots.keys() and allParkingSpots[chosenCar].MAC != "0":
                break
            if not queryYesNo("That is not a valid option. continue? "):
                chosenCar = ""
                break
        if chosenCar:
            sendConfirmation(allParkingSpots[chosenCar].Confirmation)
    else:
        print("There are no cars currently parked")


def getPrice(timeStart):

    """Docstring goes here"""

    rates = [200, 35, 5]
    nextRates = [None] + rates
    del nextRates[-1]
    startTime = datetime.strptime(timeStart, "%Y-%m-%d %H:%M:%S.%f")
    currentTime = datetime.now()
    timeParked = currentTime - startTime
    times = [timeParked.days // 7,              # Weeks parked
             timeParked.days % 7,               # Days parked
             ceil(timeParked.seconds / 3600)]   # Hours parked
    totalPrice = 0
    print("Total time parked: ")
    print("{: <4} week(s)".format(times[0]))
    print("{: <4} day(s)".format(times[1]))
    print("{: <4} hour(s)".format(times[2]))
    for time, rate, nextRate in zip(times, rates, nextRates):
        price = time * rate
        totalPrice += price if (not nextRate or nextRate > price) else nextRate
    return totalPrice


def printMenu():

    """ Displays the menu options for the program"""

    options = ["check in customer",
               "check out customer",
               "check current vehicles",
               "resend confirmation",
               "create user",
               "delete user",
               "log out"]
    print("\n===================| MENU |====================")
    print("|                                             |")
    for count, option in enumerate(options, 1):
        print("|     Press [{}] to {: <27s}|".format(count, option))
    print("|                                             |")
    print("===============================================")


def logOut():

    """ this function is only to print 'logging out...' but is used to
        keep the methodology for the user choosing an option in mainMenu()
        consistent
    """

    print("logging out...")


def mainMenu():

    """ Handles all input choices from the parking attendant for parking
        garage functions and operations
    """

    dictChoices = {"1": checkIn,
                   "2": checkOut,
                   "3": currentCars,
                   "4": resendConfirmation,
                   "5": createUser,
                   "6": deleteUser,
                   "7": logOut}
    numSpotsFull = [car for car in allParkingSpots.values() if car.MAC != "0"]
    if len(numSpotsFull) == len(allParkingSpots):
        print("\nNO VACANCY: Check-in currently unavailable.")
        vacancy = False
    else:
        vacancy = True

    printMenu()
    userChoice = input("\nPlease make a selection from the MENU: ")
    if userChoice in dictChoices.keys():
        if dictChoices[userChoice] == checkIn and not vacancy:
            print("\nAll parking spots are full")
        else:
            dictChoices[userChoice]()
    else:
        print("that is not a valid option")
    if dictChoices[userChoice] != logOut:
        if queryYesNo("\nContinue? "):
            LCDandKeypad.entranceWrite(" Peters Parking", "  Party Palace")
            LCDandKeypad.exitWrite(" Peters Parking", "  Party Palace")
            mainMenu()
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

    if userDict:
        username = None
        print("\n'Delete user' selected.")
        username = input("Enter username to delete: ")
        userDict.pop(username, None)
        print(username + "'s account has been deleted.")
        saveUsers()
    else:
        print("There are no current users")

def saveUsers():

    """Updates csv file of valid users"""

    fileLoc = '/home/pi/Documents/ENET_Capstone/users.csv'
    writeUsers = csv.writer(open(fileLoc, newline='', mode='w'))
    for key, value in userDict.items():
        writeUsers.writerow([key, value])


def main():

    """ Start of program. Initializes information from CSV files to dictionaries
        on first run.
    """

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
    # REMOVE from final code
    if userDict:
        for key, value in userDict.items():
            print("{} : {}".format(key, value))

    loginAttempts = 3
    if userDict:
        while loginAttempts > 0:
            username = input("Username: ")
            password = getpass.getpass("Enter password (input is hidden): ")
            if username in userDict.keys() and userDict[username] == password:
                mainMenu()
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
        mainMenu()


if __name__ == "__main__":
    print("Welcome to Peter's Parking Party Palace")
    LCDandKeypad.entranceWrite(" Peters Parking", "  Party Palace")
    LCDandKeypad.exitWrite(" Peters Parking", "  Party Palace")
    main()
    LCDandKeypad.entranceWrite()
    LCDandKeypad.exitWrite()
    print("exiting program...")
