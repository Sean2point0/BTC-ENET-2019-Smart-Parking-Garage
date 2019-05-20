import csv
import random
import serial
import sys
import getpass
from collections import OrderedDict
from bluepy.btle import Scanner, DefaultDelegate, Peripheral
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

locDict = OrderedDict()
userDict = OrderedDict()
SMSCarriers = OrderedDict()


def arduinoCom():

    """function for RPi to communicate serially with Arduino"""

    ser = serial.Serial('/dev/ttyACM0')
    while 1:
        n = input('Enter a number of times for the led to flash: ')
        ser.write(n)

def checkIn():

    """function for selecting parking location and receiving location password"""

    print("\nCheck-in selected")
    while True:
        print("vacant locations: ")
        for key, value in locDict.items():
            if value == '0':
                print(key)
        select = input("Please select a location: ")
        
        if select in locDict.keys() and int(locDict.get(select)) == 0:
            print("\nYou have selected location number {}.".format(select))
            print("Generating parking pass...")
            locDict[select] = str(random.randint(10000000, 99999999))
            print("Your parking pass confirmation number is {}.".format(locDict[select]))
            if queryYesNo("Would you like us to email/text you your confirmation number?"):
                sendConfirmation(locDict[select])
            saveLoc()
            break
        
        print("\nInvalid. Parking location is occupied or non-existant.")


def checkOut():

    """function to prompt for location password to retrieve vehicle / vacate location"""
    
    print("\nCheck-out selected.")
    selectO = input("Please enter parking pass confirmation number to retrieve vehicle: ")
    for key, value in locDict.items():
        if selectO == value:          
            print("\nRetrieving vehicle from location {}.".format(key))
            print("Location {} is now vacant.".format(key))
            locDict[key] = '0'
            saveLoc()
            break
    else:
        print("Parking pass is invalid.")

def saveLoc():
    with open('/home/pi/Documents/ENET_Capstone/parking_database.csv', mode='w') as outfile:
        writer = csv.writer(outfile)
        for key, value in locDict.items():
           writer.writerow([key, value])

def sendConfirmation(ConfirmationNum):

    """Sends the ConfirmationNum to the user-provided mobile number or email via STMP

       NOTE - if sending to a mobile phone the parking garage email must be whitelisted
       by the text recipient prior to sending or else the email will be blocked."""
    
    garageEmail = "petersparkingpalace@gmail.com"
    
    if not SMSCarriers:
        carrierInfo =[["AT&T", "txt.att.net"],
                      ["Sprint", "messaging.sprintpcs.com"],
                      ["T-Mobile", "tmomail.net"],
                      ["Verizon", "vtext.com"],
                      ["Other", ""]]
        for count, carrier in enumerate(carrierInfo, 1):
            SMSCarriers[str(count)] = carrier
            
    if queryYesNo("Will this email be sent to a mobile device?"):
        while True:
            phoneNum = input("Enter phone number: ")
            if len(phoneNum) == 10:
                if queryYesNo("You entered {}. Is this correct?".format(phoneNum)):
                    break
            else:
                print("That is not a valid number. Please provide a 10 digit number")
                
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
        while True:
            customerEmail = input("Enter email address: ")
            if queryYesNo("You entered {}. Is this correct?".format(customerEmail)):
                break
            
    if len(customerEmail) > 0:
        if queryYesNo("Ready to send. Confirm?"):
            msg = MIMEMultipart()
            msg["From"] = garageEmail
            msg["To"] = customerEmail
            msg["Subject"] = "Peter's Parking Palace Confirmation"
            body = "Thank you for choosing Peter's Parking Palace." +\
                  "Your confirmation Number is: {}".format(ConfirmationNum)
            msg.attach(MIMEText(body, "plain"))
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo
            server.starttls()
            try:
                password = getpass.getpass("enter parking garage email password: ")
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
    currentCars = [key for key in locDict.keys() if locDict[key] != "0"]
    if currentCars:
        while True:
            for count, car in enumerate(currentCars, 1):
                print("({}) parking space {}".format(count, car))
            chosenCar = input("choose a car to resend confirmation email to: ")
            if chosenCar in locDict.keys() and locDict[chosenCar] != "0":
                break
            if not queryYesNo("That is not a valid option. continue? "):
                chosenCar = ""
                break
        if chosenCar:
            sendConfirmation(locDict[chosenCar])
    else:
        print("There are no cars currently parked")

def menu():

    """ Displays the menu options for the program"""
    
    options = ["check in",
               "check out",
               "create user",
               "delete user",
               "resend confirmation",
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
                   "6": logOut}
    
    if len([val for val in locDict.values() if val != "0"]) == len(locDict):
        print("\nNO VACANCY: Check-in currently unavailable.")
        print(locDict.values())
        vacancy = False
    else:
        vacancy = True
        
    menu()
    userChoice = input("\nPlease make a selection from the MENU: ")
    if userChoice in dictChoices.keys():
        if dictChoices[userChoice] == checkIn and not vacancy:
            print("\nNo vacancy. Unable to check in new customers at this time.")
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
    
    writeUsers = csv.writer(open('/home/pi/Documents/ENET_Capstone/users.csv', 'w'))
    for key, value in userDict.items():
        writeUsers.writerow([key, value])

def main():

    """Start of program. Initializes information from CSV files to dictionaries
       on first run."""
    loginAttempts = 3
    
    if not locDict:
        with open('/home/pi/Documents/ENET_Capstone/parking_database.csv', mode='r') as infile:
            reader = csv.reader(infile)
            for rows in reader:
               locDict[rows[0]] = rows[1]
    if not userDict:
        with open('/home/pi/Documents/ENET_Capstone/users.csv', mode='r') as userInfile:
            userReader = csv.reader(userInfile)
            for rows in userReader:
                userDict[rows[0]] = rows[1]
            
    print(locDict)
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
                print("invalid username or password. {} tries remaining".format(loginAttempts))
        if loginAttempts > 0:
            if queryYesNo("Would you like to log in as a different user? "):
                main()
        else:
            print("You have exceeded the maximum number of login attempts.")
    else:
        startRoutine()
    print("exiting program...")

if __name__ == "__main__":
    main()
