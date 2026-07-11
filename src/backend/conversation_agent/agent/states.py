from langchain_core.messages import BaseMessage
from langgraph.graph import add_message
from pydantic import BaseModel, Field
from Typing import Annotated, TypedDict


class UserPreferencesState(BaseModel):
    """
    Data object for the representation of the AI agent's understanding of the user's preferences.
    """
    risk_tolerance: str = Field(description="The user's risk tolerance level. Could be something like 'low', 'med', 'high', or more quantitative such as actual standard deviation and such.")
    horizon: str = Field(description="The user's investment horizon. Could be something like 'short-term', 'medium-term', or 'long-term'.")
    other: str = Field(description="Any other preferences the user has.")

class LLMResponseState(BaseModel):
    """
    Data object for representing the response from the LLM to the user.
    """
    message: str = Field(description="The message from the LLM.")

class LLMFinishedExtractingState(BaseModel):
    """
    Data object for representing whether the LLM has finished extracting user preferences.
    """
    is_finished: bool = Field(description="Indicates whether the LLM has finished extracting user preferences.")

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
    messages: Annotated[list[BaseMessage], add_message]
    response: str | None = None
    user_preferences: UserPreferencesState | None = None
    is_complete: bool | None = None