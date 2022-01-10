import sys
import time

from remi import Server

from orchestrator.master import global_controller
from orchestrator.song import loadsong
from orchestrator.tools.midi import get_port, open_all_inputs
from orchestrator.ui.menu import Menu
from orchestrator.ui.remiui import RemiUI


def quit(closables, server):
    print("QUIT!!, Stop server")
    server.stop()
    print("QUIT!!, Server stopped, close midi ports")
    global_controller.save()
    for closable in closables:
        if closable and hasattr(closable, "close"):
            print("Closing", closable)
            closable.close()
            print(closable, "closed")
    sys.exit(0)


def filter_clock(callback):
    def receive(msg):
        if msg.type != "clock":
            callback(msg)

    return receive


def main():
    gc = global_controller

    # MIDI Ports
    # midikbd = get_port(
    #     "iRig", direction="input", callback=filter_clock(gc.ec.publish)
    # )
    # midictrl = get_port("launch control", direction="input", callback=gc.ec.publish)
    # clockport = get_port("midiclock", direction="input", callback=gc.ec.publish)
    # all_ports = [midikbd, midictrl, clockport]
    all_ports = open_all_inputs(gc.ec)

    song, closables = loadsong("song2.json", global_controller)
    all_ports.extend(closables)

    # with a clock at 120bpm and 120ticks per quarter
    # 6 at 4/16 = 120bpm

    # UI
    menu = gc.menu
    menu.display()
    # ec.subscribe("tick", menu.tick)
    gc.ec.subscribe("display", menu.display)
    gc.ec.subscribe("control_change", menu.user_action)

    server = Server(
        RemiUI, start=False, start_browser=False, port=32841, update_interval=0.01
    )
    gc.ec.subscribe("quit", lambda *_a, **_kw: quit(all_ports, server))
    server.start()
    print("Main loop")
    while server._alive:
        time.sleep(0.01)


if __name__ == "__main__":
    main()
