import mido


class EventChannel:
    def __init__(self):
        self.subscribers = {}
    
    def unsubscribe(self, event, callback):
        if event in self.subscribers:
            self.subscribers[event] = list(
                filter(
                    lambda x: x is not callback,
                    self.subscribers[event]
                )
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
        if event not in ("tick", "clock"):
            print(event, callargs, kwargs)
        for callback in self.subscribers.get(event, []):
            callback(event, *callargs, **kwargs)
