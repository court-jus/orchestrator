import mido


def get_port(query, direction="output", **kwargs):
    port_lister = (
        mido.get_output_names if direction == "output" else mido.get_input_names
    )
    port_getter = mido.open_output if direction == "output" else mido.open_input
    kwargs.update({"autoreset": True} if direction == "output" else {})
    for portname in port_lister():
        print(portname)
        if query.lower() in portname.lower():
            return port_getter(portname, **kwargs)
