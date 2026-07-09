# Tests for the conversation service
# 1. Just an end to end test with starting up the conversation service, sending UserConversationInputEvent into the eventbus and ensuring that the UserConversationOutputEvent is published to the eventbus with the expected fields filled out
import asyncio

import pytest
from conversation_agent.conversation_service import ConversationService
from core.eventbus import EventBus
from core.events import UserConversastionInputEvent, UserConversastionOutputEvent


def test_conversation_service_smoke():
    eventbus = EventBus()
    service = ConversationService(eventbus)

    async def run_service():
        await service.run()

    async def send_input_event():
        await asyncio.sleep(1)  # Give the service some time to start
        input_event = UserConversastionInputEvent(
            conversation_id="test_conversation",
            user_id="test_user",
            message="I want to invest in a low-risk portfolio with a long-term horizon."
        )
        await eventbus.publish(input_event)

    async def listen_for_output_event():
        queue = asyncio.Queue()
        eventbus.subscribe(UserConversastionOutputEvent, queue)
        output_event = await queue.get()
        assert output_event.conversation_id == "test_conversation"
        assert output_event.user_id == "test_user"
        assert output_event.ai_response is not None
        assert output_event.user_preferences is not None
        assert isinstance(output_event.is_done, bool)

    loop = asyncio.get_event_loop()
    tasks = [
        loop.create_task(run_service()),
        loop.create_task(send_input_event()),
        loop.create_task(listen_for_output_event())
    ]
    loop.run_until_complete(asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED))