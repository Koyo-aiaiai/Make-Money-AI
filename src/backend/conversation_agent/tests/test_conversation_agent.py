# Tests for the conversation agent
# 1. test each node individually and make sure the output is as expected
# a. record_preferences: records the user preferences in the conversation state. User another LLM to judge whether this is related. That llm then outputs some sort of pass/fail boolean score.
# b. generate_response: generates a response, trying to reflect its understanding of the user's preferences and asking for more information that might be needed in building a finance portfolio. Again use LLM as a judge for whether or not this works as intended.
# c. check_is_done: checks if the conversation is complete. Just looking at if the output can be parsed into boolean
# 2. Try invoking the graph as a whole and ensuring that key fields are in fact filled out
# NOTE: ideally for testing this conversation agent, we run the conversation agent on a whole test set of potential user prompts and conversations. Then we pass these through LLM as a judge to see how accurate our model is. The code in this file is largely just a smoke test to make sure things are at least moderately coherent in the conversation.
import os

import pytest
from conversation_agent.agent.conversation_agent import ConversationModel
from convesation_agent.agent.states import ConversationState
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def llm_judge(prompt: str) -> bool:
    """
    LLM as a judge for whether or not the output from different nodes in the conversation agent is relevant.
    """
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    response = response.output[0].content[0].text
    response = response.strip().lower()
    if "true" in response:
        return True
    elif "false" in response:
        return False
    else:
        raise ValueError("LLM judge did not return a valid boolean response.")


@pytest.fixture(scope="module")
def setup():
    model = ConversationModel()
    return model

def test_record_preferences_returns_relevant_preferences_from_user(setup):
    model = setup
    state = ConversationState(
        conversation_id="test_conversation",
        user_id="test_user",
        messages=[{"role": "user", "content": "I want to invest in a low-risk portfolio with a long-term horizon."}],
        user_preferences="",
        is_complete=None
    )
    updated_state = model.record_preferences(state)
    judge_model_prompt = f"""You are to judge whether or not the user's preferences are adequately stored in the following output from an AI.
    Here is the original user message: 'I want to invest in a low-risk portfolio with a long-term horizon.' Here is the output from the AI: '{updated_state.user_preferences}'. Please respond with 'True' if the outpu  is relevant and captures the user's preferences, or 'False' if it does not."""
    assert llm_judge(judge_model_prompt) is True

def test_generate_response_returns_relevant_response(setup):
    model = setup
    state = ConversationState(
        conversation_id="test_conversation",
        user_id="test_user",
        messages=[{"role": "user", "content": "I want to invest in a low-risk portfolio with a long-term horizon."}],
        user_preferences="risk_tolerance: low, horizon: long-term",
        is_complete=None
    )
    updated_state = model.generate_response(state)
    judge_model_prompt = f"""You are to judge whether or not the AI's response is relevant and reflects its understanding of the user's preferences.
    Here is the original user message: 'I want to invest in a low-risk portfolio with a long-term horizon.' Here is the output from the AI: '{updated_state.messages[-1]['content']}'. Please respond with 'True' if the output correctly reflects the user's preferences and asks for more information if needed and return 'False' if it does not."""
    assert llm_judge(judge_model_prompt) is True

def test_check_is_done_returns_boolean(setup):
    model = setup
    state = ConversationState(
        conversation_id="test_conversation",
        user_id="test_user",
        messages=[{"role": "user", "content": "I want to invest in a low-risk portfolio with a long-term horizon."}],
        user_preferences="risk_tolerance: low, horizon: long-term",
        is_complete=None
    )
    updated_state = model.check_is_done(state)
    assert isinstance(updated_state.is_complete, bool)

def test_invoke_returns_expected_output(setup):
    model = setup
    conversation_input = {
        "user_prompt": "I want to invest in a low-risk portfolio with a long-term horizon.",
        "conversation_id": "test_conversation",
        "user_id": "test_user",
        "version": "0.1.0"
    }
    output = model.invoke(conversation_input)
    assert isinstance(output, dict)
    assert output.get("messages") is not None
    assert output.get("user_preferences") is not None
    assert output.get("is_complete") is not None