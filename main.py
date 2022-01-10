import sys
import time

from remi import Server

from orchestrator.master import global_controller
from orchestrator.song import loadsong
from orchestrator.tools.midi import get_port
from orchestrator.ui.menu import Menu
from orchestrator.ui.remiui import RemiUI


def quit(ports, server):
    print("QUIT!!")
    server.stop()
    global_controller.save()
    for port in ports:
        if port:
            print("Closing port", port)
            port.close()
            print("Port", port, "closed")
    sys.exit(0)


def filter_clock(callback):
    def receive(msg):
        if msg.type != "clock":
            callback(msg)

    return receive


def main():
    gc = global_controller

    # MIDI Ports
    midikbd = get_port(
        "digital piano", direction="input", callback=filter_clock(gc.ec.publish)
    )
    midictrl = get_port("launch control", direction="input", callback=gc.ec.publish)
    clockport = get_port("midiclock", direction="input", callback=gc.ec.publish)
    all_ports = [midikbd, midictrl, clockport]

    opened_ports, song = loadsong("song1.json", global_controller)
    all_ports.extend(opened_ports)

    # with a clock at 120bpm and 120ticks per quarter
    # 6 at 4/16 = 120bpm

    # UI
    menu = gc.menu
    menu.display()
    # ec.subscribe("tick", menu.tick)
    gc.ec.subscribe("display", menu.display)
    gc.ec.subscribe("control_change", menu.user_action)

    server = Server(RemiUI, start=False, start_browser=False, port=32841)
    gc.ec.subscribe("quit", lambda *_a, **_kw: quit(all_ports, server))
    server.start()
    while server._alive:
        time.sleep(0.5)


if __name__ == "__main__":
    main()
