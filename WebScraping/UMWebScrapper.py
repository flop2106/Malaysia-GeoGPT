#import bs4
import requests
import xml.etree.ElementTree as ET
import time
from bs4 import BeautifulSoup
from Kafka.KafkaPublisher import setupPublisher, publish
from WebScraping.BaseWebScrapper import BaseWebScrapper

import utils.LoggerBaseUtil as LoggerBaseUtil

logger = LoggerBaseUtil.setup()

class UMWebScrapper(BaseWebScrapper):
    def __init__(self):
        pass
    def read_html(self, url:str) -> dict:
        """
        Reads the HTML content, parses using BS4 and create json of:
        Title, Keyword, Tag, Author, URL, Abstract
        """
        logger.info(f"Start Reading html: {url}")
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

    def extract_html(self, list_of_url:dict, kafkaPublisher: setupPublisher, topic: str, key: str):
        """
        Extract The HTML Result
        """
        for keys in list_of_url.keys():
            repeat = 0
            while repeat < 3:
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

                        publish(kafkaPublisher, topic, key, {"title":page_title, 
                                                        "authors": author_names,
                                                        "url": url,
                                                        "abstract":abstract})
                        repeat = 3
                        time.sleep(2)

                        ###Add to create hash algorithms from the whole result to enable unique id and thus compare the data using hashing techniques
                    except Exception as e:
                        logger.error(f"Error for {keys}, {url}: {e}")
                        repeat+=1

if __name__=="__main__":
    logger.info("test")
    um_xml = r"https://eprints.um.edu.my/cgi/exportview/subjects/QE/RSS2/QE.xml"
    result = BaseWebScrapper.read_html(um_xml)
    BaseWebScrapper.extract_html(result)


