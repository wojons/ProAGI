from typing import Callable, List, Dict, Any
import asyncio # evently is asyncio-based
import evently # Import the evently library

# Import necessary data models from core.shared.data_models
from core.shared.data_models.data_models import Event # Assuming Event data model exists (Issue #XX)

from core.interfaces.event_bus_interface import EventBusInterface

class EventBus(EventBusInterface):
    """
    Provides an in-memory event bus for asynchronous communication between core framework components.
    It allows components to publish events and subscribe handler functions to specific event types.
    Uses the `evently` library for underlying event handling logic.
    """
    def __init__(self):
        """
        Initializes the EventBus with an `evently.EventBus` instance.
        """
        self._event_bus = evently.EventBus()
        print("EventBus initialized using evently.") # Basic logging
        # Note: evently handles the internal storage and dispatching,
        # no need for manual queue or subscriber registry here.

    async def publish(self, event: Event):
        """
        Publish an event to the bus. The event will be dispatched to all subscribed
        handlers for the event's type.

        Args:
            event: The Event object to publish.
        """
        print(f"Publishing event: {event.event_type} (Event ID: {getattr(event, 'eventId', 'N/A')})") # Basic logging, assuming eventId exists
        try:
            # evently's publish method takes the event type and the event data
            await self._event_bus.publish(event.event_type, event)
        except Exception as e:
            print(f"Error publishing event {event.event_type}: {e}") # Basic logging
            # TODO: Log this error properly (Issue #XX)
            # TODO: Consider error handling or retry mechanisms for publishing (Issue #XX)


    async def subscribe(self, event_type: str, handler: Callable):
        """
        Subscribe an asynchronous handler function to a specific event type.
        The handler will be called whenever an event of the specified type is published.

        Args:
            event_type: The type of event to subscribe to.
            handler: The async callable function to handle the event. This function should accept one argument, the Event object.
        """
        print(f"Subscribing handler {handler.__name__} to event type: {event_type}") # Basic logging
        try:
            # evently's subscribe method takes the event type and the handler
            self._event_bus.subscribe(event_type, handler)
        except Exception as e:
            print(f"Error subscribing handler {handler.__name__} to event type {event_type}: {e}") # Basic logging
            # TODO: Log this error properly (Issue #XX)


    async def unsubscribe(self, event_type: str, handler: Callable):
        """
        Unsubscribe a handler function from a specific event type.
        The handler will no longer receive events of this type.

        Args:
            event_type: The type of event to unsubscribe from.
            handler: The async callable function to unsubscribe.
        """
        print(f"Unsubscribing handler {handler.__name__} from event type: {event_type}") # Basic logging
        try:
            # evently's unsubscribe method takes the event type and the handler
            self._event_bus.unsubscribe(event_type, handler)
        except Exception as e:
            print(f"Error unsubscribing handler {handler.__name__} from event type {event_type}: {e}") # Basic logging
            # TODO: Log this error properly (Issue #XX)

    # evently handles the event processing loop internally when publish/subscribe are used.
    # No need for a separate _process_events or _dispatch_event method here.
    # TODO: Consider adding methods for listing subscribers or event types if needed for debugging/monitoring (Issue #XX)
    # TODO: Consider adding support for persistent event storage or a distributed message queue for robustness/scalability (Issue #XX)
