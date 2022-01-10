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


def list_inputs():
    choices = []
    for portname in mido.get_input_names():
        print(portname)
        choices.append((portname, portname))
    return choices


def open_all_inputs(event_channel):
    opened = []
    for portname in mido.get_input_names():
        print("OPEN", portname)

        def callback(*a, **kw):
            kw.update({"midi_port_name": portname})
            event_channel.publish(*a, **kw)

        port = mido.open_input(portname, callback=callback)
        opened.append(port)
    return opened


def filter_events(callback, allowed_events):
    def receive(msg):
        if msg.type in allowed_events:
            callback(msg)

    return receive
