import requests
import json
from bs4 import BeautifulSoup
#from fake_useragent import UserAgent
from requests_html import HTMLSession

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
Returns an array of Vehicle objects containing all the matches
'''
def Search_Craigslist(location, model, year, mileage, price):
    session = HTMLSession()
    # URL["Bay Area"] = "https://sfbay.craigslist.org/d/cars-trucks/search/cta?query=" + model
    URL = "https://" + location + ".craigslist.org/search/cta?query=" + model
    #ua = UserAgent()

    # Get the webpage 
    page = session.get("https://sfbay.craigslist.org/")

    print(page.html.render())

    # Creating a beautiful soup object
    soup = BeautifulSoup(page.content, "html.parser")
    #print(soup)
    #return []

    # Use Beautiful Soup to find all search results             
    search_results = soup.find(id="search-results")
    print(search_results)

    vehicle_url_list = []

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
                vehicle_url_list.append(subTitle['href'])      # extracts the URL from the HTML tag
            else:
                #print("Not a ", model)
                pass
    
    ###################

    # Creating a list to store the VEHICLE objects generate by the script
    VEHICLE_OBJ_LIST = []

    # Visiting each link and getting desired data and inserting it into a VEHICLE object
    for vehicle in vehicle_url_list:
        VEHICLE_OBJ = Vehicle.VEHICLE()         # Creating object to store data

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
