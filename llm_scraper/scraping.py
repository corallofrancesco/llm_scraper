from selenium import webdriver
from selenium.webdriver.common.by import By


class Scraper:
    """Class to scrape websites with the Selenium library"""

    def __init__(self, website: str) -> None:
        """Constructor for the Scraper class
        Args:
            website (str): website to scrape
        Attributes:
            _driver (selenium.webdriver): browser driver
        """
        self.website: str = website
        self._driver: webdriver = None

    def set_website(self):
        """set in the driver the website to scrape"""
        # TODO Timeout
        self._driver.get(self.website)

    def get_text_from_html(self) -> str:
        """extract text from the html section"""
        # extract text rendered by the html page
        html = self._driver.find_element(By.CSS_SELECTOR, "html")

        return html.text


class FirefoxScraper(Scraper):
    """Class to scrape websites with the Selenium using Firefox driver, in "headless" mode
    Args:
        website (str): website to scrape
    Attributes:
        _driver (selenium.webdriver): browser driver
    """

    def __init__(self, website: str) -> None:
        super().__init__(website)

        # select Firefox driver with headless option
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        self._driver = webdriver.Firefox(options=options)

        # set website to scrape in the driver
        self.set_website()


class ChromeScraper(Scraper):
    """Class to scrape websites with the Selenium using Chrome driver
    Args:
        website (str): website to scrape
    Attributes:
        _driver (selenium.webdriver): browser driver
        options (selenium.webdriver.FirefoxOptions): driver options
    """

    def __init__(self, website: str) -> None:
        super().__init__(website)

        # select Chrome driver
        self._driver = webdriver.Chrome()

        # set website to scrape in the driver
        self.set_website()
