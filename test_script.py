from typing import Union

from WebScraping.UTPWebScrapper import UTPWebScrapper
from WebScraping.UMWebScrapper import UMWebScrapper
import utils.LoggerBaseUtil as LoggerBaseUtil
from Kafka.KafkaSetup import setup
from Kafka.KafkaPublisher import setupPublisher
from LLM.Chat import Chat
from LLM.Embedding import Embedding
from LLM.BaseLLM import BaseLLM
from Database.SqlLiteSetup import execute_sql
from LLM.VectorSearch import VectorSearch
import threading
logger = LoggerBaseUtil.setup()
logger.info("Start!")

def test_kafka():
    working_server = setup()
    kafkaPublisher = setupPublisher(list_server = [working_server])
    um_xml = r"https://eprints.um.edu.my/cgi/exportview/subjects/QE/RSS2/QE.xml"
    ums_xml = r"https://eprints.ums.edu.my/cgi/exportview/subjects/QE/RSS2/QE.xml"
    utm_xml = r"https://eprints.utm.my/cgi/exportview/subjects/QE/RSS2/QE.xml"
    utp_xml = r"https://utpedia.utp.edu.my/cgi/exportview/subjects/QE/RSS2/QE.xml"


    def scrapper(url , webscrapingConstructor: Union[UTPWebScrapper, UMWebScrapper]):
        list_of_url = webscrapingConstructor.read_html(url)
        webscrapingConstructor.extract_html(list_of_url, kafkaPublisher, "scraper","scraper")


    um_scrapper_thread = threading.Thread(
        target = scrapper,
        args = (um_xml, UMWebScrapper())
    )

    ums_scrapper_thread = threading.Thread(
        target = scrapper,
        args = (ums_xml, UMWebScrapper())
    )

    utm_scrapper_thread = threading.Thread(
        target = scrapper,
        args = (utm_xml, UMWebScrapper())
    )

    utp_scrapper_thread = threading.Thread(
        target = scrapper,
        args = (utp_xml, UTPWebScrapper())
    )

    um_scrapper_thread.start()
    ums_scrapper_thread.start()
    utm_scrapper_thread.start()
    utp_scrapper_thread.start()

    um_scrapper_thread.join()
    ums_scrapper_thread.join()
    utm_scrapper_thread.join()
    utp_scrapper_thread.join()

def test_LLM():
    test = Chat()
    print(test.execute("hello GPT"))
def test_embedding():
    test = Embedding()
    print(test.execute("Hello Vector!"))

def test_initial_pipeline():
    #test_kafka()
    embedding = Embedding()
    embedding.embedding_sequence()

def test_query():
    logger.info("Check listpaper")
    result_paper = execute_sql("SELECT COUNT(*) FROM listpaper")
    logger.info(result_paper[0][0])
    logger.info("Check embedding")
    result_embeddings = execute_sql("SELECT COUNT(*) FROM embeddings")
    logger.info(result_embeddings[0][0])
    assert result_paper == result_embeddings

def test_vector_search():
    logger.info("Start Vector Search")
    vector_search = VectorSearch()
    query = "Tell me the list of paper with balingian province chemistry and provide an overview on its geochemistry"
    result_list = vector_search.execute(query)
    logger.info(result_list)
    return result_list, query

def test_vector_search_and_summarize():
    result_list, query = test_vector_search()
    # prep the list into str
    result_str = ""
    for res in result_list:
        result_str = (result_str + "title: " + res[1] +
                      "author: " +  res[2] + "url: " + res[3]
                      + "abstract: " + res[4] +"\n"
        ) 
    prompt = f"Based on the following data: {result_str} + summarize and answer the following query from the user: {query}"
    role = """a geology data calatog experts for malaysia. 
                       ONLY USE THE DATA PROVIDED AND AVOID USE YOUR OWN KNOWLEDGE. 
                       ENSURE AT THE BOTTOM OF YOUR RESPONSE ADD THE TITLE AND URL THAT YOU USE FOR REFERENCE.
                       YOU ARE FOUND TO ALWAYS GET MIXED UP ON GEOGRAPHY LIKE SARAWAK IN PERAK. ENSURE YOU GOT THIS RIGHT WHEN GIVING ANSWER.
                       """
    chat = Chat()
    result = chat.execute(prompt, role)
    #interrogate
    print("\n" + result)
    print(chat.execute(str(input("Add your interrogation: ")), role, result))


test_query()    
#test_initial_pipeline()
test_vector_search_and_summarize()
#test_initial_pipeline()