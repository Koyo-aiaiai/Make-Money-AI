from langchain_core.language_models.chat_models import BaseChatModel


class LLMFactory:
    """
    Builds LLM stuff that are used in the conversation_agent.py

    Attributes:
    - model_mappings (dict[str, callable]): A dictionary mapping model names to function that build said class

    Methods:
    - create_model (str, **kwargs): Creates a model based on the model name and any additional keyword arguments.
    """
    def __init__(self):
        self.model_mappings = {
            # TODO: this should have model names and also the function that builds the model
            "gemini": self.create_gemini,
        }

    def create_gemini(self, **kwargs) -> BaseChatModel:
        """
        Creates a Gemini model with the given keyword arguments.

        Args:
        - **kwargs: Additional keyword arguments to pass to the Gemini model constructor.

        Returns:
        - BaseChatModel: An instance of the Gemini model.
        """
        # TODO: implement this
        pass

    def create_model(self, model_name: str, **kwargs) -> BaseChatModel:
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

        if model_name not in self.model_mappings:
            raise ValueError(f"Model {model_name} not found in model mappings.")
        
        return self.model_mappings[model_name](**kwargs)