import requests
from bs4 import BeautifulSoup
from loguru import logger
from bs4 import ResultSet

st_accept = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"  # говорим веб-серверу,
# что хотим получить html
# имитируем подключение через браузер Mozilla на macOS
st_useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
# формируем хеш заголовков
headers = {
    "Accept": st_accept,
    "User-Agent": st_useragent,
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Encoding": "gzip, deflate"

}


class Parser:

    def __init__(self, link: str) -> None:
        self.link = link
        self.soup = self.set_soup()

    def set_soup(self) -> BeautifulSoup:
        try:
            req = requests.get(self.link, headers)
            return BeautifulSoup(req.text, features="html.parser")
        except Exception as ex:
            logger.exception(ex)

    def return_title(self) -> BeautifulSoup:
        try:
            return self.soup.title.string
        except Exception as ex:
            logger.exception(ex)

    def return_list_tags(self, tag) -> ResultSet:
        try:
            return self.soup.find_all(tag)
        except Exception as ex:
            logger.exception(ex)

