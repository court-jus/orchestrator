import math
import sys
import time

from .core import EventChannel, LFO
from .core.values import Value as v
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

    # Transformers
    vt1 = VelocityTransformer(output=lead, min=30, max=70)

    # Emitters
    crd = ChordsEmitter(ec, sc, output=chords)
    rne = RandomNoteEmitter(
        ec,
        sc,
        range_size=LFO(ec, rate=v(300), min=v(1), max=v(18)),
        range_center=LFO(ec, rate=v(100), min=v(50), max=v(75)),
        output=vt1,
        note_duration=LFO(ec, rate=v(80), min=v(10), max=v(55)),
    )

    # with a clock at 120bpm and 120ticks per quarter
    # 6 at 4/16 = 120bpm
    # Rythm
    BresenhamEuclideanRythm(
        ec,
        rne,
        base=v(6),
        pulses=LFO(
            ec, rate=LFO(ec, rate=v(200), min=v(50), max=v(250)), min=v(3), max=v(13)
        ),
        length=v(32),
    )
    BresenhamEuclideanRythm(ec, crd, base=v(6), pulses=v(2), length=v(32))

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
