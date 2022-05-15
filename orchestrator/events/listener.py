class EventListener:
    """Base class all listeners must implement."""

    def __init__(self, ec=None):
        self.ec = ec
        self._uimode = None
        if self.ec:
            self.ec.subscribe("uimode", self.uimode)

    def uimode(self, _event, newmode, *_a, **_kw):
        self._uimode = newmode
        if hasattr(self, "display"):
            getattr(self, "display")()

    def set_event_channel(self, ec):
        if self.ec is not None:
            self.ec.unsubscribe_all(self)
        self.ec = ec
        self.ec.subscribe("uimode", self.uimode)
