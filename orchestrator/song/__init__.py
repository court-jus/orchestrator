import logging
import json

from ..emitters import Value
from ..emitters.numbers.midi_control import MidiControl
from ..emitters.numbers.multiplier import Multiplier
from ..emitters.numbers.quantizer import Quantizer
from ..emitters.numbers.lfo import LFO
from ..emitters.numbers.random_value import RandomValue
from ..emitters.lists.chords import ChordsEmitter
from ..emitters.booleans.euclidean import BresenhamEuclideanRythm
from ..outputs.midi_notes import MidiNotes
from ..master.track import Track

logger = logging.getLogger("Song")
MODULES = {
    "MidiNotes": {"class": MidiNotes},
    "dict": {"class": dict},
    "Track": {
        "class": Track,
        "args": [
            "ec",
        ],
    },
    "BresenhamEuclideanRythm": {
        "class": BresenhamEuclideanRythm,
    },
    "Value": {
        "class": Value,
    },
    "RandomValue": {
        "class": RandomValue,
    },
    "LFO": {
        "class": LFO,
        "args": [
            "ec",
        ],
    },
    "MidiControl": {
        "class": MidiControl,
        "args": [
            "ec",
        ],
    },
    "Multiplier": {
        "class": Multiplier,
    },
    "Quantizer": {
        "class": Quantizer,
    },
    "ChordsEmitter": {
        "class": ChordsEmitter,
    },
}


def loadsong(filename, ctrl):
    ec = ctrl.ec
    with open(filename, "r") as fp:
        song = json.load(fp)
    return recursively_load(song, ec=ec)


def recursively_load(data, **global_kwargs):
    item_type = MODULES[data.pop("type", "Value")]
    item_class = item_type["class"]
    logger.debug(f"=== LOAD {item_class} from ---\n{data}")
    item_args = [global_kwargs[arg_name] for arg_name in item_type.get("args", [])]
    item_kwargs = {}
    result = None
    opened_ports = set()
    for k, v in data.items():
        logger.debug(f"For {item_type} get {k} from {v}")
        if not isinstance(v, dict):
            item_kwargs[k] = v
            continue
        ports, item_kwargs[k] = recursively_load(v, **global_kwargs)
        opened_ports = opened_ports.union(ports)
        logger.debug(f"Spawn class {item_class}(*{item_args}, **{item_kwargs})")
    result = item_class(*item_args, **item_kwargs)
    if hasattr(result, "opened_port"):
        opened_ports.add(getattr(result, "opened_port"))
    logger.debug(f"--- result: {result} ===")
    return opened_ports, result
