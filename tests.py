from llm_scraper._agent import template_replacer, OpenaiInterface, ScraperAgent
from unittest import TestCase, main
from unittest.mock import Mock, patch


class TestScraperAgent(TestCase):
    def test_setup_with_firefox(self):
        _ = ScraperAgent(browser="firefox")

    def test_setup_with_chrome(self):
        _ = ScraperAgent(browser="chrome")

    def test_assemble_user_message(self):
        agent = ScraperAgent(browser="firefox")

        template = "Hello {TEXT}, {QUESTION}"
        x, y = "Francesco", "how are you?"
        result = agent._assemble_user_message(template, x, y)
        expected = "Hello Francesco, how are you?"

        self.assertEqual(result, expected)

    @patch("selenium.webdriver.Firefox")
    def test_scrape_website(self, MockFirefox):
        agent = ScraperAgent(browser="firefox")

        mock_firefox_instance = Mock()
        MockFirefox.return_value = mock_firefox_instance
        mock_firefox_instance.find_element.return_value.text = "Sample Text"

        agent.scrape_website("my_url")

        self.assertEqual(agent._website_text, "Sample Text")


class TestTemplateReplacer(TestCase):
    def test_replaces_with_dictionary(self):
        self.assertEqual(
            template_replacer("Hello {name}", {"name": "John"}), "Hello John"
        )

    def test_leaves_unmatched_keys(self):
        self.assertEqual(template_replacer("Hello {name}", {}), "Hello {name}")


class TestOpenaiInterface(TestCase):
    @patch("openai.ChatCompletion.create")
    def test_completion(self, MockChatCompletionCreate):
        # mocking OpenaiInterface completion
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content="Test response"))]
        MockChatCompletionCreate.return_value = mock_response

        openai_if = OpenaiInterface()
        openai_if.add_user_message("Test user message")
        response = openai_if.completion()

        self.assertEqual(response, "Test response")


class TestScraperAgentIntegration:
    @patch("llm_scraper._openai.OpenaiInterface")
    @patch("llm_scraper._scraping.FirefoxScraper")
    def test_integration(self, MockFirefoxScraper, MockOpenaiInterface):
        # mocking FirefoxScraper
        firefox_scraper_instance = MockFirefoxScraper.return_value
        firefox_scraper_instance.get_text_from_html.return_value = "The text"

        # mocking OpenaiInterface
        openai_if_instance = MockOpenaiInterface.return_value
        openai_if_instance.completion.return_value = "My answer"

        # instantiate agent and scrape website
        agent = ScraperAgent(browser="firefox")
        website = "https://www.google.it"
        agent.scrape_website(website)

        # get answer
        question = "My question"
        answer = agent.answer(question)

        self.assertEqual(agent._website_text, "The text")
        self.assertEqual(answer, "My answer")


if __name__ == "__main__":
    main()
