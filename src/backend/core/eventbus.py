import asyncio
import logging
from typing import Any

logger = logging.getLogger("core")

class EventBus:
    def __init__(self):
        self._subscribers = {}

    def subscribe(self, event_type: Any, queue: asyncio.Queue):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(queue)

    async def publish(self, event_type: Any, *args, **kwargs):
        if event_type in self._subscribers:
            for queue in self._subscribers[event_type]:
                await queue.put((args, kwargs))
        else:
            logger.warning(f"No subscribers for event type: {event_type}")