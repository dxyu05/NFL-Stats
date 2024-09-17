import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

#'https://www.pro-football-reference.com/players/E/EricAl01.htm'   <- Link to team def as template

#Gets the URL to be scraped and takes the page content as its input
URL = "https://www.pro-football-reference.com/players/"
page = requests.get(URL)

if page.status_code == 200:
    soup = BeautifulSoup(page.text, 'html.parser')
else:
    print(f"Failed to retrieve data: {page.status_code}")


#Finds the content div and gets the contents of an unordered list
#These list items contain hrefs to help build links to NFL players sorted by an index of letters
results = soup.find(id="content")
items = results.find("ul", class_="page_index")

positions = set(["(QB)", "(RB)", "(WR)", "(TE)", "(K)"])
offense = {"QB": [], "RB": [], "WR": [], "TE": [], "K": []}

#Loops through each list item and builds a link to a letter
for item in items:
    
    #Gets the link to each letter and parses through it
    link = "https://www.pro-football-reference.com" + str(item.find('a', href=True)['href'])
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")

    #Gets the link of each player that is currently active
    players = soup.find(id="div_players")
    for bold in players.find_all('b'):

        if bold.contents[-1].strip() in positions:
            link = "https://www.pro-football-reference.com"  + str(bold.find('a', href = True)['href'])
            
            #sorts players by position
            if bold.contents[-1].strip() == "(QB)":
                offense["QB"].append(link)
            elif bold.contents[-1].strip() == "(RB)":
                offense["RB"].append(link)
            elif bold.contents[-1].strip() == "(WR)":
                offense["WR"].append(link)
            elif bold.contents[-1].strip() == "(TE)":
                offense["TE"].append(link)
            else:
                offense["K"].append(link)
        
    #Sleeps to avoid rate limiting as per PFR scraping guidlines
    time.sleep(4)
    print(offense["K"])

'''
#Gets the table, apply below
url = requests.get('https://www.pro-football-reference.com/players/E/EricAl01.htm')
soup = BeautifulSoup(url.content, 'html.parser')
print(position)
c = url.content
df = pd.read_html(c)[0]
#print(df)
'''