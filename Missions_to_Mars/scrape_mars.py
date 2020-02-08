#dependencies
import pandas as pd
import requests
from selenium import webdriver
from splinter import Browser
from bs4 import BeautifulSoup
import time
import os


def scrape ():
    mars_dict = {}

    #NASA Mars News
    executable_path = {'executable_path':'/Users/yanellynunez/Desktop/web-scraping-challenge/Missions_to_Mars/chromedriver'}
    browser = Browser('chrome', **executable_path, headless = False)

    news_url = 'https://mars.nasa.gov/news'
    browser.visit(news_url)
    html = browser.html

    soup = BeautifulSoup(browser.html, 'html.parser')

    news_title = soup.find("div",class_="content_title").text
    print(news_title)

    news_p = soup.find("div", class_="rollover_description_inner").text
    print(news_p)

    mars_dict['news_title'] = news_title
    mars_dict['news_p'] = news_p


    # JPL Mars Space Images - Featured Image
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)
    html = browser.html

    soup = BeautifulSoup(browser.html, 'html.parser')

    image = soup.find("img", class_="thumb")["src"]
    featured_image_url = "https://www.jpl.nasa.gov" + image
    print(featured_image_url)

    mars_dict['featured_image_url'] = featured_image_url


    # Mars Weather
    twitter_url = "https://twitter.com/marswxreport?lang=en"
    url_response = requests.get(twitter_url)
    soup = BeautifulSoup(url_response.text, 'html.parser')
    url_result = soup.find('div', class_='js-tweet-text-container')
    #print(url_result)

    mars_weather = url_result.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    print(mars_weather)

    mars_dict['mars_weather'] = mars_weather


    # Mars Facts
    facts_url = 'https://space-facts.com/mars/'
    facts_table = pd.read_html(facts_url)
    facts_table

    facts_df = facts_table[0]
    facts_df.columns = ['Description', 'Value']
    facts_df.head()

    facts_df.set_index('Description', inplace=True)
    facts_df.head()

    mars_facts = facts_df.to_html()
    mars_facts.replace("\n", "")
    facts_df.to_html('mars_facts.html')

    mars_dict['mars_facts'] = mars_facts


    # Mars Hemispheres
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    html = browser.html

    soup = BeautifulSoup(html, 'html.parser')

    base_url ="https://astrogeology.usgs.gov"
    hemispheres_list = soup.find_all('div', class_='item')

    hemispheres_img_urls = []

    for hemispheres in hemispheres_list:
        hemispheres_dict = {}
    
        href = hemispheres.find('a', class_='itemLink product-item')
        link = base_url + href['href']
        browser.visit(link)
    
        time.sleep(1)
    
        hemispheres_html2 = browser.html
        hemispheres_soup2 = BeautifulSoup(hemispheres_html2, 'html.parser')
    
        images_title = hemispheres_soup2.find('div', class_='content').find('h2', class_='title').text
        hemispheres_dict['title'] = images_title
    
        images_url = hemispheres_soup2.find('div', class_='downloads').find('a')['href']
        hemispheres_dict['url_img'] = images_url
    
        hemispheres_img_urls.append(hemispheres_dict)
      
    hemispheres_img_urls

    mars_dict['hemispheres_img_urls'] = hemispheres_img_urls

    return mars_dict




