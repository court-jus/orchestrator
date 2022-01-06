class EventListener:
    """Base class all listeners must implement."""

    def __init__(self, ec=None):
        self.ec = ec
        self._uimode = None
        if self.ec:
            self.ec.subscribe("uimode", self.uimode)

    def uimode(self, _event, newmode):
        self._uimode = newmode
        if hasattr(self, "display"):
            getattr(self, "display")()
