#Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
    #Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    #Run all scraping functions and store results in dictionary
    data = {"news_title": news_title,
            "news_paragraph": news_paragraph,
            "featured_image": featured_image(browser),
            "facts": mars_facts(),
            "hemisphere_images": mars_hemispheres(browser), 
            "last_modified": dt.datetime.now()
    }

    #Stop webdriver and return data
    browser.quit()

    return data

def mars_news(browser):
    #Scrape Mars News
    #Set up url variable to visit the 'NASA Mars News' website
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    #Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    #Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup =soup(html, 'html.parser')

    #Add try_except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        #Use the parent element to find the first 'a' tag and save it as 'news_title' 
        news_title = slide_elem.find('div', class_='content_title').get_text()
        #Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p

def featured_image(browser):
    # ### Featured Images
    #Visit new url to be scraped
    url='https://spaceimages-mars.com/'
    browser.visit(url)

    #Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    #Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    #Add try/except for error handling
    try:
        #Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        
    except AttributeError:
        return None
    
    #Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url

# ### Mars Facts
def mars_facts():
    try:
        #use 'read_html' to scrape the facts tble into a dataframe
        mars_facts_df = pd.read_html('https://galaxyfacts-mars.com/')[0]
    except BaseException:
        return None
    
    #Assign columns and set index of dataframe
    mars_facts_df.columns=['Description', 'Mars', 'Earth']
    mars_facts_df.set_index('Description', inplace=True)
    
    #Convert dataframe to HTML format, add bootstrap
    return mars_facts_df.to_html(classes="table table-striped")

# ### Mars Hemispheres
def mars_hemispheres(browser):
    #Visit new url to be scraped
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    #Parsing the resulting html with soup
    html = browser.html
    mars_hemispheres_soup = soup(html, 'html.parser')

    try:
        url_to_full_img = []
        items = mars_hemispheres_soup.find_all('div', class_="item")
        for item in items:
            url_to_full_img.append(item.a.get('href'))
    except AttributeError:
        return None

    try:
        hemisphere_image_urls = []

        for mars_hemisphere_url in url_to_full_img:
            browser.visit(f'{url}{mars_hemisphere_url}')
            html= browser.html
            current_hemisphere_soup = soup(html, 'html.parser')
            download_box = current_hemisphere_soup.find('div', class_="downloads")
            hemisphere_rel_url = download_box.find('a').get('href')
            full_img_url =f'{url}{hemisphere_rel_url}'
            title = current_hemisphere_soup.find('h2', class_='title')
            hemisphere_image_urls.append({"img_url":full_img_url,"title":title.text})
    except AttributeError:
        return None

    return hemisphere_image_urls

if __name__ == "__main__":
    #If running as script, print scraped data
    print(scrape_all())