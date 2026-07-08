from pydantic import BaseModel


class ConversationInput(BaseModel):
    # TODO: work out what should be in this class
    user_prompt: str
    conversation_id: str
    user_id: str
    version: str = "0.1.0"

class ConversationOutput(BaseModel):
    # TODO: idk what goes in here
    pass