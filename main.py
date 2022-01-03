import sys
import time

from .core import EventChannel
from .emitters import ChordsEmitter, RandomNoteEmitter
from .master import Clock, Scale
from .tools import get_port
from .ui import Menu


def quit(ports):
    for port in ports:
        print("Closing port", port)
        port.close()
        print("Port", port, "closed")
    sys.exit(0)


def main():
    # Events handling
    ec = EventChannel()

    # MIDI Ports
    inport = get_port("keyboard", direction="input", callback=ec.publish)
    ctrl = get_port("launch control", direction="input", callback=ec.publish)
    sysport = get_port("midiclock:output", direction="input", callback=ec.publish)
    outport = get_port("fluid")
    all_ports = [inport, ctrl, sysport, outport]
    ec.subscribe("quit", lambda *_a, **_kw: quit(all_ports))

    # Master
    Clock(ec)

    sc = Scale(ec)
    sc.set_scale("major")

    # Emitters
    rne = RandomNoteEmitter(ec, sc, output=outport, channel=0)
    crd = ChordsEmitter(ec, sc, output=outport, channel=1)
    ec.subscribe("tick", rne.tick)
    ec.subscribe("uimode", rne.uimode)
    ec.subscribe("tick", crd.tick)
    ec.subscribe("uimode", crd.uimode)

    # UI
    menu = Menu(ec)
    menu.display()
    ec.subscribe("control_change", menu.user_action)

    try:
        while True:
            time.sleep(1)
            ec.publish("heartbeat")
    finally:
        quit(all_ports)


if __name__ == "__main__":
    main()
