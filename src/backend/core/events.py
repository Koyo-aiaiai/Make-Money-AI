from pydantic import BaseModel


class UserConversastionInputEvent(BaseModel):
    user_prompt: str
    conversation_id: str
    user_id: str
    version: str = "0.1.0"

class UserConversastionOutputEvent(BaseModel):
    ai_response: str
    conversation_id: str
    user_id: str
    version: str = "0.1.0"