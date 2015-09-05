#! /usr/bin/env python
# python 2.7

from bs4 import BeautifulSoup
import urllib
import re
import json
import sys


# returns hash of book dom element
def get_book_info(book):
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
    if published != '':
        published = int(published)
    else:
        published = -1
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


# USE DEFENSEIVE PROGGRAMMING
def get_movie_info(movie):
    movie_name = movie.find_next('a').text
    movie_url = 'http://www.imdb.com' + movie.find_next('a').get('href')
    info = movie.find_next('div', class_='rating')
    try:
        info = info.get('title')
        avg_rating = re.findall('rated this ([0-9.]*)', info)[0]
        avg_rating = float(avg_rating)
        num_ratings = re.findall('([0-9,]*) votes', info)[0]
        num_ratings = int(num_ratings.replace(',', ''))
    except:
        avg_rating = -1
        num_ratings = -1
    published = movie.find_next('span', class_='year_type').text
    try:
        published = int(re.findall('\(([0-9]*)', published)[0])
    except ValueError:
        published = -1

    movie_hash = {
        'movie_name': movie_name,
        'movie_url': movie_url,
        'avg_rating': avg_rating,
        'num_ratings': num_ratings,
        'published': published
    }
    return movie_hash


# parses goodreads
def get_goodreads_data(base_url, pages=41):
    books_hash = []
    for page in range(1, pages+1):
        print('Getting info from page %s' % page)
        r = urllib.urlopen('%s?page=%s' % (base_url, page))
        soup = BeautifulSoup(r.read(), 'html.parser')
        books = soup.find_all('div', class_='elementList')
        books_hash += [get_book_info(book) for book in books]
        print("we have %d books so far" % len(books_hash))
    return books_hash


def get_imdb_data(base_url, movies):
    movies_hash = []
    for start in range(1, movies, 50):
        print('Getting info from movie %s' % start)
        r = urllib.urlopen('%s&start=%s' % (base_url, start))
        print('%s&start=%s' % (base_url, start))
        soup = BeautifulSoup(r.read(), 'html.parser')
        movies = soup.find_all('', class_='title')
        movies_hash += [get_movie_info(movie) for movie in movies]
        print("we have %d movies so far" % len(movies_hash))
    return movies_hash


def defaults(data_points):
    if('books' in data_points):
        book_movies_url = 'https://www.goodreads.com/shelf/show/books-made-into-movies'
        books_hash = get_goodreads_data(base_url=book_movies_url, pages=41)
        books_output_filename = 'goodreads_ratings.json'

        with open(books_output_filename, 'w') as outfile:
            json.dump(books_hash, outfile)

    if('movies' in data_points):
        movies_base_url = 'http://www.imdb.com/search/title?at=0&keywords=based-on-novel&sort=moviemeter&title_type=feature&year=1990,2015'
        movies_hash = get_imdb_data(base_url=movies_base_url, movies=4578)
        movies_output_filename = 'movies_ratings.json'

        with open(movies_output_filename, 'w') as outfile:
            json.dump(movies_hash, outfile)


if __name__ == "__main__":
    print(sys.argv)
    defaults(sys.argv)
