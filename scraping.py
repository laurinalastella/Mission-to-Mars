### Module 10
### 2022 August
### Laurina LaStella

# Import Splinter and BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import datetime as dt

# executable_path = {'executable_path': 'chromedriver.exe'}
# browser = Browser('chrome', **executable_path, headless=False)


# Set up Splinter
# 1. Initialize the browser.
# 2. Create a data dictionary.
# 3. End the WebDriver and return the scraped data.
def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    # print(executable_path)
    browser = Browser('chrome', **executable_path, headless=False)
    # executable_path = {'executable_path': 'chromedriver.exe'}
    # browser = Browser('chrome', **executable_path, headless=False)


# When headless=True:
# run in headless mode. All of the 
# scraping will still be accomplished, but behind the scenes.
    news_title, news_paragraph = mars_news(browser)
    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }

# Stop webdriver and return data
    browser.quit()
    return data
# Function end.



###### Scrape Mars News
# Function start:
def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # This line is missing in Mod 10.5.2 instructions.
        # slide_elem.find('div', class_='content_title')
        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # news_title
        # Mod 10/3/3
        # There are two methods used to find tags and attributes with BeautifulSoup:
        # .find() is used when we want only the first class and attribute we've specified.
        # .find_all() is used when we want to retrieve all of the tags and attributes.
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
        # news_p
    except AttributeError:
        return None, None

    return news_title, news_p
# Function end.


###### JPL Space Images Featured Image
# Function start:
def featured_image(browser):

    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        # img_url_rel
    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    # img_url

    return img_url
# Function end.



####### Mars Facts
# Function start:
def mars_facts():
    # By specifying an index of 0, we're telling Pandas to 
    # pull only the first table it encounters, 
    # or the first item in the list.
    # Add try/except for error handling
    try:
        # use 'read_html" to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)
    # df

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")
# Function end.

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())


######### VS Code won't run these files.
# Use the Anaconda Prompt terminal to run:
# python app.py
# python scraping.py
###### Also run:
# mongosh (not mongod like Mod says)

