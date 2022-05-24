import sys
import time
import logging

from remi import Server

from orchestrator.master import global_controller
from orchestrator.ui.remiui import RemiUI


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main")
logger.setLevel(logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def quit(server):
    logger.info("QUIT!!")
    server.stop()
    global_controller.save()
    global_controller.close_all_ports()
    sys.exit(0)


def main():
    gc = global_controller
    # with a clock at 120bpm and 120ticks per quarter
    # 6 at 4/16 = 120bpm

    # UI
    menu = gc.menu
    menu.display()
    # ec.subscribe("tick", menu.tick)
    gc.ec.subscribe("display", menu.display)
    gc.ec.subscribe("control_change", menu.user_action)

    server = Server(RemiUI, start=False, start_browser=False, address="0.0.0.0", port=32841)
    gc.ec.subscribe("quit", lambda *_a, **_kw: quit(server))
    gc.postinit()
    server.start()
    try:
        while server._alive:
            time.sleep(0.5)
    except KeyboardInterrupt:
        quit(server)


if __name__ == "__main__":
    main()
