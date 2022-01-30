'''
Search_For_Car() function takes the user input to search craigslist for the desired car 
and parse the retrieved HTML file for a matching search result

A huge help: https://realpython.com/python-send-email/

Apparently gmail's smtp server does not work most of the time 
https://zetcode.com/python/smtplib/
'''

from email import message
import json
import re
import requests
from bs4 import BeautifulSoup 

import smtplib
import ssl
from email.mime.text import MIMEText

'''
Object that stores craigslist listings that match the search criteria
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


'''
Function takes a dictionary as input and returns a list of keys
'''
def getList(dict):
    return[*dict]

'''
Takes a list string of strings and parses out the vehicle's mileage 
Compares extracted data to the search criteria
    If it is a match, return mileage as int
    Otherwise, ignore and return
'''
def Scrape_Mileage(vehicleDataStr):
    # Data is currently one massive string with multiple lines, needs to be splic
    for line in vehicleDataStr.splitlines():
        #print(line)
        if "odometer" in line:
            odometerLst = line.split(":")
            #print(odometerLst[0], "\t", int(odometerLst[1]))
            return int(odometerLst[1])
        else:
            pass

'''
Takes a list string of strings and parses out the vehicle's mileage 
Compares extracted data to the search criteria
    If it is a match, return mileage as int
    Otherwise, ignore and return
