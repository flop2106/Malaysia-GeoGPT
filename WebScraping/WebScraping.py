#import bs4
import requests
import xml.etree.ElementTree as ET
import sys
import os
from bs4 import BeautifulSoup

# Set the root directory as the working directory
root_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, root_directory)

from utils.LoggerBaseUtil import LoggerBaseUtil

logger = LoggerBaseUtil.get_logger()

class WebScraping:
    def __init__(self, url):
        pass
    @staticmethod
    def read_html(url:str) -> dict:
        """
        Reads the HTML content, parses using BS4 and create json of:
        Title, Keyword, Tag, Author, URL, Abstract
        """
        result = {}
        try:
            response = requests.get(url, verify=False)
            response.raise_for_status()
            
            root = ET.fromstring(response.content)
            id = 0
            for item in root.findall('./channel/item'):
                title = item.find('title').text
                link = item.find('link').text
                result[id] = {
                    "title": title,
                    "url": link
                    }
                id+=1
        except requests.exceptions.RequestException as e:
            logger.info(f"Error fetching RSS feed: {e}")
        except ET.ParseError:
            logger.info("Error Parsing the XML")
        
        return result

    @staticmethod
    def extract_html(list_of_url:dict):
        """
        Extract The HTML Result
        """
        for keys in list_of_url.keys():
            url = list_of_url[keys]["url"]
            response = requests.get(url, verify = False)
            if response.status_code == 200:
                try:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    page_title = soup.find('h1', class_='ep_tm_pagetitle').get_text(strip = True)
                    authors = []
                    for author in soup.find_all('span', class_='person_name'):
                        authors.append(author.get_text(strip = True))
                    author_names = ", ".join(authors)

                    abstract = soup.find('h2', text = 'Abstract').find_next('p').get_text(strip = True)

                    logger.info(f"Title: {page_title}")
                    logger.info(f"Authors: {author_names}")
                    logger.info(f"Abstract: {abstract}")
                    ###Add to create hash algorithms from the whole result to enable unique id and thus compare the data using hashing techniques
                    ###Add to directly post to kafka
                except Exception as e:
                    logger.error(f"Error for {keys}, {url}: {e}")

                

    def vector_search(self, embedding:list, query:str) -> list:
        """
        Perform vector search using the embedding and query
        """
        pass

if __name__=="__main__":
    logger.info("test")
    um_xml = r"https://eprints.um.edu.my/cgi/exportview/subjects/QE/RSS2/QE.xml"
    result = WebScraping.read_html(um_xml)
    #logger.info(result)
    WebScraping.extract_html(result)


