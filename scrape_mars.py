#!/usr/bin/env python
# coding: utf-8

#################################################################################
# Mission to Mars Web Scrapping
#  This application will build a web application that scrapes various websites 
# for data related to the Mission to Mars and displays the information in a 
# single HTML page
#################################################################################

#--------------------------------------------------------------------------------
# Dependencies and Setup
#--------------------------------------------------------------------------------
import pandas as pd
from bs4 import BeautifulSoup
import requests
from splinter import Browser

################################################################################
# NASA Mars News
# Scrape the [NASA Mars News Site](https://mars.nasa.gov/news/) and collect the 
# latest News Title and Paragraph Text. Assign the text to variables that you 
# can reference later.
#################################################################################

#--------------------------------------------------------------------------------
# URL of page to be scraped for the Mars News info
#--------------------------------------------------------------------------------
url = 'https://mars.nasa.gov/news/'

#--------------------------------------------------------------------------------
# Retrieve page with the requests module
#--------------------------------------------------------------------------------
response = requests.get(url)

#--------------------------------------------------------------------------------
# Create BeautifulSoup object; parse with 'html.parser'
#--------------------------------------------------------------------------------
soup = BeautifulSoup(response.text, 'html.parser')

#--------------------------------------------------------------------------------
# Find the Title & Paragraph Text for the feature news article.
#--------------------------------------------------------------------------------
news_title = soup.find('div', class_="slide").find('div', class_='content_title').text
news_title = news_title.replace('\n', '')

news_p = soup.find('div', class_="slide").div.a.div.div.text
news_p = news_p.replace('\n', '')

#################################################################################
# JPL Mars Space Images - Featured Image
# Visit the url for JPL Featured Space Image at
# https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars).
# 
# Use splinter to navigate the site and find the image url for the current 
# Featured Mars Image and assign the url string to a variable called 
# `featured_image_url`.
#################################################################################

