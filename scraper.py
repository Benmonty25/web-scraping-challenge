from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import tweepy
import json
import time
import config
import requests
from webdriver_manager.chrome import ChromeDriverManager


def scrape():
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find_all('div', class_="slide")
    news_title = soup.find('div', class_='content_title').find('a').text
    news_title = news_title.replace("\n","")
    

    news_p = soup.find('div', attrs = {'class':'rollover_description_inner'}).text
    
    executable_path = {'executable_path': ChromeDriverManager().install() }
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://spaceimages-mars.com/'
    browser.visit(url)

    html = browser.html   
    soup = BeautifulSoup(html,'html.parser')

    browser.click_link_by_partial_text('FULL IMAGE')
    featured_image = soup.find('img', class_='headerimage fade-in')['src']

    featured_image_url = url + featured_image

    df = pd.read_html('http://space-facts.com/mars/')[0]
    df.columns=['description','value']
    df.set_index('description', inplace=False)
    
    html_table = df.to_html()
    html_table

    html_table.replace('\n', '')

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html

    soup = BeautifulSoup(html, 'html.parser')

    results = soup.find_all('div', class_='item')

    mars_dictionary = []

# Iterate through each page
    for result in results:
#     Get the title
        title = result.h3.text
        title = title.replace ("Enhanced","")
    
#Find the link and create url
        href = result.find('a')['href']
        base_url = "https://astrogeology.usgs.gov"
        image_link = base_url + href
    
#Loop through images
        browser.visit(image_link)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
    
# create image URLs
        downloads = soup.find('div', class_ = "downloads")
        image_url = downloads.find('a')['href']
    
#Create dictonary of hemispheres
        mars_dictionary.append({"title": title, "img_url": image_url})

    browser.quit()
    data = {"News_Header":news_title,"News_Article":news_p,"JPL_Image":featured_image_url,"Facts":html_table,"Hemispheres":mars_dictionary}

    return data