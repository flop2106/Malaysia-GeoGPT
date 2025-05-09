import bs4
import requests

class WebScraping:
    def __init__(self, url):
        pass

    def read_html(self, url:str) -> dict:
        """
        Reads the HTML content, parses using BS4 and create json of:
        Title, Keyword, Tag, Author, URL, Abstract
        """
        pass

    def write_html(self, ):
        """
        Write the html content to database
        """
        pass

    def vector_search(self, embedding:list, query:str) -> list:
        """
        Perform vector search using the embedding and query
        """
        pass