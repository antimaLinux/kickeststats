from splinter import Browser
from splinter.driver.webdriver.chrome import WebDriver as ChromeWebDriver  # type: ignore
from splinter.driver.webdriver import WebDriverElement  # type: ignore
from typing import List
import time

from kickeststats.helpers.parsers import HeaderParser, RowParser, PaginationParser
from kickeststats.constants import KICKEST_URL, CHROMEDRIVER_EXECUTABLE_PATH
from loguru import logger


class TableHeader:

    xpath = '//*[@id="statsTableTHead"]/tr'

    def __init__(self, browser: ChromeWebDriver):
        self._data = self.find_data(browser)

    def find_data(self, browser: ChromeWebDriver) -> str:
        return browser.find_by_xpath(self.xpath).first.html

    @property
    def data(self) -> List[str]:
        parser = HeaderParser()
        parser.feed(self._data)
        return parser.out()

    @classmethod
    def from_browser(cls, browser: ChromeWebDriver) -> List[str]:
        return cls(browser).data


class TableData:

    xpath = '//*[@id="statsTableTBody"]'

    def __init__(self, browser: ChromeWebDriver, header: List[str]):
        self._data = self.find_data(browser)
        self._header = header

    def find_data(self, browser: ChromeWebDriver) -> str:
        return browser.find_by_xpath(self.xpath).first.html

    @property
    def data(self) -> List[dict]:
        parser = RowParser()
        parser.feed(self._data)
        return parser.out(self._header)

    @classmethod
    def from_browser(cls, browser: ChromeWebDriver, header: List[str]) -> List[dict]:
        return cls(browser, header).data


class Pagination:

    xpath = '//*[@id="statsTablePagination"]/div/div'

    def __init__(self, browser: ChromeWebDriver):
        self._data = self.find_data(browser)

    def find_data(self, browser: ChromeWebDriver) -> str:
        return browser.find_by_xpath(self.xpath).first.html

    @property
    def data(self) -> range:
        parser = PaginationParser()
        parser.feed(self._data)
        return parser.out()

    @classmethod
    def from_browser(cls, browser: ChromeWebDriver) -> range:
        return cls(browser).data


class NextPage:

    xpath = '//*[@id="statsTablePagination"]/div/div/ul/li[{}]/a'

    def __init__(self, browser: ChromeWebDriver):
        self._next = self.find_data(browser)

    def find_data(self, browser: ChromeWebDriver) -> WebDriverElement:
        parser = PaginationParser()
        parser.feed(browser.find_by_xpath(Pagination.xpath).first.html)
        index = len(parser.data)
        return browser.find_by_xpath(self.xpath.format(index)).first

    def visit(self):
        self._next.click()


def download_data() -> List[dict]:

    with Browser(
        driver_name="chrome", executable_path=CHROMEDRIVER_EXECUTABLE_PATH
    ) as browser:
        players_data = []
        browser.visit(KICKEST_URL)
        # required sleep due to interaction with webdriver
        time.sleep(2)
        pagination = Pagination.from_browser(browser)
        header = TableHeader.from_browser(browser)
        for current_page in pagination:
            logger.info(f"Parsing page {current_page} of {pagination[-1]}")
            data = TableData.from_browser(browser, header)
            players_data.extend(data)
            NextPage(browser).visit()
            # required sleep due to interaction with webdriver
            time.sleep(1)

        return players_data


if __name__ == "__main__":
    download_data()
