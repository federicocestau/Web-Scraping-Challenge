import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import re
def scrape():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    ##Visit The NASA Mars news site

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    browser.is_element_present_by_css('ul.item_list li.slide')

    html = browser.html

    news_soup = bs(html, 'html.parser')
    slide_elem = news_soup.select_one('ul.item_list li.slide')
    slide_elem.find('div',class_='content_title')

    news_title = slide_elem.find('div',class_='content_title').get_text()
    news_title

    news_p = slide_elem.find('div',class_='article_teaser_body').get_text()
    news_p

    ##JPL Mars Space Images - Featured Image

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.find_link_by_partial_text('more info')
    more_info_elem.click()

    html = browser.html
    img_soup = bs(html, 'html.parser')

    img_url_rel = img_soup.select_one('figure.lede a img').get('src')
    img_url_rel

    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    img_url

    ##Mars Weather

    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)

    time.sleep(5)

    html = browser.html
    weather_soup = bs(html, 'html.parser')

    
    pattern = re.compile(r'sol')
    mars_weather = weather_soup.find('span',text=pattern).text
    mars_weather

    ##Mars Hemispheres

    url ='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    hemisphere_image_urls = []
    links = browser.find_by_css('a.product-item h3')

    for i in range(len(links)):
        hemisphere = {}
        
        browser.find_by_css('a.product-item h3')[i].click()
        sample_elem = browser.find_link_by_text('Sample').first
        hemisphere['img_url'] = sample_elem['href']
        
        hemisphere['title'] = browser.find_by_css('h2.title').text
        
        hemisphere_image_urls.append(hemisphere)
        
        browser.back()

        hemisphere_image_urls
    url="https://space-facts.com/mars/"

    tables = pd.read_html(url)
    #this is a dataframe. Tables is a list
    df = tables[0]
    df.columns = ['Paramters','Data']
    #html table file
    tabledata=df.to_html()

    tabledata.replace('\n', '')

    Results={"news_paragraph":news_p, 
    "news_title":news_title,
    "img_url":img_url,
    "mars_weather":mars_weather,
    "hemisphere":hemisphere_image_urls,
    "Tabledata":tabledata}

    return Results