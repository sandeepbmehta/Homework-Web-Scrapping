# Dependencies
from bs4 import BeautifulSoup
from splinter import Browser
import requests
import pymongo
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape_info():
    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    #print(soup.prettify())
    
    # NASA Mars News
    # Selecting the first title and paragraph from the site
    results = soup.find_all('div', class_="slide")
    #print(results)
    for result in results:
        news_title = result.find('div', class_="rollover_description_inner").text
        news_p = result.find('div', class_="content_title").a.text
        break

    #print(news_title)
    #print(news_p)

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    #print(soup.prettify())

    # select the first image and appending the image name to the actual URL link to obtain the complete URL of the image
    # JPL Mars Space Images - Featured Image
    results = soup.find_all('div', class_="carousel_items")
    #print(results)
    for result in results:
        featured_image_url = 'https://www.jpl.nasa.gov/'
        temp_style = result.article["style"]
        #print(temp_var)
        #print(temp_var.split("url('")[1].split("');")[0])
        featured_image_url = featured_image_url + temp_style.split("url('")[1].split("');")[0]
        break
    
    #print(featured_image_url)

    url = 'https://twitter.com/marswxreport?lang=en'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    #print(soup.prettify())

    # Selecting the first valid weather data
    # Mars Weather
    results = soup.find_all('div', class_="tweet")
    for result in results:
        if result["data-name"] == 'Mars Weather' and \
            result["data-screen-name"] == 'MarsWxReport':
            mars_weather = result.find('p').text
            position = mars_weather.find("InSight")
            if position == 0:
                mars_weather = mars_weather.split('pic.twitter')[0]
                break
    print(mars_weather)

    url = 'http://space-facts.com/mars/'
    tables = pd.read_html(url)

    # Mars Facts
    #df = tables[0]
    df = pd.DataFrame(tables[0])
    df.columns = ["Parameter", "Value"]
    df.set_index("Parameter", inplace=True)
    html_table_rep = df.to_html()
    html_table = html_table_rep

    browser = init_browser()
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Mars Hemispheres
    hemisphere_image_urls = []
    link = 'https://astrogeology.usgs.gov'
    items = soup.find_all('div', class_='item')
    #print(items)
    for item in items:
        diction = {}
        imgurl = item.a["href"]
        #print(imgurl)
        target_url = link + imgurl
        #print(target_url)
        desc = item.find('div', class_="description")
        description = desc.find('h3').text
        #print(description)
        diction.update(title = description)
    
        url1 = target_url
        response = requests.get(url1)
        #print(url1)
        soup1 = BeautifulSoup(response.text, 'lxml')
        imgs = soup1.find_all('div', class_='downloads')
        #print(imgs)
        for img in imgs:
            #print(img)
            full_img_url = img.find('a')["href"]
            #print(full_img_url)
            diction.update(img_url = full_img_url)
            break
    
        hemisphere_image_urls.append(diction)  

    #print(hemisphere_image_urls)
    browser.quit()

    mars_data = {
        "news_title" : news_title,
        "news_para" : news_p,
        "image_url":featured_image_url,
        "mars_weather":mars_weather,
        "table":html_table,
        "hemisphere_image_urls":hemisphere_image_urls
    }
    #print(mars_data["news_title"])
    #print(mars_data["news_para"])
    #print(mars_data["image_url"])
    #print(mars_data["mars_weather"])
    #print(mars_data["table"])
    #print(mars_data["hemisphere_image_urls"])
    # Return results
    return mars_data;