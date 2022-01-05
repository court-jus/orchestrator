import math
import sys
import time

from .core import EventChannel
from .emitters import ChordsEmitter, RandomNoteEmitter
from .master import Clock, Scale
from .outputs import MidiNotes
from .rythm import BresenhamEuclideanRythm
from .tools import get_port
from .transformers import VelocityTransformer
from .ui import Menu


def quit(ports):
    for port in ports:
        if port:
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

    # Outputs
    lead = MidiNotes(port=outport, channel=0)
    chords = MidiNotes(port=outport, channel=1)

    # Master
    Clock(ec)

    sc = Scale(ec)
    sc.set_scale("major")

    # Transformers
    vt1 = VelocityTransformer(output=lead, min=50, max=100)

    # Emitters
    crd = ChordsEmitter(ec, sc, output=chords)
    rne = RandomNoteEmitter(ec, sc, range=(60, 72), output=vt1)

    # with a clock at 120bpm and 120ticks per quarter
    # 6 at 4/16 = 120bpm
    # Rythm
    BresenhamEuclideanRythm(ec, rne, base=6, pulses=10, length=16)
    BresenhamEuclideanRythm(ec, crd, base=6, pulses=1, length=16)

    # UI
    menu = Menu(ec, sc)
    menu.display()
    # ec.subscribe("tick", menu.tick)
    ec.subscribe("display", menu.display)
    ec.subscribe("control_change", menu.user_action)

    try:
        while True:
            time.sleep(1)
            ec.publish("heartbeat")
    finally:
        quit(all_ports)


if __name__ == "__main__":
    main()
