from pydantic import BaseModel
from Typing import TypedDict


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