import time

from .core import EventChannel
from .emitters import ChordsEmitter, RandomNoteEmitter
from .master import Clock, Scale
from .tools import get_port


def main():
    # Events handling
    ec = EventChannel()

    # MIDI Ports
    inport = get_port("keyboard", direction="input", callback=ec.publish)
    sysport = get_port("midiclock:output", direction="input", callback=ec.publish)
    outport = get_port("fluid")

    # Master
    ck = Clock(ec)
    ec.subscribe("clock", ck.clock)

    sc = Scale()
    sc.set_scale("major")
    sc.set_scale("minor")
    # ec.subscribe("note_on", sc.noteon)

    # Emitters
    # rne = RandomNoteEmitter(sc, output=outport, channel=0)
    crd = ChordsEmitter(sc, output=outport, channel=1)
    # ec.subscribe("tick", rne.tick)
    ec.subscribe("tick", crd.tick)
    ec.subscribe("note_on", crd.noteon)

    try:
        print(">")
        while True:
            time.sleep(10)
            print(".")
    finally:
        inport.close()
        sysport.close()
        outport.close()


if __name__ == "__main__":
    main()
