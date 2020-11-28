#!/usr/bin/env python
import argparse
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

parser = argparse.ArgumentParser(description='For custom product searching')
parser.add_argument("--searchTerm", type=str, default="generic")
parser.add_argument("--quantity", type=int, default=1)
args = parser.parse_args()

searchTerm = args.searchTerm
quanti = args.quantity


def get_url(search_term):
    """Generate a url from search term"""
    template = 'https://www.amazon.co.uk/s?k={}&ref=nb_sb_noss_1'
    search_term = search_term.replace(' ', '+')
    return template.format(search_term)


def extract_record(item):
    """Extract and return data from a single record"""
    # Item
    atag = item.h2.a

    # Description
    try:
        description = atag.text.strip()
        print(description)
    except AttributeError:
        description = 'no-description'
        print(description)
        return description

    # Product image
    try:
        super_image_parent = item.find('div', {'class': 'a-section aok-relative s-image-square-aspect'})
        image_parent = super_image_parent.find('img')
        image = str(image_parent['src'])
        print(image)
    except AttributeError:
        image = 'no-image'
        image = str(None)
        return image

    # price
    try:
        price_parent = item.find('span', 'a-price')
        price = price_parent.find('span', 'a-offscreen').text
        print(price)
    except AttributeError:
        price = 'no-price'
        print(price)
        return price

    # rating
    try:
        rating = item.i.text
        print(rating)
    except AttributeError:
        rating = 'no-rating'
        print(rating)
        return rating

    # review count
    try:
        review_count = item.find('span', {'class': 'a-size-base', 'dir': 'auto'}).text
        print(review_count)
    except AttributeError:
        review_count = 'no-review-count'
        print(review_count)
        return review_count

    # url
    try:
        url = 'https://www.amazon.co.uk' + atag.get('href')
        print(url)
    except AttributeError:
        url = 'no-url'
        print(url)
        return url

    print(description, image, rating, review_count, url)
    result = (description, image, price, rating, review_count, url)

    return result


def clean_results():
    print("Rewriting results file.")
    file_state = 'w'
    with open('results.csv', file_state, newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # print("Inserting header columns.")
        # writer.writerow(['Description', 'Image', 'Price', 'Rating', 'ReviewCount', 'Url'])


def main(search_term, quantity=1):
    """Run main program routine"""
    options = Options()
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=852x480')
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)

    records = []
    url = get_url(search_term)

    driver.get(url.format(search_term))
    print("Seach term is:", search_term)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    results = soup.find_all('div', {'data-component-type': 's-search-result'})
    print("Total number of results on page:", len(results))

    i = 0
    while i < quantity:
        for item in results[i]:
            record = extract_record(item)
            if record:
                records.append(record)
                i = i + 1
    print("Number of recorded results: ", i)

    driver.close()
    # save data to csv
    with open('results.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(records)


clean_results()
main(searchTerm, quanti)
