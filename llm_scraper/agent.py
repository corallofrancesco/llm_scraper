import re
from .openai import OpenaiInterface
from .scraping import ChromeScraper, FirefoxScraper


DEFAULT_MODEL = "gpt-3.5-turbo"
USER_PROMPT_TEMPLATE = """Given the following text, please answer concisely to the question "{QUESTION}":\n\n{TEXT}"""
MAX_TOKENS = 100


def template_replacer(template, replace_dict):
    """Function to replace text between the braces in a text wrt a dict
    Args:
        template (str): text template with text to be replaced between braces
        replace_dict (dict): dict containing the text to replace for each brace
    """

    def replacer(match):
        # Extracts the text between the {braces}
        tag = match.group(1)
        # Replace with value from dict or keep original tag
        return replace_dict.get(tag, match.group(0))

    return re.sub(r"\{([^}]+)\}", replacer, template)


class ScraperAgent:
    """Agent capable of extracting text from a given website
    and answering questions based on the text rendered by the page html.
    """

    def __init__(self, browser: str) -> None:
        """Constructor for the ScraperAgent class
        Args:
            browser (str): browser to be used by selenium
        Attributes:
            _website_text (str): rendered text extracted from the html page
            _openai_if (OpenaiInterface): interface class to OpenAI API
        """
        self.browser = browser

        self._website_text: str = None
        self._openai_if = OpenaiInterface(max_tokens=MAX_TOKENS)

    def _assemble_user_message(self, template: str, text: str, question: str) -> str:
        """Uses template_replacer() to replace the placeholders in the template
        and assembles the final user message
        Args:
            website (str): website URL
        Returns:
            user_message (str): assembled user message
        """
        user_message = template_replacer(
            template=template, replace_dict={"TEXT": text, "QUESTION": question}
        )

        return user_message

    def scrape_website(self, website: str):
        """Scrapes the rendered text from the html page of a website
        Args:
            website (str): website URL
        """
        if not website:
            raise ValueError("Website URL cannot be empty.")

        # create scraper object
        if self.browser == "firefox":
            scraper = FirefoxScraper(website)
        elif self.browser == "chrome":
            scraper = ChromeScraper(website)
        else:
            raise NotImplementedError()

        # extract text from the scraped content
        website_text = scraper.get_text_from_html()

        self._website_text = website_text

    def answer(self, question: str) -> str:
        """Returns answers to the given question
        Args:
            question (str): question to answer
        Returns:
            bot_message (str): answer returned by the openAI model
        """

        # create the user message starting from the template
        user_message = self._assemble_user_message(
            USER_PROMPT_TEMPLATE, self._website_text, question
        )

        # set the user message
        self._openai_if.add_user_message(user_message)

        # request completion to OpenAI model
        bot_message = self._openai_if.completion()

        return bot_message
