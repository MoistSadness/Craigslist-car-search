'''
Search_For_Car() function takes the user input to search craigslist for the desired car 
and parse the retrieved HTML file for a matching search result
'''

import json
import requests
from bs4 import BeautifulSoup 

'''
Function takes a dictionary as input and returns a list of keys
'''
def getList(dict):
    return[*dict]

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

    # Make the vehicle search in every location in the list of locations 
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
        print(search_results.prettify())

        # Use beautiful soup to find all elements by class
        search_results_class = search_results.find_all("div", class_="result-row")
        for result in search_results_class:
            #print(result, end="\n*2")
            

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
            print("Searching for:\t", carList[car]["Model"], "\t", carList[car]["Mileage"], "\t",  carList[car]["Price"])
            Search_For_Car(carList[car]["Model"], carList[car]["Mileage"], carList[car]["Price"])


if __name__ == "__main__":
    main()