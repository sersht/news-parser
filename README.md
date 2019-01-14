# News parser

The script for parsing UKR.NET and TSN.UA resources. Get news from main pages and categories.  

Demo is available [here](https://parser-news.herokuapp.com/). 

Last version (on GitHub) is adapted for Heroku platform, so have some limitations (see __Limitations__).  
__Examples of general versions can be found in commit history.__  

Sites parser automatically runs on schedule.  

_Get images_ button allows user to see images from news content.  
_Download image_ button is __implemented and not available in Demo__.

## How to use

Short instructions on _Help_ button.

## Limitations

* Due to the free hosting plan and high server load - sometimes queries may not respond.
* Manually restricted parser area because of holding a little amount of news in a database.

## Technologies

* Python 3.7.2  
* BeautifulSoup 4 (LXML parser) 
* Selenium (Chrome driver)  
* Flask
* PostgreSQL
