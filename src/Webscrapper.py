from bs4 import BeautifulSoup 
import sys
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re
import pandas as pd

#.........................................<CODE STRUCTURE>.................................
#      two parts
#      1. scraping titles, ratings, votes, year, duration, metascore, pgrating
#      2. scraping the cast, genre, director_list
#
#      two drivers
#      `driver` for scraping the data in first part
#      `newdriver` for scraping the data in the second part
#      
#      url = "https://www.imdb.com/search/title/?title_type=feature&release_date=,2023-12-15&primary_language=en"
#                                                                                       |
#      `links` contains the links for all the movies for scraping the second part data  |
#                                                                                       !
#      data updated till `2023-12-15` you can change it to any date right here ---------^





# Set up the Selenium webdriver (make sure you have the appropriate webdriver installed)
driver = webdriver.Chrome()


# Load the initial URL
url = "https://www.imdb.com/search/title/?title_type=feature&release_date=,2023-12-15&primary_language=en"
driver.get(url)


def click_show_more():
    # IMDB uses a Dynaic Show More button at the bottom of page for loading more data this button needs to be
    # clicked repeatedly to load more html data.

    try:
        time.sleep(2)
        show_more_button = driver.find_element(By.XPATH , "/html/body/div[2]/main/div[2]/div[3]/section/section/div/section/section/div[2]/div/section/div[2]/div[2]/div[2]/div/span/button")
        driver.execute_script("arguments[0].scrollIntoView(true);", show_more_button)
        
        # adding a delay for the screen to load
        time.sleep(2)

        show_more_button.click()
        return True
    except Exception as e:
        print(f"Error clicking 'show more': {e}")
        return False


num_clicks = 35

# Click the "show more" button multiple times
for _ in range(num_clicks):
    if not click_show_more():
        break

def get_ratings_votes(exp):
    # Uses regular expression for extracting rating and votes
    # 'exp' a string containing rating and votes in a combine expression.

    pattern = re.compile(r'(\d+\.\d+?)\s*\(([^)]+)\)')
    match = pattern.search(exp)
    multipliers = {"K" : 1000 , "M" : 1000000}
    if match:
        if match.group(2)[-1] in multipliers:
            numeric_part, multiplier = match.group(2)[:-1], match.group(2)[-1] 
            votes = float(numeric_part)*multipliers[multiplier]
        else:
            votes = float(match.group(2))
        return float(match.group(1)) , votes
    return "NA", "NA"


# Loading the `html` data 
soup = BeautifulSoup(driver.page_source, 'html.parser')
movie_data = soup.findAll('div', attrs = {'class': "ipc-metadata-list-summary-item__c"})


titles = soup.findAll('h3', attrs={'class': "ipc-title__text"})
titles = [".".join(x.text.split(".")[1:]) for x in titles][:-1]

ratings = []
votes = []
metascores = []
years = []
durations = [] 
rated = []
links = []
rating_cls = "ipc-rating-star ipc-rating-star--base ipc-rating-star--imdb ratingGroup--imdb-rating"
for id, x in enumerate(movie_data):
    
    rating = x.find('span', attrs={'class': rating_cls}).text  if x.find('span', attrs={'class': rating_cls}) else "NA"
    rating, vote = get_ratings_votes(rating)
    ratings.append(rating)
    votes.append(vote)
 
    metascore = x.find('span',attrs= {"class": "sc-b0901df4-0 bcQdDJ metacritic-score-box"}).text if x.find('span' ,attrs={"class": "sc-b0901df4-0 bcQdDJ metacritic-score-box"}) else 'NA'
    metascores.append(metascore)
    
    metadata = x.find('div',attrs= {"class": "sc-43986a27-7 dBkaPT dli-title-metadata"}) if x.find('div' ,attrs={"class": "sc-43986a27-7 dBkaPT dli-title-metadata"}) else 'NA'

    metadata = [x.text for x in metadata]
    
    years.append(metadata[0])


    try:
        durations.append(metadata[1])
    except:
        durations.append("NA")
    
    
    try:
        if metadata[2] == "Not Rated":
            metadata[2]="NA"
        rated.append(metadata[2])
    except:
        rated.append("NA")

    
    link = x.find('a',attrs= {"class": "ipc-lockup-overlay ipc-focusable"}).get('href') if x.find('span' ,attrs={"class": "sc-b0901df4-0 bcQdDJ metacritic-score-box"}) else 'NA'
    links.append(link)

#Getting the cast
casts = []
genres = []
director_list = []

newdriver = webdriver.Chrome()


for link in links:
    if link != 'NA':
        newdriver.get("https://www.imdb.com" + link)
        soup = BeautifulSoup(newdriver.page_source, 'html.parser')
        
        genre = soup.find('div', attrs={'class':"ipc-chip-list__scroller"})
        # genre = [x.text for x in genre]
        try:
            genres.append(", ".join([x.text for x in genre]))
        except:
            genres.append("NA")
            
        cast = soup.findAll('div', attrs={'class': 'sc-bfec09a1-5 hNfYaW' })  
        try:
            casts.append(", ".join([x for x in [x.find('a', attrs={'class': 'sc-bfec09a1-1 gCQkeh'}).text for x in cast][:4]]))
        except:
            casts.append("NA")

        director = soup.find('div', attrs={'class': 'ipc-metadata-list-item__content-container'}) 
        try:
            director_list.append(director.text) 
        except:
            director_list.append("NA")

    else:
        genres.append("NA")
        casts.append("NA")
        director_list.append("NA")


movies_data = pd.DataFrame({"Moive Name" : titles, "Rating" : ratings, "Votes" : votes, "Meta Score" : metascores, "Genre" : genres , 
                            "PG Rating" : rated , "Year" : years , "Duration" : durations, "Cast" : casts , "Director" : director_list })

# saving to the directory
movies_data.to_csv("metadata/imdb_movie_data_2023.csv", index = True)