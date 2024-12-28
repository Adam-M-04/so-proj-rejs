import threading
import time
import src.globals as GLOBALS

class ShipCaptain:
    def __init__(self):
        """
        Initializes the ShipCaptain with the ship and bridge semaphore.
        :param ship: Instance of the Ship class.
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
                print("Mostek jest pusty.")
                return True
            else:
                print("Pasażerowie nadal na mostku.")
                return False

    def depart(self):
        """
        Initiates the departure process.
        Waits until the bridge is empty before departing.
        """
        print("Przygotowanie do odpłynięcia.")
        while not self.check_bridge_empty():
            time.sleep(1)

        print("Statek gotowy do odpłynięcia.")
        self.allow_departure.set()

    def handle_signal(self, signal):
        """
        Handles signals from the PortCaptain.
        :param signal: Signal type (e.g., 'DEPART_NOW').
        """
        # if signal == "DEPART_NOW":
        #     print("Received signal: DEPART_NOW. Departing immediately!")
        #     self.departure_signal.set()
