import json
import os
import logging


import mido
from jsonpath_ng import parse

from ..events.listener import EventListener
from ..tools.midi import list_inputs
from ..tools.midi import filter_events


logger = logging.getLogger("Menu")


class Menu(EventListener):
    def __init__(self, global_controller):
        self.gc = global_controller
        self.scale = self.gc.scale
        ec = self.gc.ec
        with open("orchestrator/ui/menu.json", "r") as fp:
            self.menu = json.load(fp)
        self.initmenu("$.main")
        super().__init__(ec)
        self.ec.subscribe("choose_port", self.choose_port)

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

    def display(self, _event=None, _msg=None, *_a, **_kw):
        print(f"{self.currentmenu['title']} - {self._uimode}")
        print(
            f"{self.scale.root} - {self.scale.scale_name} - {self.scale.chord_name} - {self.scale.degree + 1}"
        )
        for idx, item in list(enumerate(self.actions))[::-1]:
            print(
                f"{'>' if self.currentselection == idx else ' '}  {idx + 1}. {item['title']}"
            )

    def user_action(self, event, msg, *_a, **_kw):
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
                if self.ec:
                    self.ec.publish(
                        menuitem["action"],
                        *menuitem.get("args", []),
                        **menuitem.get("kwargs", {}),
                    )
        elif msg.control == 2 and msg.value == 127:
            # Emergency quit with left arrow
            if self.ec:
                self.ec.publish("quit")

    def scaletype(self):
        return [{"title": "Back", "action": "menu", "args": ["$.perform"],},] + [
            {
                "title": scalename,
                "action": "set_scale",
                "args": [scalename],
            }
            for scalename in self.scale.available_scales
        ]

    def chordtype(self):
        return [{"title": "Back", "action": "menu", "args": ["$.perform"],},] + [
            {
                "title": chordname,
                "action": "set_chord",
                "args": [chordname],
            }
            for chordname, _ in self.scale.available_chords
        ]

    def midiclocks(self):
        return [
            {
                "id": deviceid,
                "title": devicename,
                "action": "set_clock",
                "args": [deviceid],
            }
            for deviceid, devicename in list_inputs()
        ]

    def midinote(self):
        return [
            {
                "id": deviceid,
                "title": devicename,
                "action": "set_noteinput",
                "args": [deviceid],
            }
            for deviceid, devicename in list_inputs()
        ]

    def choosedegree(self):
        return [{"title": "Back", "action": "menu", "args": ["$.perform"],},] + [
            {
                "title": idx + 1,
                "action": "set_degree",
                "args": [idx],
            }
            for idx in range(len(self.scale.base_notes))
        ]

    def listsongs_to_load(self):
        return [{"title": "Back", "action": "menu", "args": ["$.song"],},] + [
            {
                "title": filename,
                "action": "loadsong",
                "args": [filename],
            }
            for filename in os.listdir("songs")
        ]

    def choose_port(self, _event, action, direction, filtered_events, portname=None):
        logger.debug(f"{action} for {direction} (args: {filtered_events}, {portname})")
        if action == "list_ports":
            self.actions = []
            # Add a "back to main menu" action
            self.actions.append(
                {
                    "title": "Back to main menu",
                    "action": "menu",
                    "args": ["$.main"],
                }
            )
            port_lister = (
                mido.get_output_names if direction == "output" else mido.get_input_names
            )
            for portname in port_lister():
                self.actions.append(
                    {
                        "title": portname,
                        "action": "choose_port",
                        "args": ["choose", direction, filtered_events, portname],
                    }
                )
            self.ec.publish("display")
        elif action == "choose":
            port_getter = mido.open_output if direction == "output" else mido.open_input
            kwargs = {"callback": filter_events(self.gc.ec.publish, filtered_events)}
            kwargs.update({"autoreset": True} if direction == "output" else {})
            self.gc.opened_ports.append(
                {
                    "direction": direction,
                    "filtered_events": filtered_events,
                    "portname": portname,
                    "instance": port_getter(portname, **kwargs),
                }
            )

    def tick(self, _event, step, *_a, **_kw):
        # For debug purpose
        return
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
