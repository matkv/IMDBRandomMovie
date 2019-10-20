#!/usr/bin/env python
import csv
import random

movies = []
with open('WATCHLIST.csv', encoding='latin_1') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')

    for row in csv_reader:
        if row[5] != 'Title':  # don't add first row

            # create dictionary for each movie
            movie = {'title': row[5], 'link': row[6]}
            movies.append(movie)

selected_movie = random.choice(movies)
print('Randomly selected movie:\n\n' + selected_movie['title'] + '\nLink: '
      + selected_movie['link'])

input("\nPress enter to exit!")
