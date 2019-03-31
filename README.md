# News parser

The script for parsing UKR.NET and TSN.UA resources. Get news from main pages and categories.  

Demo is available [here](https://parser-news.herokuapp.com/) __(currently disabled)__.

Last version (on GitHub) is adapted for Heroku platform, so have some limitations (see __Limitations__).  
__Examples of general versions can be found in commit history.__  

Sites parser automatically runs on schedule.  

_Get images_ button allows user to see images from news content.  
_Download image_ button is __implemented and not available in Demo__.

## How to use
### Demo 

Short instructions on _Help_ button.

### Local setup

Make sure that you installed all needed programming packages (including from `requirements.txt` and PostgreSQL).    

1. Clone the repository on your computer.  

2. In `helper.py` 

* add `from selenium.webdriver.firefox.options import Options`

* add `PATH_TO_GECKODRIVER = r"your_path_to_project\geckodriver.exe` - variable with path to your Firefox driver 

* change `PAUSE_TIME` to 2.   

* make `get_html()` function look like this:  

```python
# Headless version
options = Options()
options.set_headless(True)
browser = webdriver.Firefox(options=options, executable_path=PATH_TO_GECKODRIVER)

# Get html-code from url
browser.get(url)
if to_scroll: 
    scroll_down(browser)
html = browser.page_source

browser.quit()

return html
```   

3. In `db_interactor.py`
* remove `DATABASE_URL = os.environ['DATABASE_URL']`  

* change all `connection = psycopg2.connect(DATABASE_URL, sslmode='require')` occurences to:  
```python
connection = psycopg2.connect(
    user=DB_CONNECTION_CONFIG["user"],
    password=DB_CONNECTION_CONFIG["password"],
    host=DB_CONNECTION_CONFIG["host"],
    port=DB_CONNECTION_CONFIG["port"],
    database=DB_CONNECTION_CONFIG["db_name"])
```   

* at the top of the code add your database config (similar to this):
```python
DB_CONNECTION_CONFIG = {
    "user": "postgres",
    "password": "123456",
    "host": "127.0.0.1",
    "port": "5432",
    "db_name": "news"}
```   

4. If needed - remove `break` from `tsnua.py` and `ukrnet.py` in `get_news_from_categories` functions.  

5. Create script `your_name.py` in repository folder and run it:  

```python
# -*- coding: utf-8 -*-
import tsnua
import ukrnet

ukrnet.parse()
tsnua.parse()
```

## Limitations

Due to the free hosting plan and high server load - sometimes queries may not respond.  

Manually restricted parser area because of holding a little amount of news in a database.

## Technologies

* Python 3.7.2  
* BeautifulSoup 4 (LXML parser) 
* Selenium (Chrome driver)  
* Flask
* PostgreSQL
