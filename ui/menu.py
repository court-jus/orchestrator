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
        if msg.channel == 0 and msg.control == 4:
            # Update current selection
            self.currentselection = min(
                len(self.actions) - 1, int(msg.value * len(self.actions) / 127)
            )
            self.display()
        elif (
            msg.channel == 0 and msg.control == 5 and self.currentselection is not None
        ):
            # Activate current selection
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
