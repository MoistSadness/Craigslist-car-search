'''
Search_For_Car() function takes the user input to search craigslist for the desired car 
and parse the retrieved HTML file for a matching search result
'''

import json
import requests
from bs4 import BeautifulSoup 

'''
Function does all the searching and parsing for search results
'''
def Search_For_Car(model, mileage, price):
    print(model, mileage, price)


'''
Imports data from JSON file and uses it to run the desired searches
'''
def main():
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