import json
from jsonpath_ng import jsonpath, parse

from ..core.events import EventListener


class Menu(EventListener):
    def __init__(self, ec):
        self.ec = ec
        with open("orchestrator/ui/menu.json", "r") as fp:
            self.menu = json.load(fp)
        self.initmenu("$.main")
        super().__init__(ec)

    def initmenu(self, menupath):
        self.currentmenupath = menupath
        self.currentselection = None
        self.currentmenu = None
        self.actions = []
        self.loadmenu()

    def loadmenu(self):
        self.currentmenu = parse(self.currentmenupath).find(self.menu)[0].value
        self.actions = []
        for item in self.currentmenu["items"]:
            self.actions.append(item)

    def display(self):
        print(f"{self.currentmenu['title']} - {self._uimode}")
        for idx, item in list(enumerate(self.actions))[::-1]:
            print(
                f"{'>' if self.currentselection == idx else ' '}  {idx + 1}. {item['title']}"
            )

    def user_action(self, event, msg):
        if msg.channel != 15:  # Channels are 0 indexed
            return
        if msg.control == 0 and msg.value == 127:
            # Up arrow
            self.currentselection = (
                min(len(self.actions) - 1, self.currentselection + 1)
                if self.currentselection is not None
                else 1
            )
            self.display()
        elif msg.control == 1 and msg.value == 127:
            # Down arrow
            self.currentselection = (
                max(0, self.currentselection - 1)
                if self.currentselection is not None
                else 0
            )
            self.display()
        elif (
            msg.control == 3 and msg.value == 127 and self.currentselection is not None
        ):
            # Right arrow
            menuitem = self.actions[self.currentselection]
            if menuitem["action"] == "menu":
                self.initmenu(menuitem["args"][0])
                self.display()
            else:
                self.ec.publish(
                    menuitem["action"],
                    *menuitem.get("args", []),
                    **menuitem.get("kwargs", {}),
                )
        elif msg.control == 2 and msg.value == 127:
            # Emergency quit with left arrow
            self.ec.publish("quit")
