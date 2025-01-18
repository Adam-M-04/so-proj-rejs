import threading
import time
import src.globals as GLOBALS
from src.LogService import BaseLogger
from src.objects.port_captain import PortCaptain
from src.objects.ship import ShipStatus
from src.stop_boarding_passengers import stop_boarding_passengers


class ShipCaptain(BaseLogger):
    def __init__(self):
        """
        Initializes the ShipCaptain with the ship and bridge semaphore.
        """
        super().__init__("Kapitan statku")
        self.lock = threading.Lock()
        self.allow_departure = threading.Event()

    def check_bridge_empty(self):
        """
        Checks if the bridge is empty.
        :return: True if the bridge is empty, False otherwise.
        """
        with self.lock:
            if GLOBALS.bridge_semaphore._value == GLOBALS.bridge_capacity:
                self.log("Mostek jest pusty.")
                return True
            else:
                self.log("Pasażerowie nadal na mostku.")
                return False

    def depart(self):
        """
        Initiates the departure process.
        Waits until the bridge is empty before departing.
        """
        try:
            if GLOBALS.port_captain.signal_stop.is_set():
                return
            self.log("Przygotowanie do odpłynięcia.")
            while not self.check_bridge_empty():
                time.sleep(1)

            self.log("Statek gotowy do odpłynięcia.")
            self.allow_departure.set()
        except Exception as e:
            GLOBALS.logger.error(e)

    def handle_signal(self, signal):
        """
        Handles signals from the PortCaptain.
        :param signal: Signal type (e.g., 'DEPART_NOW').
        """
        try:
            self.log(f"Otrzymano sygnał {signal}.")
            if signal == PortCaptain.DEPART_NOW_SIGNAL:
                if GLOBALS.ship.status != ShipStatus.BOARDING_IN_PROGRESS:
                    self.log("Statek już odpłynął.")
                    return

                GLOBALS.ship.depart()
            elif signal == PortCaptain.STOP_ALL_CRUISES_SIGNAL:
                stop_boarding_passengers()
                if GLOBALS.ship.status != ShipStatus.IN_CRUISE:
                    for passenger in GLOBALS.passengers:
                        passenger.thread.join()
                    GLOBALS.ship.unload_all_passengers(False)
                    GLOBALS.ship.return_event.set()
        except Exception as e:
            GLOBALS.logger.error(e)
