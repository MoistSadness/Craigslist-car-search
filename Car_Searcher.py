'''
Search_For_Car() function takes the user input to search craigslist for the desired car 
and parse the retrieved HTML file for a matching search result
'''

import json
from lib2to3.pgen2 import driver
import requests
from bs4 import BeautifulSoup 

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
            print(VEHICLE_OBJ.getTitle())         # Printing title so user has visual aid to see the script progress
            
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

            # Add the VEHICLE object to the list of matching objects
            VEHICLE_OBJ_LIST.append(VEHICLE_OBJ)
            
            break       # to only work on one link


        # Now that the list of objects has been generated, we will email the results to my email address
        for vehicle in VEHICLE_OBJ_LIST:
            vehicle.printObj()
            print()

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
        self.title = title
    def setURL(self, url):
        self.url = url
    def setPrice(self, price):
        self.price = price
    def setDrive(self, drive):
        self.drive = drive
    def setOdometer(self, odometer):
        self.odometer = odometer
    
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
Imports data from JSON file and uses it to run the desired searches
'''
def main():
    # Open the text file containing car data
    with open("cars.json", "r") as carJSON:
        carList = json.loads(carJSON.read())
        # print(cars.read())

        print("\t\tModel\tMileage\tMax. Price")
        print("\t\t--------------------------------------")
        # Iterate through the list of cars and run the search for each one
        for car in range(len(carList)):
            #print(carList[car])
            print("Searching for:\t", carList[car]["Model"], "\t", carList[car]["Mileage"], "\t",  carList[car]["Price"], "\n")
            Search_For_Car(carList[car]["Model"], carList[car]["Mileage"], carList[car]["Price"])

            print("\n\n--------\--------\--------\--------\--------\n\n")


if __name__ == "__main__":
    main()