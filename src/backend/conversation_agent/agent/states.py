from pydantic import BaseModel
from Typing import TypedDict


class UserPreferences(BaseModel):
    """
    Represents the LLM's understanding of the user's preferences.
    
    Attributes:
    - risk_tolerance (str): The user's risk tolerance level. (could be something like "low", "med", "high", or more quantitative such as actual standard deviation and such)
    - horizon (str): how long term the user is planning with their portfolio.
    - other (str): other preferences that the user has
    """
    risk_tolerance: str
    horizon: str
    other: str

class LLMResponse(BaseModel):
    """
    How the LLM's response should be formatted.

    Attributes:
    - message: str: The message from the LLM.
    """
    message: str

class ConversationState(TypedDict):
    """
    Represents the state of a conversation.
    
    Attributes:
    - conversation_id (str): The unique identifier for the conversation.
    - user_id (str): The unique identifier for the user.
    - messages (list[BaseChatMessage]): A list of messages exchanged in the conversation.
    """
    conversation_id: str
    user_id: str
    messages: list
    user_preferences: UserPreferences | None = None
    is_complete: bool | None = None