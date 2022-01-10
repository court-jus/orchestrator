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
    closable = []
    item_args = [global_kwargs[arg_name] for arg_name in item_type.get("args", [])]
    item_kwargs = {}
    result = None
    for k, v in data.items():
        logger.debug(f"For {item_type} get {k} from {v}")
        if not isinstance(v, dict):
            item_kwargs[k] = v
            continue
        item_kwargs[k], child_closable = recursively_load(v, **global_kwargs)
        closable.extend(child_closable)
    result = item_class(*item_args, **item_kwargs)
    if hasattr(result, "close"):
        closable.append(result)
    return result, closable
