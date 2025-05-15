"""Simple Event / Observer System."""

# IMPORT STANDARD LIBRARIES
from typing import Dict, List, Any, Protocol, Callable

# IMPORT LOCAL LIBRARIES
from cyclone.logger import logger


class Event:
    """Represents an event emitted by the system.

    Might extend this later to carry data between listeners
    or provide additional information (eg.: trigger source)

    Attributes:
        name: The name of the event.
    """

    def __init__(self, name: str):
        self.name = name


class EventCallback(Protocol):
    """A protocol representing a valid event callback function.

    Functions must accept an Event instance and optional keyword arguments.

    """

    def __call__(self, event: Event, **kwargs: Any) -> None: ...


_listeners: Dict[str, List[EventCallback]] = {}
"""Map of registered callbacks by event name."""


def register(event_name: str, callback: EventCallback) -> None:
    """Register a callback to be called when an event with the given name is emitted.

    Args:
        event_name: The name of the event to listen for.
        callback: A function that takes an Event instance.

    """
    _listeners.setdefault(event_name, []).append(callback)


def on(event_name: str) -> Callable[..., EventCallback]:

    def decorator(func: EventCallback) -> EventCallback:
        register(event_name, func)
        return func

    return decorator


def emit(event_name: str, **kwargs: Any) -> None:
    """Emit an event with the given name. All registered callbacks for that name will be called.

    Args:
        event_name: The name of the event being emitted.
        **kwargs: Additional data to attach to the event.

    """
    logger.debug(f"{event_name} | kwargs: {kwargs}")
    kwargs["event"] = Event(event_name)
    for callback in _listeners.get(event_name, []):
        callback(**kwargs)


def clear(event_name: str | None = None) -> None:
    """Clear registered listeners.

    Args:
        event_name (str, optional): If provided, only clears listeners for that event name.
                                    If None, clears all registered listeners.

    """
    if event_name:
        _listeners.pop(event_name, None)
    else:
        _listeners.clear()