'''
def Scrape_Drive(vehicleDataStr):
# Data is currently one massive string with multiple lines, needs to be splic
    for line in vehicleDataStr.splitlines():
        #print(line)
        if "drive" in line:
            driveList = line.split(":")
            #print(driveList[0], "\t", driveList[1])
            return driveList[1].strip()         #   .strip() removes whitespace

    

'''
Function does all the searching and parsing for search results
Runs once for every car
'''
def Search_For_Car(model, mileage, price):
    # Creating URLs, one for each location
    URL = {}
    URL["Bay Area"] = "https://sfbay.craigslist.org/d/cars-trucks/search/cta?query=" + model
    #URL["Sacramento"] = "https://sacramento.craigslist.org/d/cars-trucks/search/cta?query=" + model

    # getting a list of keys from the urls
    keyListLocations = getList(URL)

    # Make the vehicle search in every location in the list of URLs 
    for location in range(len(keyListLocations)):
        # Get the webpage 
        page = requests.get(URL[keyListLocations[location]])
        #print(page.text)
        #print("Page for ", URL[keyListLocations[location]])

        # Creating a beautiful soup object
        soup = BeautifulSoup(page.content, "html.parser")
        #print(soup.prettify())

        # Use Beautiful Soup to find all search results             
        search_results = soup.find(id="search-results")
        #print(search_results.prettify())

        vehicle_link_list = []

        # Use beautiful soup to find all elements by class
        search_results_class = search_results.find_all("li", class_="result-row")

        # Extract vehicle URLs from each class
        # Make sure the advertisments title has a match to the search vehicle
        # Because assholes on craigslist advertise their stupid for f150s or silverados
        # On a search for Land Cruisers
        for result in search_results_class:
            titleMatch = result.find_all('a', class_='result-title hdrlnk')

            # If the model is found in the title of the listing, acquire the listing's URL.
            # Otherwise ignore the listing
            for subTitle in titleMatch:
                if model in subTitle.get_text():            # use python's in operator to find substrings  
                    #print(subTitle.get_text())              # .get_text() extracts the raw text from the html tag
                    vehicle_link_list.append(subTitle['href'])      # extracts the URL from the HTML tag
                else:
                    #print("Not a ", model)
                    pass
        
        ###################

        # Creating a list to store the VEHICLE objects generate by the script
        VEHICLE_OBJ_LIST = []

        # Visiting each link and getting desired data and inserting it into a VEHICLE object
        for vehicle in vehicle_link_list:
            VEHICLE_OBJ = VEHICLE()         # Creating object to store data

            # SETTING URL HERE
            VEHICLE_OBJ.setURL(vehicle)

            # Acquiring web page
            vehiclePage = requests.get(vehicle)

            # Create beautiful soup object for page
            vehicleSoup = BeautifulSoup(vehiclePage.content, "html.parser")
            #print(vehicleSoup.prettify())

            # ACQUIRING THE TITLE HERE 
            VEHICLE_OBJ.setTitle(vehicleSoup.find(id="titletextonly").get_text())
            #print(VEHICLE_OBJ.getTitle())         # Printing title so user has visual aid to see the script progress
            
            # ACQUIRING THE PRICE HERE
            try:
                VEHICLE_OBJ.setPrice(vehicleSoup.find(class_="price").get_text())

            except AttributeError:
                print("Price not found")


            # ACQUIRING THE DRIVE AND ODOMETER DATA HERE
            vehicleData = vehicleSoup.find_all('p', class_="attrgroup")     # Stores data in list
            
            # Since find_all() gave us a list of strings, we need to merge
            # them into one superstring
            idk = ""
            for x in range(len(vehicleData)):
                idk += vehicleData[x].get_text()

            # Scrape the odomenter and drive data from the superstring
            VEHICLE_OBJ.setOdometer(Scrape_Mileage(idk))     # Acquire the odometer reading
            VEHICLE_OBJ.setDrive(Scrape_Drive(idk))                  # Acquire the vehicle's drive

            # Check if the VEHICLE object matches the criteria
            # If match, add to list, otherwise ignore
            try:
                if int(VEHICLE_OBJ.getOdometer()) < int(mileage) and int(VEHICLE_OBJ.getPrice()) < int(price):
                    VEHICLE_OBJ_LIST.append(VEHICLE_OBJ)
                    print("Found Match:\t", VEHICLE_OBJ.getTitle())         # Printing title so user has visual aid to see the script progress
                else: 
                    print("Not a Match")
            except ValueError:
                print("No Valid price found!")

            '''
            # Add the VEHICLE object to the list of matching objects
            VEHICLE_OBJ_LIST.append(VEHICLE_OBJ)
            '''
            #break       # to only work on one link

        return VEHICLE_OBJ_LIST

'''
Function takes a list of VEHICLE objects
Sends email containing the contents of the list to my email address
'''
def SendEmail(VEHICLE_LIST):
    # Now that the list of objects has been generated,
    # We will email the results to my email address

    port = 1025

    sender = 'moistsadness@gmail.com'
    reciever = 'moistsadness666@gmail.com'

    # Creating a string with the message
    messageStr = ''
    for vehicle in VEHICLE_LIST:
        messageStr += vehicle.returnString()
        messageStr += "\n"

    # print(messageStr)

    # Creating MIMEText object
    msg = MIMEText(messageStr)
    msg['Subject'] = 'Test Email'
    msg['From']  = sender
    msg['To'] = reciever

    # Creating local mail server
    # Make sure to run: python -m smtpd -n -c DebuggingServer lhost:1025
    # To create a local mail server
    with smtplib.SMTP('localhost', port) as server:
        # server.login('username', 'password')      # Do not need to log into local server
        server.sendmail(sender, reciever, msg.as_string())
        print("\n**********************")
        print('*    sending mail    *')
        print("\**********************")


'''
Imports data from JSON file and uses it to run the desired searches
'''
def main():
    # Open the text file containing car data

    VEHICLE_LIST = []

    with open("cars.json", "r") as carJSON:
        carList = json.loads(carJSON.read())
        # print(cars.read())
        
        # Iterate through the list of cars and run the search for each one
        for car in range(len(carList)):
            print("********************************************")
            print("Searching for:\t", carList[car]["Model"], "\t", carList[car]["Mileage"], "\t",  carList[car]["Price"])
            print("********************************************")

            Matched_Vehicles = Search_For_Car(carList[car]["Model"], carList[car]["Mileage"], carList[car]["Price"])

            #print("\n\n--------\--------\--------\--------\--------\n\n")
            VEHICLE_LIST.extend(Matched_Vehicles)
    
    # Sending email
    SendEmail(VEHICLE_LIST)

if __name__ == "__main__":
    main()