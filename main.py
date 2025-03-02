import pandas as pd 
import matplotlib.pyplot as plt 
import requests
from bs4 import BeautifulSoup

from_year = 2012
country = None

def getYearsSource() -> str:

    url = f"https://www.setlist.fm/search?query={country}"

    headers = {"User-Agent": "Mozilla/5.0"}  

    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")

    return soup.find("select", {"id": "id18"})


def dataSource() -> list[list[str], list[int]]:

    year_sources = getYearsSource()

    year_list = []
    count_list = []

    if year_sources:

        options = year_sources.find_all('option')

        for option in options:
            text = option.text.strip()

            if ' (' in text:
                year, count = text.split(' (')
                
                if (int(year) >= from_year):   
                    count = count.replace(')', '')
                    
                    year_list.append(year)
                    count_list.append(int(count))

    return year_list, count_list

def buildTotalConcertsChart():

    data_source = dataSource()

    years = data_source[0]
    counts = data_source[1]

    data = pd.DataFrame({
        'year': years,
        'count': counts
    })

    data.sort_values(by='year', ascending=True, inplace=True)

    plt.style.use('seaborn')

    plt.figure(figsize=(12, 6))

    plt.bar(data['year'], data['count'], alpha=.6, color='purple')
    plt.xlabel('Year')
    plt.ylabel('Count')
    plt.title(f'Concerts in {country} ({from_year} - 2025)')
    plt.xticks(data['year'], rotation=45)

countries = ['malaysia', 'thailand', 'singapore']

for current_country in countries:
    country = current_country.capitalize()
    buildTotalConcertsChart()
