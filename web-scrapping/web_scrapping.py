import requests
from bs4 import BeautifulSoup
import csv

url = 'https://books.toscrape.com'

titles = []
prices = []
ratings = []
availability = []


def scrape_web(url):

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    titles = soup.find_all('h3')
    prices = soup.find_all('p', class_='price_color')
    ratings = soup.find_all('p', class_='star-rating')
    availability = soup.find_all('p', class_='instock')

    return titles, prices, ratings, availability


def save_csv(books, filename):

    titles, prices, ratings, availability = books

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        write_csv = csv.writer(file)

        write_csv.writerow(['Title', 'Price', 'Rating', 'Availability'])

        for title, price, rating, available in zip(titles, prices, ratings, availability):
            stars = rating['class'][1]
            pricing = price.text.replace('Â£', '£')
            write_csv.writerow(
                [title.text, pricing, stars, available.text.strip()])


for page in range(1, 51):
    url = f'https://books.toscrape.com/catalogue/page-{page}.html'
    page_titles, page_prices, page_ratings, page_availability = scrape_web(url)

    titles.extend(page_titles)
    prices.extend(page_prices)
    ratings.extend(page_ratings)
    availability.extend(page_availability)


books = titles, prices, ratings, availability
save_csv(books, 'data.csv')
print('CSV file successfully created.')
