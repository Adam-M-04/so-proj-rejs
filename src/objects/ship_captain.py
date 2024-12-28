import threading
import time
import src.globals as GLOBALS
from src.objects.port_captain import PortCaptain
from src.objects.ship import ShipStatus
from src.stop_boarding_passengers import stop_boarding_passengers


class ShipCaptain:
    def __init__(self):
        """
        Initializes the ShipCaptain with the ship and bridge semaphore.
        """
        self.lock = threading.Lock()
        self.allow_departure = threading.Event()

    def check_bridge_empty(self):
        """
        Checks if the bridge is empty.
        :return: True if the bridge is empty, False otherwise.
        """
        with self.lock:
            if GLOBALS.bridge_semaphore._value == GLOBALS.bridge_capacity:
                GLOBALS.logger.log("[Kapitan statku] Mostek jest pusty.")
                return True
            else:
                GLOBALS.logger.log("[Kapitan statku] Pasażerowie nadal na mostku.")
                return False

    def depart(self):
        """
        Initiates the departure process.
        Waits until the bridge is empty before departing.
        """
        if GLOBALS.port_captain.signal_stop.is_set():
            return
        GLOBALS.logger.log("[Kapitan statku] Przygotowanie do odpłynięcia.")
        while not self.check_bridge_empty():
            time.sleep(1)

        GLOBALS.logger.log("[Kapitan statku] Statek gotowy do odpłynięcia.")
        self.allow_departure.set()

    def handle_signal(self, signal):
        """
        Handles signals from the PortCaptain.
        :param signal: Signal type (e.g., 'DEPART_NOW').
        """
        GLOBALS.logger.log(f"[Kapitan statku] Otrzymano sygnał {signal}.")
        if signal == PortCaptain.DEPART_NOW_SIGNAL:
            if GLOBALS.ship.status != ShipStatus.BOARDING_IN_PROGRESS:
                GLOBALS.logger.log("[Kapitan statku] Statek już odpłynął.")
                return

            GLOBALS.ship.depart()
        elif signal == PortCaptain.STOP_ALL_CRUISES_SIGNAL:
            stop_boarding_passengers()
            if GLOBALS.ship.status == ShipStatus.IN_CRUISE:
                GLOBALS.ship.return_to_port()
            else:
                GLOBALS.ship.unload_all_passengers()
                GLOBALS.ship.return_event.set()
