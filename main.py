from bs4 import BeautifulSoup
import requests
from csv import writer
import re
from datetime import datetime

#get today's date
today = datetime.now()
today = today.strftime("%Y-%m-%d")

#get html format of marciano dining's website
html_text = requests.get('https://www.bu.edu/dining/location/marciano/#menu').text

#create BeautifulSoup object
soup = BeautifulSoup(html_text, 'lxml')

#finds the menu that corresponds to today's date
current = soup.find('ol', {"data-menudate":today})

#finds all the food items corresponding to today's menu
foods = current.find_all('li', class_='menu-item menu-main menu-has-warning')


def find_foods():
    #writing to csv file
    with open('foods.csv' , 'w', encoding='utf8', newline='') as f:
        thewriter = writer(f)
        header = ['Food', 'Calories', 'Protein (g)', 'Carbs (g)']
        thewriter.writerow(header)  
        #loop through the food items and write their nutrition values to the cvs file
        for food in foods:
            try:
                #find info on calories, protein, carbs, and the food name itself
                calories = food.find('li', class_='menu-nutrition-cals').text
                protein = food.find('li', class_='menu-nutrition-protein').text
                carbs = food.find('li', class_='menu-nutrition-carbs').text
                food_name = food.find('h4', class_='js-nutrition-open-alias menu-item-title').text
                info = [food_name, re.sub(r'[^\d]', "", calories), re.sub(r'[^\d]', "", protein), re.sub(r'[^\d]', "", carbs) ]
                thewriter.writerow(info)
            except:
                food_name = food.find('h4', class_='js-nutrition-open-alias menu-item-title').text
                #ignore food items that requires customization
                if "Create" not in food_name:
                    info = [food_name, 0, 0, 0]
                    thewriter.writerow(info)
                else:
                    continue
find_foods()
