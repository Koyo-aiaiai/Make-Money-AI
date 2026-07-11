from pydantic import BaseModel


class UserPreferences(BaseModel):
    """
    Represents the LLM's understanding of the user's preferences. Exact same as user preferences state which is used internally in the graph.
    
    Attributes:
    - risk_tolerance (str): The user's risk tolerance level. (could be something like "low", "med", "high", or more quantitative such as actual standard deviation and such)
    - horizon (str): how long term the user is planning with their portfolio.
    - other (str): other preferences that the user has
    """
    risk_tolerance: str
    horizon: str
    other: str

class ConversationInput(BaseModel):
    # TODO: work out what should be in this class
    user_prompt: str
    conversation_id: str
    user_id: str
    version: str = "0.1.0"

class ConversationOutput(BaseModel):
    """
    Output event from the conversation module.
    """
    user_preferences: UserPreferences