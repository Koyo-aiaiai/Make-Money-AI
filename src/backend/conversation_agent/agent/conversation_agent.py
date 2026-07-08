from conversation_agent.agent import states
from conversation_agent.data import ConversationInput, ConversationOutput
from langgraph import StateGraph


class ConversationModel:
    """
    Implementation of the actual AI for the conversation, uses langgraph. This kinda just is a wrapper over the langgraph StateGraph.
    The messages from the AI should all be JSON formatted. After every call of the AI stuff, we then run validation on it again.
    If any validation node returns false, then we return to that node and prompt the AI to try again or just to fix the formatting on their last message.

    Attributes:
    - llm (BaseChatModel): The language model used for generating responses.
    - graph (StateGraph): The state graph used to manage the conversation flow.
    - short_term_checkpointer (BaseCheckpointSaver): The checkpointer used to manage short-term memory.

    Nodes:
    - START
    - record_preferences: this extracts the user's preferences from their prompt and stores it in the output object
    - generate_response: this generates a response based on the user's prompt and the recorded preferences. Asks user for further preferences and stuff.
    - check_is_done: check if the we have extracted enough information about the user's preferences for their portfolio to continue onto building it
    - END

    Methods:
    - _build_graph (): builds the state graph for the conversation model
    - invoke (ConversationInput) -> ConversationOutput: takes in the user prompt and returns the response
    """
    def __init__(self):
        pass

    def _build_graph(self):
        pass

    def invoke(self, conversation_input: ConversationInput) -> ConversationOutput:
        pass

    ###################################
    # EVEYRTHING DOWN HERE ARE NODES  #
    ###################################
    def record_preferences(self, state: states.ConversationState) -> states.ConversationState:
        pass

    def generate_response(self, state: states.ConversationState) -> states.ConversationState:
        pass

    def check_is_done(self, state: states.ConversationState) -> states.ConversationState:
        pass

