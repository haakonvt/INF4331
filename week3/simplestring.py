class SimpleString:
    "Get a string from console input, store it and print it in CAPS if requested"

    def __init__(self):
        "Initiate SimpleString-object"

    def getString(self):
        "Enter and save user input"
        self.latest_user_input = raw_input('Please input a string..: ')

    def printString(self):
        "Print user input in CAPS"
        try:
            print self.latest_user_input.upper()
        except AttributeError:
            print "No user input given via .getString(), see 'pydoc simplestring'"

if __name__ == "__main__":
    s = SimpleString()
    s.getString()
    s.printString()
