#! usr/local/bin/env python
# python 2.7

from bs4 import BeautifulSoup
import urllib
import re
import json


# returns hash of book dom element
def get_info(book):
    book_name = book.find('a', class_='bookTitle').text
    book_url = 'http://www.goodreads.com' + book.find('a').get("href")
    author_name = book.find(class_='authorName').text
    author_url = book.find(class_='authorName').get('href')
    info = book.find(class_='greyText smallText').text
    avg_rating = re.findall('avg rating ([0-9.]*)', info)[0]
    avg_rating = float(avg_rating)
    num_ratings = re.findall('([0-9,]*) ratings', info)[0]
    num_ratings = int(num_ratings.replace(',', ''))
    published = re.findall('published ([0-9]*)', info)[0]
    book_hash = {
        'book_name': book_name,
        'book_url': book_url,
        'author_name': author_name,
        'author_url': author_url,
        'avg_rating': avg_rating,
        'num_ratings': num_ratings,
        'published': published
    }
    return(book_hash)


# parses goodreads
def get_goodreads_data(base_url, pages=41):
    books_hash = []
    for page in range(1, pages+1):
        print('Getting info from page %s' % page)
        r = urllib.urlopen('%s?page=%s' % (base_url, page)).read()
        soup = BeautifulSoup(r)
        books = soup.find_all('div', class_='elementList')
        books_hash += [get_info(book) for book in books]
        print("we have %d books so far" % len(books_hash))
    return books_hash


def __main__():
    book_movies_url = 'https://www.goodreads.com/shelf/show/books-made-into-movies'
    books_hash = get_goodreads_data(base_url=book_movies_url, pages=41)
    output_filename = 'good_reads_ratings.json'

    with open(output_filename, 'wb') as outfile:
        json.dump(books_hash, outfile)