executable_path = {'executable_path': 'C:\ChromeDriver\chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)

#--------------------------------------------------------------------------------
# Define the HTML object
#--------------------------------------------------------------------------------
html = browser.html

#--------------------------------------------------------------------------------
# Parse HTML with Beautiful Soup
#--------------------------------------------------------------------------------
soup = BeautifulSoup(html, 'html.parser')

#--------------------------------------------------------------------------------
# Find and store the url to the featured image
#--------------------------------------------------------------------------------
primary_feature = soup.find('section', class_="primary_media_feature")
item = primary_feature.find('div', class_='carousel_items')
article = item.find('article', class_='carousel_item')['style']

#--------------------------------------------------------------------------------
# Split the article by "'" so we can capture the ending part of the url, then 
# add the front and ending part of the url to the feature image.
#--------------------------------------------------------------------------------
article_arr = article.split("\'")
featured_image_url = ('https://www.jpl.nasa.gov' + article_arr[1])

#################################################################################
# Mars Weather
# Visit the Mars Weather twitter account at
# (https://twitter.com/marswxreport?lang=en) and scrape the latest Mars weather 
# tweet from the page. Save the tweet text for the weather report as a variable 
# called `mars_weather`.
#################################################################################

#--------------------------------------------------------------------------------
# URL of page to be scraped for the Mars Weather data
#--------------------------------------------------------------------------------
url = 'https://twitter.com/marswxreport?lang=en'

#--------------------------------------------------------------------------------
# Retrieve page with the requests module
#--------------------------------------------------------------------------------
response = requests.get(url)

#--------------------------------------------------------------------------------
# Create BeautifulSoup object; parse with 'html.parser'
#--------------------------------------------------------------------------------
soup = BeautifulSoup(response.text, 'html.parser')

#--------------------------------------------------------------------------------
# Capture the latest mars weather statement
#--------------------------------------------------------------------------------
mars_weather = soup.find('p', class_="TweetTextSize").text

#################################################################################
# Mars Facts
# Visit the Mars Facts webpage [here](http://space-facts.com/mars/) and use 
# Pandas to scrape the table containing facts about the planet including 
# Diameter, Mass, etc.
#################################################################################

#--------------------------------------------------------------------------------
# Use the read_html function in Pandas to automatically scrape any tabular data 
# from a page.
#--------------------------------------------------------------------------------
url = 'http://space-facts.com/mars/'

tables = pd.read_html(url)

#--------------------------------------------------------------------------------
# Slice off the mars info dataframes using normal indexing.
#--------------------------------------------------------------------------------
mars_info_df = tables[0]
mars_info_df.columns = ['0', '1']

#--------------------------------------------------------------------------------
# Remove header row & rename column headers
#--------------------------------------------------------------------------------
renamed_mars_info_df = mars_info_df.rename(columns={"0":"Feature", "1":"Value"})

#--------------------------------------------------------------------------------
# Set the index to the Feature column
#--------------------------------------------------------------------------------
renamed_mars_info_df.set_index('Feature', inplace=True)

#--------------------------------------------------------------------------------
# Use the Pandas "to_html" method to generate an HTML table from DataFrames.
#--------------------------------------------------------------------------------
html_mars_info_table = renamed_mars_info_df.to_html()

#--------------------------------------------------------------------------------
# Strip unwanted newlines to clean up the table.
#--------------------------------------------------------------------------------
html_mars_info_table = html_mars_info_table.replace('\n', '')

#################################################################################
# Mars Hemispheres
# Visit the USGS Astrogeology site at
# (https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) 
# to obtain high resolution images for each of Mar's hemispheres.
#################################################################################

#--------------------------------------------------------------------------------
# URL of page to be scraped to capture the hemisphere title/image
#--------------------------------------------------------------------------------
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

#--------------------------------------------------------------------------------
# Retrieve page with the requests module
#--------------------------------------------------------------------------------
response = requests.get(url)

#--------------------------------------------------------------------------------
# Create BeautifulSoup object; parse with 'html.parser'
#--------------------------------------------------------------------------------
soup = BeautifulSoup(response.text, 'html.parser')

#--------------------------------------------------------------------------------
# The results are returned as an iterable list
#--------------------------------------------------------------------------------
results = soup.find_all('div', class_="item")

#--------------------------------------------------------------------------------
# Loop through returned results to capture the hemisphere title and link to the 
# page with the link to the full hemisphere image
#--------------------------------------------------------------------------------
sum = 0
title = []
links = []
for result in results:
    #----------------------------------------------------------------------------
    # Error handling
    #----------------------------------------------------------------------------
    try:
        #------------------------------------------------------------------------
        # Identify and store the title of hemisphere in an array/list
        #------------------------------------------------------------------------
        title.append(result.find('a', class_="itemLink").text)
        #------------------------------------------------------------------------
        # Identify and store the link to hemisphere image in an array/list
        #------------------------------------------------------------------------
        links.append('https://astrogeology.usgs.gov/' + result.a['href'])

        # # Print results only if title, price, and link are available
        # if (title and link):
        #     print('-------------')
        #     print(title[sum])
        #     print(links[sum])

        # **********************************************************************
        # Increment index counter
        # **********************************************************************
        sum += 1
    except AttributeError as e:
        print(e)

#--------------------------------------------------------------------------------
# Loop through the pages that point to the hemisphere image and capture the url
# of the hemisphere image
#--------------------------------------------------------------------------------
hemisphere_images = []
this_item = 0

for link in links:
    # Error handling
    try:
        #------------------------------------------------------------------------
        # Define page where full hemisphere image exists with the requests module
        #------------------------------------------------------------------------
        hemisphere = requests.get(link)
        
        #------------------------------------------------------------------------
        # Create BeautifulSoup object; parse with 'html.parser'
        #------------------------------------------------------------------------
        hemi_soup = BeautifulSoup(hemisphere.text, 'html.parser')
        
        #------------------------------------------------------------------------
        # The results are returned as an iterable list
        #------------------------------------------------------------------------
        hemi_results = hemi_soup.find_all('div', class_="downloads")
        
        #------------------------------------------------------------------------
        # Capture image url from the page
        #------------------------------------------------------------------------
        hemi_image = hemi_soup.find('div', class_="downloads").find('ul').find('li').a['href']
        
        #------------------------------------------------------------------------
        # Store image url in an array/list
        #------------------------------------------------------------------------
        hemisphere_images.append(hemi_image)
    
        # # Print results only if hemi_image is available
        # if (hemi_image):
        #     print('-------------')
        #     print(hemi_image)
        #     print(hemisphere_images[this_item])

        # **********************************************************************
        # Increment index counter
        # **********************************************************************
        this_item += 1
    except AttributeError as e:
        print(e)


#################################################################################
# Save both the image url string for the full resolution hemisphere image, and 
# the Hemisphere title containing the hemisphere name. Use a Python dictionary to 
# store the data using the keys `img_url` and `title`.
# 
# Append the dictionary with the image url string and the hemisphere title to a 
# list. This list will contain one dictionary for each hemisphere.
#################################################################################
this_dict_item = 0
hemisphere_image_urls = []
for i in links:
    hemisphere_image_urls.append({'title': title[this_dict_item], 'img_url': links[this_dict_item]})
    this_dict_item += 1

hemisphere_image_urls

