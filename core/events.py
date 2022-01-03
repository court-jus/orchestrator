import mido


class EventChannel:
    def __init__(self, debug=False):
        self.subscribers = {}
        self.debug = debug

    def unsubscribe(self, event, callback):
        if event in self.subscribers:
            self.subscribers[event] = list(
                filter(lambda x: x is not callback, self.subscribers[event])
            )

    def subscribe(self, event, callback):
        self.subscribers.setdefault(event, [])
        if callback not in self.subscribers[event]:
            self.subscribers[event].append(callback)

    def publish(self, event, *args, **kwargs):
        if isinstance(event, mido.Message):
            callargs = [event] + list(args)
            event = event.type
        else:
            callargs = args
        if self.debug and event not in ("tick", "clock", "heartbeat"):
            print(event, callargs, kwargs)
        for callback in self.subscribers.get(event, []):
            callback(event, *callargs, **kwargs)


class EventListener:
    """Base class all listeners must implement."""

    def __init__(self, ec):
        self._uimode = None
        self.ec.subscribe("uimode", self.uimode)

    def uimode(self, _event, newmode):
        self._uimode = newmode
        if hasattr(self, "display"):
            getattr(self, "display")()
