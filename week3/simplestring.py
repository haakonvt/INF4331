class SimpleString:
    "Get a string from console input, store it and print it in CAPS if requested"

    def __init__(self):
        "Initiate SimpleString-object"

    def getString(self):
        "Enter and save user input"
        self.latest_user_input = raw_input('Please input a string..: ')

    def printString(self):
        "Print user input in CAPS"
        print self.latest_user_input.upper()
