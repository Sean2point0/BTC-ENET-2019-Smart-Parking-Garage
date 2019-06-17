import sys

def queryYesNo(question):

    """ Ask a yes/no question via input() and return their answer.
        "question" is a string that is presented to the user. The
        "answer" return value is True for "yes" or False for "no".
    """

    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}

    while True:
        sys.stdout.write(question + "[y/n]: ")
        choice = input().lower()
        if choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")
