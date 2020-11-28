#!/usr/bin/env python
import argparse
import csv
#import numpy
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

    attrib_pass = [["description", bool], ["image", bool], ["price", bool], ["rating", bool], ["review_count", bool],
                   ["url", bool]]

    # Description
    try:
        description = atag.text.strip()
        print(description)
        attrib_pass[0, 2] = True
    except AttributeError:
        description = 'no-description'
        print(description)
        attrib_pass[0, 2] = False
        return

    # Product image
    try:
        image_parent = item.find('div', {'class': 'a-section aok-relative s-image-square-aspect'})
        try:
            image = image_parent.find('img')
            image = image['src']
            attrib_pass[1, 2] = True
        except AttributeError:
            image = ['src', "no-image"]
            attrib_pass[1, 2] = False
            return attrib_pass
    except AttributeError:
        return

    # price
    try:
        price_parent = item.find('span', 'a-price')
        price = price_parent.find('span', 'a-offscreen').text
        print(price)
        attrib_pass[2, 2] = True
    except AttributeError:
        price = 'no-price'
        print(price)
        attrib_pass[2, 2] = False
        return

    # rating
    try:
        rating = item.i.text
        print(rating)
        attrib_pass[3, 2] = True
    except AttributeError:
        rating = 'no-rating'
        print(rating)
        attrib_pass[3, 2] = False
        return attrib_pass

    # review count
    try:
        review_count = item.find('span', {'class': 'a-size-base', 'dir': 'auto'}).text
        print(review_count)
        attrib_pass[4, 2] = True
    except AttributeError:
        review_count = 'no-review-count'
        print(review_count)
        attrib_pass[4, 2] = False
        return attrib_pass

    # url
    try:
        url = 'https://www.amazon.co.uk' + atag.get('href')
        print(url)
        attrib_pass[5, 2] = True
    except AttributeError:
        url = 'no-url'
        print(url)
        attrib_pass[5, 2] = False
        return

    i = 0
    x = 0
    while x < attrib_pass.length:
        print(attrib_pass[x, i])
        while i <= x:
            print(attrib_pass[x, i])
            i = i + 1
        x = x + 1

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
