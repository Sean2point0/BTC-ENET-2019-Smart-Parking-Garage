class parkingSpot:

    """ Class to hold all the info for each parking spot. Each instance
        is created on start up when the program opens the parking_database.csv
        file. Each row of the csv is converted into a dictionary and passed
        as a parameter when the parkingSpot instance is initialized. The
        allowedAttributes are the csv column headers which are also
        the dictAttributes.keys()
    """

    allowedAttributes = []

    def __init__(self, dictAttributes):
        for key, value in dictAttributes.items():
            if key is not None and value is not None:
                setattr(self, key, value)

    def attributesToDict(self):

        """ When it is time to store customer info back to a csv file
            attributesToDict() returns a dictionary of all the current
            attributes using allowedAttributes as the keys
        """

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
