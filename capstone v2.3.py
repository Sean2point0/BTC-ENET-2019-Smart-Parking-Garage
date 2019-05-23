import csv
import random
import numpy
import codecs
import serial
import sys
import getpass
from collections import OrderedDict

loc_dict = OrderedDict()
user_dict = OrderedDict()

#function for RPi to communicate serially with Arduino
def arduino_com():
    ser = serial.Serial('/dev/ttyACM0')
    while 1:
        n = input('Enter a number of times for the led to flash: ')
        ser.write(n)
        print(string)

#function for selecting parking location and receiving location password
def check_in():
    print("\nCheck-in selected")
    while True:
        print("vacant locations: ")
        for key, value in loc_dict.items():
            if value == '0':
                print(key)
        select = input("Please select a location: ")
        if select in loc_dict.keys() and int(loc_dict.get(select)) == 0:
            print("\nYou have selected location number {}.".format(select))
            print("Generating parking pass...")
            loc_dict[select] = random.randint(10000000, 99999999)
            print("The key value for location {} is now {}.".format(select, loc_dict[select]))
            save_loc()
            break
        print("\nInvalid. Parking location is occupied or non-existant.")

#function to prompt for location password to retrieve vehicle / vacate location
def check_out():
    print("\nCheck-out selected.")
    select_o = int(input("Please enter parking pass to retrieve vehicle: "))
    for key, value in loc_dict.items():
        if select_o == int(value):          
            print("\nRetrieving vehicle from location {}.".format(key))
            print("Location {} is now vacant.".format(key))
            loc_dict[key] = '0'
            save_loc()
            break
    else:
        print("Parking pass is invalid.")

def save_loc():
    with open('/home/pi/Documents/ENET_Capstone/parking_database.csv', mode='w') as outfile:
        writer = csv.writer(outfile)
        for key, value in loc_dict.items():
           writer.writerow([key, value])

def menu_vis():
    options = ["check in", "check out", "create user", "delete user", "exit program"]
    print("\n===================| MENU |====================")
    print("|                                             |")
    for count, option in enumerate(options, 1):
        print("|  Press [{}] to {: <30s}|".format(count, option))
    print("|                                             |")
    print("===============================================")
        
def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)
    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

def exit_program():
    print("exiting program...")

#Main routine, including options menu
def start_routine():
    dict_choices = {"1": check_in, "2": check_out, "3": create_user, "4": delete_user, "5": exit_program}
    if len([val for val in loc_dict.values() if val != "0"]) == len(loc_dict):
        print("\nNO VACANCY: Check-in currently unavailable.")
        print(loc_dict.values())
        vacancy = False
    else:
        vacancy = True
    menu_vis()
    in_out = input("\nPlease make a selection from the MENU: ")
    if in_out in dict_choices.keys():
        if in_out == "1" and not vacancy:
            print("\nNo vacancy. Unable to check in new customers at this time.")
        else:
            dict_choices[in_out]()
    else:
        print("that is not a valid option")
    if in_out != "5":
        if query_yes_no("\nContinue?", None):
            start_routine()
        else:
            exit_program()

def create_user():
    username = None
    print("\n'Create user' selected.")
    username = input("Enter your new username: ")
    password = getpass.getpass("Enter your new password (input is hidden): ")
    user_dict[username] = password
    print(user_dict)
    if query_yes_no("\nCreate another user?", None):
        create_user()
    else:
        save_users()

def delete_user():
    username = None
    print("\n'Delete user' selected.")
    username = input("Enter username to delete: ")
    user_dict.pop(username, None)
    print(username + "'s account has been deleted.")
    save_users()

def save_users():
    write_u = csv.writer(open('/home/pi/Documents/ENET_Capstone/users.csv', 'w'))
    for key, value in user_dict.items():
        write_u.writerow([key, value])

def main():
    with open('/home/pi/Documents/ENET_Capstone/parking_database.csv', mode='r') as infile:
        reader = csv.reader(infile)
        for rows in reader:
           loc_dict[rows[0]] = rows[1]
    with open('/home/pi/Documents/ENET_Capstone/users.csv', mode='r') as u_infile:
        u_reader = csv.reader(u_infile)
        for rows in u_reader:
            user_dict[rows[0]] = rows[1]
    print(loc_dict)
    print(user_dict)
    start_routine()

if __name__ == "__main__":
    main()
