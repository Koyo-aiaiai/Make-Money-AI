from conversation_agent.agent import prompts, states
from conversation_agent.agent.model_factory import LLMFactory
from conversation_agent.data import ConversationInput, ConversationOutput
from langchain_core.messages import HumanMessage
from langchain_core.runnables import Runnable
from langgraph import StateGraph
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.state import END, START, CompiledStateGraph


class ConversationModel:
    """
    Implementation of the actual AI for the conversation, uses langgraph. This kinda just is a wrapper over the langgraph StateGraph.
    The messages from the AI should all be JSON formatted. After every call of the AI stuff, we then run validation on it again.
    If any validation node returns false, then we return to that node and prompt the AI to try again or just to fix the formatting on their last message.

    Attributes:
    TODO: in the future it might be best to have multiple llms instead of just one.
    - llm (BaseChatModel): The language model used for generating responses.
    - graph (StateGraph): The state graph used to manage the conversation flow.

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
        self.graph = self._build_graph()

    def _build_graph(self) -> Runnable:
        """
        Builds the state graph for the conversation model.

        Returns:
        - CompiledStateGraph: The compiled state graph.
        """
        # TODO: this defaults to gemini
        self.llm = LLMFactory.create_model("gemini")
        
        builder = StateGraph(states.ConversationState)
        checkpointer = InMemorySaver()


        # Define the nodes in the graph
        builder.add_node("record_preferences", self.record_preferences)
        builder.add_node("generate_response", self.generate_response)
        builder.add_node("check_is_done", self.check_is_done)

        # Define the edges in the graph
        builder.add_edge(START, "record_preferences")
        builder.add_edge("record_preferences", "generate_response")
        builder.add_edge("generate_response", "check_is_done")
        builder.add_edge("check_is_done", END)

        graph = builder.compile(checkpointer=checkpointer)
        return graph

    def invoke(self, conversation_input: ConversationInput) -> ConversationOutput:

        user_message = HumanMessage(content=conversation_input.user_prompt)
        response = self.graph.invoke({"messages": [user_message]}, config = {
            "configurable": {
                "thread_id": conversation_input.conversation_id,
                }
        })
        output = ConversationOutput(user_preferences=response["user_preferences"])
        return output


    ###################################
    # EVEYRTHING DOWN HERE ARE NODES  #
    ###################################
    def record_preferences(self, state: states.ConversationState) -> states.ConversationState:
        pass

    def generate_response(self, state: states.ConversationState) -> states.ConversationState:
        pass

    def check_is_done(self, state: states.ConversationState) -> states.ConversationState:
        pass

