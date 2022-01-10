import pprint
import logging

import mido

logger = logging.getLogger("EventChannel")


class EventChannel:
    def __init__(self, debug=False):
        self.subscribers = {}
        self.debug = debug

    def unsubscribe(self, event, callback):
        if event in self.subscribers:
            self.subscribers[event] = list(
                filter(lambda x: x is not callback, self.subscribers[event])
            )

    def unsubscribe_all(self, instance):
        logger.debug(f"Unsubscribe all callbacks for {instance}")
        for event in self.subscribers:
            self.subscribers[event] = list(
                filter(
                    lambda x: x is not instance
                    and (
                        x.__self__ is not instance if hasattr(x, "__self__") else True
                    ),
                    self.subscribers[event],
                )
            )
        logger.debug(f"Now subscribers are {self.subscribers}")

    def subscribe(self, event, callback):
        logger.debug(f"New subscriber on {id(self)}({event}): {callback}")
        self.subscribers.setdefault(event, [])
        subscriber_class = callback.__self__ if hasattr(callback, "__self__") else None
        if subscriber_class is not None and not hasattr(subscriber_class, "clear"):
            raise NotImplementedError(
                f"EventListener subclasses should implement the clear() method. {subscriber_class} does not."
            )

        if callback not in self.subscribers[event]:
            self.subscribers[event].append(callback)
        pprint.pprint(self.subscribers)

    def publish(self, event, *args, **kwargs):
        if isinstance(event, mido.Message):
            callargs = [event] + list(args)
            event = event.type
        else:
            callargs = args
        if self.debug and event not in ("tick", "clock"):
            logger.debug(f"{event}, {callargs}, {kwargs}")
        for callback in self.subscribers.get(event, []):
            callback(event, *callargs, **kwargs)
