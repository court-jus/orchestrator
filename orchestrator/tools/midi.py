import logging

import mido

logger = logging.getLogger("get_port")


def get_port(query, direction="output", **kwargs):
    port_lister = (
        mido.get_output_names if direction == "output" else mido.get_input_names
    )
    port_getter = mido.open_output if direction == "output" else mido.open_input
    kwargs.update({"autoreset": True} if direction == "output" else {})
    for portname in port_lister():
        logger.debug(portname)
        if query.lower() in portname.lower():
            return port_getter(portname, **kwargs)


def filter_events(callback, allowed_events):
    def receive(msg):
        if msg.type in allowed_events:
            callback(msg)

    return receive
