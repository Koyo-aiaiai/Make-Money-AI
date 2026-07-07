from fastapi import APIRouter

from api.data import ConversationInput, ConversationOutput

router = APIRouter(
    prefix="/conversation_agent",
    tags=["Conversation Agent"]
)

@router.post("/{conversation_id}", response_model=ConversationOutput)
async def invoke(conversation_id: str, conversation_input: ConversationInput):
    """
    Posts user's prompt to AI conversation agnet. Then gets the response from the AI agent.
    """
    raise NotImplementedError("This endpoint is not implemented yet.")


# TODO: This is not supported right now, later when we implement the ability for there to be multiple conversations, we will implement this endpoint <3
@router.get("/{conversation_id}", response_model=ConversationOutput)
async def get_conversation(conversation_id: str):
    """
    Gets the conversation history for a given conversation ID.
    """
    raise NotImplementedError("This endpoint is not implemented yet.")