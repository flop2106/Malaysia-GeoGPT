from typing import Union

from WebScraping.UTPWebScrapper import UTPWebScrapper
from WebScraping.UMWebScrapper import UMWebScrapper
import utils.LoggerBaseUtil as LoggerBaseUtil
from Kafka.KafkaSetup import setup
from Kafka.KafkaPublisher import setupPublisher
from LLM.Chat import Chat
from LLM.Embedding import Embedding
from LLM.BaseLLM import BaseLLM
import threading
logger = LoggerBaseUtil.setup()
logger.info("Start!")

def test_kafka():
    working_server = setup()
    kafkaPublisher = setupPublisher(list_server = [working_server])
    um_xml = r"https://eprints.um.edu.my/cgi/exportview/subjects/QE/RSS2/QE.xml"
    utp_xml = r"https://utpedia.utp.edu.my/cgi/exportview/subjects/QE/RSS2/QE.xml"


    def scrapper(url , webscrapingConstructor: Union[UTPWebScrapper, UMWebScrapper]):
        list_of_url = webscrapingConstructor.read_html(url)
        webscrapingConstructor.extract_html(list_of_url, kafkaPublisher, "scraper","scraper")


    um_scrapper_thread = threading.Thread(
        target = scrapper,
        args = (um_xml, UMWebScrapper())
    )
    utp_scrapper_thread = threading.Thread(
        target = scrapper,
        args = (utp_xml, UTPWebScrapper())
    )

    um_scrapper_thread.start() 

    utp_scrapper_thread.start()

    um_scrapper_thread.join()
    utp_scrapper_thread.join()

def test_LLM():
    test = Chat()
    print(test.execute("hello GPT"))
def test_embedding():
    test = Embedding()
    print(test.execute("Hello Vector!"))
#test_LLM()
test_embedding()