import time

from .emitters import RandomNoteEmitter, ChordsEmitter
from .core import EventChannel
from .tools import Clock, get_port


def main():
    # Events handling
    ec = EventChannel()

    # MIDI Ports
    inport = get_port("keyboard", direction="input", callback=ec.publish)
    sysport = get_port("midiclock:output", direction="input", callback=ec.publish)
    outport = get_port("fluid")

    # Clock
    ck = Clock(ec)
    ec.subscribe("clock", ck.clock)

    # Emitters
    rne = RandomNoteEmitter(output=outport, channel=0)
    crd = ChordsEmitter(output=outport, channel=1)
    rne.available_notes = [57, 60, 64, 67, 57, 60, 64, 67, 57, 60, 64, 67, 57, 57, 59, 62, 65, 69, 69]
    crd.available_notes = [57, 60, 64, 67]
    ec.subscribe("tick", rne.tick)
    ec.subscribe("note_on", rne.noteon)
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
