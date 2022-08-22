# Mission_to_Mars
## Overview:
We created a web page that shares the top Mars news article and a daily Mars featured image. The web page also contains a facts table about Mars, and images of the four hemispheres of Mars. The following tools were used in the creation of the web page.
- Flask was used to generate the web page
- Splinter was used for the automated web-scraping which supplies the most up-to-date Mars news article title and summary paragraph, and daily Mars featured image. Splinter was also used to supply the Mars facts table, as well as the Mars hemispheres images.
    - Websites that were used in the web-scraping process:
        - https://redplanetscience.com/
        - https://spaceimages-mars.com/
        - https://galaxyfacts-mars.com/
        - https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars
- Beautiful Soup object to parse the html information from the scraped websites.
- ChromeDriverManager- driver object for Chrome
- Jupyter notebook for testing the web-scraping code before exporting as a python file.
- Python to make the web-scraping code work in conjunction with an html file and the flask app file.
- MongoDB to store the scraped data that appears on the web page. 