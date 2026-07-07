from pydantic import BaseModel


class ConversationInput(BaseModel):
    user_prompt: str


class ConversationOutput(BaseModel):
    ai_response: str