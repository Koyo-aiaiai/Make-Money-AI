import os

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_google_genai import ChatGoogleGenerativeAI


class LLMFactory:
    """
    Builds LLM stuff that are used in the conversation_agent.py

    Attributes:
    - model_mappings (dict[str, callable]): A dictionary mapping model names to function that build said class

    Methods:
    - create_model (str, **kwargs): Creates a model based on the model name and any additional keyword arguments.
    """

    @staticmethod
    def create_gemini(**kwargs) -> BaseChatModel:
        """
        Creates a Gemini model with the given keyword arguments. Defaults to using "gemini 2.5 flash lite" if no model is specified.

        Args:
        - **kwargs: Additional keyword arguments to pass to the Gemini model constructor.

        Returns:
        - BaseChatModel: An instance of the Gemini model.

        Raises:
        - ValueError: If the GOOGLE_API_KEY environment variable is not set.
        """
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("Tried to load Gemini model without GOOGLE_API_KEY set in environment variables.")
        model = kwargs.get("model", "gemini-2.5-flash-lite")
        
        config = {
            "model": model,
            "google_api_key": api_key,
            **kwargs
        }

        return ChatGoogleGenerativeAI(
                **config
            )

    MODEL_MAPPINGS = {
        "gemini": create_gemini
    }

    @classmethod
    def create_model(cls, model_name: str, **kwargs) -> BaseChatModel:
        """
        Creates a model based on the model name and any additional keyword arguments. This also is responsible for binding tools to the model.

        Args:
        - model_name (str): The name of the model to create.
        - **kwargs: Additional keyword arguments to pass to the model constructor.

        Returns:
        - BaseChatModel: An instance of the requested model.

        Raises:
        - ValueError: If the model name is not found in the model mappings.
        """
        model_name = model_name.lower()

        if model_name not in cls.MODEL_MAPPINGS:
            raise ValueError(f"Model {model_name} not found in model mappings.")
        
        return cls.MODEL_MAPPINGS[model_name](**kwargs)