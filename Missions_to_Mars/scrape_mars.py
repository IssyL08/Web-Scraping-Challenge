# Declare Dependencies 
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import os
import time
import requests
import warnings
warnings.filterwarnings('ignore')

def init_browser():
    # @NOTE: Path to my chromedriver
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

# Create Mission to Mars global dictionary that can be imported into Mongo
mars_info = {}

# NASA MARS NEWS
def scrape_mars_news():

        # Initialize browser 
        browser = init_browser()

        #browser.is_element_present_by_css("div.content_title", wait_time=1)

        # Visit Nasa news url through splinter module
        url = 'https://redplanetscience.com/'
        browser.visit(url)

        # HTML Object
        html = browser.html

        # Parse HTML with Beautiful Soup
        soup = bs(html, 'html.parser')

        # Retrieve the latest element that contains news title and news_paragraph
        news_title = soup.find('div', class_='content_title').text
        news_p = soup.find('div', class_='article_teaser_body').text

        # Dictionary entry from MARS NEWS
        mars_info['news_title'] = news_title
        mars_info['news_paragraph'] = news_p

        return mars_info

   

# FEATURED IMAGE
def scrape_mars_image():

        # Initialize browser 
        browser = init_browser()

        #browser.is_element_present_by_css("img.jpg", wait_time=1)

        # Visit Mars Space Images through splinter module
        featured_image_url= 'https://spaceimages-mars.com'
        browser.visit(featured_image_url)# Visit Mars Space Images through splinter module

        # HTML Object 
        html_image = browser.html

        # Parse HTML with Beautiful Soup
        soup = bs(html_image, 'html.parser')

        image_url = soup.find('img', class_='headerimage fade-in').get('src')

        image_url = f"https://spaceimages-mars.com/{image_url}"
        
        # Display full link to featured image
        image_url

        # Dictionary entry from FEATURED IMAGE
        mars_info['image_url'] = image_url
        

        return mars_info

           
# Mars Facts
def scrape_mars_facts():

        # Initialize browser 
        browser = init_browser()

         # Visit Mars facts url 
        url = 'https://galaxyfacts-mars.com'
        browser.visit(url)

        # Use Pandas to "read_html" to parse the URL
        tables = pd.read_html(url)
        #Find Mars Facts DataFrame in the lists of DataFrames
        df = tables[1]
        #Assign the columns
        df.columns = ['Description', 'Value']
        html_table = df.to_html(table_id="html_tbl_css",justify='left',index=False)

        # Dictionary entry from Mars Facts

        mars_info['tables'] = html_table

        return mars_info

# Mars Hemisphere

def scrape_mars_hemispheres():

        # Initialize browser 
        browser = init_browser()

        # Visit hemispheres website through splinter module 
        hemispheres_url = 'https://marshemispheres.com/'
        browser.visit(hemispheres_url)

        # HTML Object
        html_hemispheres = browser.html

        # Parse HTML with Beautiful Soup
        soup = bs(html_hemispheres, 'html.parser')

        # Retreive all items that contain mars hemispheres information
        items = soup.find_all('div', class_='item')

        # Create empty list for hemisphere urls 
        hiu = []

        # Store the main_ul 
        hemispheres_main_url = 'https://marshemispheres.com/' 

        # Loop through the items previously stored
        for i in items: 
            # Store title
            title = i.find('h3').text
            
            # Store link that leads to full image website
            partial_img_url = i.find('a', class_='itemLink product-item')['href']
            
            # Visit the link that contains the full image website 
            browser.visit(hemispheres_main_url + partial_img_url)
            
            # HTML Object of individual hemisphere information website 
            partial_img_html = browser.html
            
            # Parse HTML with Beautiful Soup for every individual hemisphere information website 
            soup = bs( partial_img_html, 'html.parser')
            
            # Retrieve full image source 
            img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
            
            # Append the retreived information into a list of dictionaries 
            hiu.append({"title" : title, "img_url" : img_url})

        mars_info['hiu'] = hiu
        
       
        browser.quit()

        # Return mars_data dictionary 

        return mars_info