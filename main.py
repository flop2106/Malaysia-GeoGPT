from WebScraping.WebScraping import WebScraping
from utils.LoggerBaseUtil import LoggerBaseUtil

logger = LoggerBaseUtil.get_logger()

um_xml = r"https://eprints.um.edu.my/cgi/exportview/subjects/QE/RSS2/QE.xml"
result = WebScraping.read_html(um_xml)