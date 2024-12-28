import threading

import src.globals as GLOBALS
from src.LogService import BaseLogger


class PortCaptain(BaseLogger):
    DEPART_NOW_SIGNAL = "DEPART_NOW"
    STOP_ALL_CRUISES_SIGNAL = "STOP_ALL_CRUISES"

    def __init__(self):
        """
        Initializes the PortCaptain with a reference to the ShipCaptain.
        """
        super().__init__("Kapitan portu")
        self.signal_stop = threading.Event()

    def send_depart_now_signal(self):
        """
        Sends a signal to the ship captain to depart immediately.
        """
        self.log("Wysyłanie sygnału DEPART_NOW.")
        GLOBALS.captain.handle_signal(PortCaptain.DEPART_NOW_SIGNAL)

    def send_stop_signal(self):
        """
        Sends a signal to stop further cruises.
        """
        self.log("Wysyłanie sygnału STOP_ALL_CRUISES.")
        if self.signal_stop.is_set():
            self.log("Sygnał STOP_ALL_CRUISES został już wysłany.")
            return
        self.signal_stop.set()
        GLOBALS.captain.handle_signal(PortCaptain.STOP_ALL_CRUISES_SIGNAL)
