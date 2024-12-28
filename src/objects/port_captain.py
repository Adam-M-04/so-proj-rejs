import threading

import src.globals as GLOBALS

class PortCaptain:
    DEPART_NOW_SIGNAL = "DEPART_NOW"
    STOP_ALL_CRUISES_SIGNAL = "STOP_ALL_CRUISES"

    def __init__(self):
        """
        Initializes the PortCaptain with a reference to the ShipCaptain.
        """
        self.signal_stop = threading.Event()

    @staticmethod
    def send_depart_now_signal():
        """
        Sends a signal to the ship captain to depart immediately.
        """
        GLOBALS.logger.log("[Kapitan portu] Wysyłanie sygnału DEPART_NOW.")
        GLOBALS.captain.handle_signal(PortCaptain.DEPART_NOW_SIGNAL)

    def send_stop_signal(self):
        """
        Sends a signal to stop further cruises.
        """
        GLOBALS.logger.log("[Kapitan portu] Wysyłanie sygnału STOP_ALL_CRUISES.")
        if self.signal_stop.is_set():
            GLOBALS.logger.log("[Kapitan portu] Sygnał STOP_ALL_CRUISES został już wysłany.")
            return
        self.signal_stop.set()
        GLOBALS.captain.handle_signal(PortCaptain.STOP_ALL_CRUISES_SIGNAL)
