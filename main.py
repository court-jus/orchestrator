import sys
import time

from remi import start

from orchestrator.master.track import Track

from orchestrator.emitters import (
    LFO,
    BresenhamEuclideanRythm,
    ChordsEmitter,
    RandomNoteEmitter,
    RandomValue,
)
from orchestrator.emitters import Value as v
from orchestrator.emitters.numbers.quantizer import Quantizer
from orchestrator.emitters.numbers.multiplier import Multiplier
from orchestrator.emitters.numbers.midi_control import MidiControl
from orchestrator.master import Clock, global_controller
from orchestrator.outputs.midi_notes import MidiNotes
from orchestrator.tools.midi import get_port
from orchestrator.ui.menu import Menu
from orchestrator.ui.remiui import RemiUI


def quit(ports):
    global_controller.save()
    for port in ports:
        if port:
            print("Closing port", port)
            port.close()
            print("Port", port, "closed")
    sys.exit(0)


def main():
    ctrl = global_controller
    ec = ctrl.ec
    sc = ctrl.scale

    # MIDI Ports
    inport = get_port("keyboard", direction="input", callback=ec.publish)
    ctrl = get_port("launch control", direction="input", callback=ec.publish)
    sysport = get_port("midiclock:output", direction="input", callback=ec.publish)
    outport = get_port("fluid")
    all_ports = [inport, ctrl, sysport, outport]
    ec.subscribe("quit", lambda *_a, **_kw: quit(all_ports))

    # Emitters
    # crd = ChordsEmitter(ec, sc, output=chords)
    # rne = RandomNoteEmitter(
    #     ec,
    #     sc,
    #     range_size=LFO(ec, rate=v(300), min=v(1), max=v(18)),
    #     range_center=LFO(ec, rate=v(100), min=v(50), max=v(75)),
    #     velocity=RandomValue(min=v(30), max=v(70)),
    #     note_duration=LFO(ec, rate=v(80), min=v(10), max=v(55)),
    #     output=lead,
    # )

    Track(
        BresenhamEuclideanRythm(
            base=v(6),
            pulses=LFO(ec, rate=v(150), min=v(10), max=v(13)),
            length=v(32),
        ),
        Quantizer(
            RandomValue(
                center=MidiControl(ec, channel=15, control=24, initial=64),
                size=Multiplier(
                    omin=v(2),
                    omax=v(40),
                    value=MidiControl(ec, channel=15, control=16, initial=64),
                ),
            ),
            ChordsEmitter(),
            filter_in=v(False),
            extend=v(True),
        ),
        MidiNotes(
            port=outport,
            channel=0,
            velocity=MidiControl(ec, channel=15, control=32, initial=64),
        ),
        mute=v(False),
    )
    Track(
        BresenhamEuclideanRythm(
            base=v(6),
            pulses=v(4),
            length=v(32),
        ),
        ChordsEmitter(),
        MidiNotes(
            port=outport,
            channel=1,
            velocity=MidiControl(ec, channel=15, control=33, initial=32),
            duration=v(100),
        ),
    )

    # with a clock at 120bpm and 120ticks per quarter
    # 6 at 4/16 = 120bpm
    # Rythm

    # BresenhamEuclideanRythm(ec, crd, base=v(6), pulses=v(2), length=v(32))

    # UI
    menu = Menu(ec, sc)
    menu.display()
    # ec.subscribe("tick", menu.tick)
    ec.subscribe("display", menu.display)
    ec.subscribe("control_change", menu.user_action)

    start(
        RemiUI,
        start_browser=False,
    )
    quit(all_ports)


if __name__ == "__main__":
    main()
