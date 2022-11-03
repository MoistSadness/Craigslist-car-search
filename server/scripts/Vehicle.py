'''
Object stores craigslist listings that match the search criteria
Contains the following:
    title 
    url
    price 
    drive 
    odometer 
'''
class VEHICLE:
    def __init__(self):
        self.title = "none"
        self.url = "none"
        self.price = "none"
        self.drive = "none"
        self.odometer = "none"

    # Setter functions
    def setTitle(self, title):
        self.title = str(title)
    def setURL(self, url):
        self.url = str(url)
    def setPrice(self, price):
        self.price = int(re.sub("[^0-9]", "", price))
    def setDrive(self, drive):
        self.drive = str(drive)
    def setOdometer(self, odometer):
        self.odometer = int(odometer)
    
    # Getter functions
    def getTitle(self):
        return self.title
    def getUrl(self):
        return self.url
    def getPrice(self):
        return self.price
    def getDrive(self):
        return self.drive
    def getOdometer(self):
        return self.odometer
    
    def printObj(self):
        print("Title:\t\t", self.title)
        print("URL:\t\t", self.url)
        print("Price:\t\t", self.price)
        print("Drive:\t\t", self.drive)
        print("Odometer:\t", self.odometer)
    
    '''
    Returns a string containing all the data
    '''
    def returnString(self):
        textStr = ""

        textStr += "Title:      "
        textStr += self.title
        textStr += "\n"

        textStr += "URL:        "
        textStr += self.url
        textStr += "\n"

        textStr += "Price:      "
        textStr += str(self.price)
        textStr += "\n"

        textStr += "Drive:      "
        textStr += self.drive
        textStr += "\n"

        textStr += "Odometer:   "
        textStr += str(self.odometer)
        textStr += "\n"


        return textStr
