# get national day as inspiration

import requests
from bs4 import BeautifulSoup

url = 'https://nationaltoday.com/what-is-today/'

def get_day_cards():
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    day_cards = soup.find_all('div', class_='day-card')
    return day_cards

if __name__ == '__main__':
    print(get_day_cards())
