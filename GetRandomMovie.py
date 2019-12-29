#!/usr/bin/env python
import csv
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
from pathlib import Path
import time
import sys

email = "ENTER EMAIL HERE"
password = "ENTER PASSWORD HERE"
downloadfolder = 'ENTER DOWNLOAD FOLDER HERE'
watchlistpath = downloadfolder + 'WATCHLIST.csv'


def delete_old_watchlist():

    print('Deleting old watchlist...')

    # delete existing watchlist if there is one
    watchlist = Path(watchlistpath)
    if watchlist.is_file():
        os.remove(watchlistpath)


def open_login_page():

    print('Opening IMDb login page...')

    driver.get("https://www.imdb.com/registration/signin?u=/")
    elem = driver.find_element_by_link_text("Sign in with IMDb")
    elem.click()


def login():
    try:
        print('Logging in and downloading watchlist...')

        # enter the email address
        elem = driver.find_element_by_name("email")
        elem.send_keys(email)

        # wait for 3 seconds to avoid captcha
        time.sleep(3)

        # enter the password
        elem = driver.find_element_by_name("password")
        elem.send_keys(password)

        # wait for 3 seconds to avoid captcha
        time.sleep(3)

        # click login button
        elem = driver.find_element_by_id("signInSubmit")
        elem.click()

        driver.get("https://www.imdb.com/list/watchlist?ref_=nv_usr_wl")
        elem = driver.find_element_by_link_text("Export this list")
        elem.click()

    except:
        input('Error - probably captcha!')
        quit()


def get_random_movie():

    time.sleep(3)   # wait 3 seconds for download
    tries = 0

    watchlist = Path(watchlistpath)

    if watchlist.is_file() == False:
        # give the download more time if it hasn't succeeded yet
        while (watchlist.is_file() == False and (tries <= 3)):
            time.sleep(3)
            tries = tries + 1
            if tries > 3:
                input(
                    'Error - watchlist has not been downloaded correctly!')
                quit()
        else:
            movies, selected_movie = pick_movie()

    else:
        movies, selected_movie = pick_movie()

    return movies, selected_movie


def pick_movie():
    movies = []
    with open(watchlistpath, encoding='latin_1') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        for row in csv_reader:
            if row[5] != 'Title':  # don't add first row

                # create dictionary for each movie
                movie = {'title': row[5], 'link': row[6]}
                movies.append(movie)

    selected_movie = random.choice(movies)
    return movies, selected_movie


def printresults():
    print('Selecting a movie from ' + str(len(movies)) + ' movies!\n')
    print('Randomly selected movie:\n\n' + selected_movie['title'] + '\nLink: '
          + selected_movie['link'])


delete_old_watchlist()

driver = webdriver.Chrome()
driver.implicitly_wait(30)

open_login_page()
login()

movies, selected_movie = get_random_movie()
printresults()
driver.close()

result = input("\nPress 1 to pick another movie, press 2 to exit!")

while result == '1':
    selected_movie = random.choice(movies)
    printresults()
    result = input("\nPress 1 to pick another movie, press 2 to exit!")
else:
    quit()
