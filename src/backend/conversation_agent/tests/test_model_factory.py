# Tests for model factory
# 1. For each different type of chat model that model factory can output, just make sure that it can in fact intialize it (might need a lot of API keys)
# a. Gemini
# 2. Making sure that the model factory can handle invalid model names and raises the appropriate error
import pytest
from conversation_agent.agent.model_factory import LLMFactory
from langchain_core.language_models.chat_models import BaseChatModel


def test_model_factory_initialize_gemini_smoke():
    factory = LLMFactory()
    model = factory.create_model("gemini")
    assert isinstance(model, BaseChatModel)

def test_model_factory_invalid_model_name_raises_value_error():
    factory = LLMFactory()
    with pytest.raises(ValueError):
        factory.create_model("invalid_model_name")