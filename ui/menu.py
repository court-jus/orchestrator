import mido
import json
from jsonpath_ng import parse

from ..core.events import EventListener


class Menu(EventListener):
    def __init__(self, ec, scale):
        self.ec = ec
        self.scale = scale
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
        if self.currentmenupath != "$.main":
            # Add a "back to main menu" action
            self.actions.append(
                {
                    "id": "main",
                    "title": "Back to main menu",
                    "action": "menu",
                    "args": ["$.main"],
                }
            )
        menuitems = self.currentmenu["items"]
        if isinstance(menuitems, str) and hasattr(self, menuitems):
            self.actions.extend(getattr(self, menuitems)())
        elif isinstance(menuitems, (tuple, list)):
            for item in menuitems:
                self.actions.append(item)

    def display(self, _event=None, _msg=None):
        print(f"{self.currentmenu['title']} - {self._uimode}")
        print(f"{self.scale.root} - {self.scale.scale_name} - {self.scale.chord_name}")
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

    def scaletype(self):
        return [
            {
                "id": scalename,
                "title": scalename,
                "action": "set_scale",
                "args": [scalename],
            }
            for scalename in self.scale.available_scales
        ]

    def chordtype(self):
        return [
            {
                "id": chordname,
                "title": chordname,
                "action": "set_chord",
                "args": [chordname],
            }
            for chordname in self.scale.available_chords
        ]

    def tick(self, _event, step):
        # For debug purpose
        if step % 20 != 0:
            return
        step = int(step / 20)
        actions = [
            None,
            0,
            0,
            3,
            0,
            0,
            0,
            3,
            1,
            1,
            1,
            3,
            0,
            0,
            0,
            3,
            0,
            0,
            3,
            1,
            1,
            3,
            None,
            2,
        ]
        try:
            action = actions[step]
        except IndexError:
            return

        if action is None:
            return
        self.user_action(
            "control_change",
            mido.Message("control_change", channel=15, control=action, value=127),
        )
