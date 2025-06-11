#import bs4
import requests
import xml.etree.ElementTree as ET
import time
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
from Kafka.KafkaPublisher import setupPublisher, publish

import utils.LoggerBaseUtil as LoggerBaseUtil

logger = LoggerBaseUtil.setup()

class BaseWebScrapper(ABC):
    def __init__(self):
        pass
    @abstractmethod
    def read_html(url:str) -> dict:
        pass

    @abstractmethod
    def extract_html(self, list_of_url:dict, kafkaPublisher: setupPublisher, topic: str, key: str):
        """
        Extract The HTML Result
        """

if __name__=="__main__":
    logger.info("test")
    

