import asyncio

from conversation_agent.agent.conversation_agent import ConversationModel
from core.eventbus import EventBus
from core.events import UserConversastionInputEvent, UserConversastionOutputEvent


class ConversationService:
    """
    Handles communication between conversation module and the rest of the applicaiton.

    Attrbutes:
    - eventbus (EventBus): The event bus used to send and receive events.
    - queue (asyncio.Queue): The queue used to receive events from the event bus.
    - conversation_model (ConversationModel): The model used to generate AI responses.
    """
    def __init__(self, eventbus: EventBus):
        self.eventbus = eventbus
        self.queue = asyncio.Queue()
        self.conversation_model = ConversationModel()

        # Subscribe to the event bus for conversation events
        self.eventbus.subscribe(UserConversastionInputEvent, self.queue)

    async def run(self):
        while True:
            # Wait for a new event from the queue
            event = await self.queue.get()

            # TODO: use conversation model to build the UserConversationOutputEvent and publish it to the event bus