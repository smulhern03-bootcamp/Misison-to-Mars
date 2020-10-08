# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt


def scrape_all():
    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "hemisphere": hemisphere_image_urls
    }

    # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one("ul.item_list li.slide")
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find("div", class_="content_title").get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find("div", class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


def featured_image(browser):
    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')[0]
    full_image_elem.click()

    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'

    return img_url

def mars_facts():
# 1. Use browser to visit the URL 
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    hemisphere_image_urls = []
#Cerberus
    browser.links.find_by_partial_text('Cerberus').click()
    html = browser.html
    cerberus_soup = soup(html, 'html.parser')
    cerberus_url = cerberus_soup.select_one('div.downloads a').get("href")
    cerberus_title = cerberus_soup.select_one('div.content h2').text
#dictionary:
    cerberus_dict = {
        "img_url": cerberus_url,
        "title": cerberus_title
    }
    hemisphere_image_urls.append(cerberus_dict)

#schiaparelli
    browser.visit(url)
    browser.links.find_by_partial_text('Schiaparelli').click()
    html = browser.html
    schiaparelli_soup = soup(html, 'html.parser')
    schiaparelli_url = schiaparelli_soup.select_one('div.downloads a').get("href")
    schiaparelli_title = schiaparelli_soup.select_one('div.content h2').text
#dictionary:
    schiaparelli_dict = {
        "img_url": schiaparelli_url,
        "title": schiaparelli_title
    }
    hemisphere_image_urls.append(schiaparelli_dict)

#syrtis
    browser.visit(url)
    browser.links.find_by_partial_text('Syrtis').click()
    html = browser.html
    syrtis_soup = soup(html, 'html.parser')
    syrtis_url = syrtis_soup.select_one('div.downloads a').get("href")
    syrtis_title = syrtis_soup.select_one('div.content h2').text
#dictionary:
    syrtis_dict = {
        "img_url": syrtis_url,
        "title": syrtis_title
    }
    hemisphere_image_urls.append(syrtis_dict)

#valles_marineris
    browser.visit(url)
    browser.links.find_by_partial_text('Valles Marineris').click()
    html = browser.html
    valles_marineris_soup = soup(html, 'html.parser')
    valles_marineris_url = valles_marineris_soup.select_one('div.downloads a').get("href")
    valles_marineris_title = valles_marineris_soup.select_one('div.content h2').text
#dictionary:
    valles_marineris_dict = {
        "img_url": valles_marineris_url,
        "title": valles_marineris_title
    }
    hemisphere_image_urls.append(valles_marineris_dict)

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())