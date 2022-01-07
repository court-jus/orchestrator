from remi import App, gui

from ..master import global_controller


class RemiUI(App):
    def __init__(self, *args):
        global_controller.ec.subscribe("display", self.display)
        super().__init__(*args)

    def main(self):
        self.main_container = gui.VBox(width=320, height=240)
        global_controller.main_label = gui.Label()
        global_controller.sub_label = gui.Label()
        global_controller.menu_container = gui.VBox(width=320, height="100%")
        self.main_container.append(global_controller.main_label, key="title")
        self.main_container.append(global_controller.sub_label, key="subtitle")
        self.main_container.append(global_controller.menu_container, key="menu")
        self.display()
        return self.main_container

    def display(self, evt=None):
        menu = global_controller.menu
        global_controller.main_label.set_text(
            f"{menu.currentmenu['title']} - {menu._uimode}"
        )
        global_controller.sub_label.set_text(
            f"{menu.scale.root} - {menu.scale.scale_name} - {menu.scale.chord_name} - {menu.scale.degree + 1}"
        )
        global_controller.menu_container.empty()
        for idx, item in list(enumerate(menu.actions))[::-1]:
            btn = gui.Button(
                f"{'>' if menu.currentselection == idx else ' '}  {idx + 1}. {item['title']}"
            )
            btn.onclick.do(self.on_button_pressed, idx, item)
            global_controller.menu_container.append(btn, key=str(idx))

    # listener function
    def on_button_pressed(self, widget, idx, item):
        menu = global_controller.menu
        menuitem = menu.actions[idx]
        if menuitem["action"] == "menu":
            menu.initmenu(menuitem["args"][0])
            self.display()
        else:
            if menu.ec:
                menu.ec.publish(
                    menuitem["action"],
                    *menuitem.get("args", []),
                    **menuitem.get("kwargs", {}),
                )
