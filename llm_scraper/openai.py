from dotenv import load_dotenv
import openai
import os


SYSTEM_MESSAGE = ""


class OpenaiInterface:
    """Interface with OpenAI APIs"""

    def __init__(self, model_id="gpt-3.5-turbo", max_tokens=100, temperature=0) -> None:
        """Constructor for the OpenaiInterface class
        Args:
            model_id (str): which openai model to use. Defaults to "gpt-3.5-turbo"
                See https://platform.openai.com/docs/models/gpt-base for avail models
            max_tokens (int): max number of tokens to generate for each bot answer
                See https://platform.openai.com/docs/models/gpt-base for avail models
            temperature (float): temperature of the model from 0 to 1, where 0 is most
                factual and 1 is most creative
        Attributes:
            messages (dict): contains the chat messages between user and bot

        """
        self.model_id: str = model_id
        self.max_tokens: int = max_tokens
        self.temperature: float = temperature
        self.messages: list = [{"role": "system", "content": SYSTEM_MESSAGE}]

        self._load_api_key()

    def _load_api_key(self):
        """Loads the .env variables and then loads the OpenAI api key"""
        # load the .env variables
        load_dotenv()
        api_key = os.getenv("OPENAI_KEY")
        if not api_key:
            raise EnvironmentError("API Key for OpenAI not found")

        # set the api key in the openai library
        openai.api_key = api_key

    def add_user_message(self, user_message: str):
        """Appends a user message to the chat"""
        self.messages.append({"role": "user", "content": user_message})

    def completion(self):
        """Requests completion to openai model and parses the response
        Returns:
            bot_message (str): bot text message
            The bot responses basing on the current chat
        """
        # TODO rate limiter
        # create a chat completion request to openai
        response = openai.ChatCompletion.create(
            model=self.model_id,
            messages=self.messages,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
        )

        # Retrieve the answer from the model
        bot_message = response.choices[0].message.content

        # append the bot message to the existing chat
        self.messages.append({"role": "assistant", "content": bot_message})

        return bot_message
