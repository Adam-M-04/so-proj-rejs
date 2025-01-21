import multiprocessing
import sys
import select
import threading

import src.globals as GLOBALS

class PortCaptain:
    def __init__(self):
        """
        Initializes the PortCaptain with a reference to the ShipCaptain.
        """
        self.signal_stop = multiprocessing.Event()
        self.end_thread = multiprocessing.Event()
        self.boarding_allowed = multiprocessing.Value('b', False)

    def send_depart_now_signal(self):
        """
        Sends a signal to the ship captain to depart immediately.
        """
        GLOBALS.logger.log("Wysyłanie sygnału DEPART_NOW.")
        self.boarding_allowed.value = False

    def send_stop_signal(self):
        """
        Sends a signal to stop further cruises.
        """
        try:
            GLOBALS.logger.log("Wysyłanie sygnału STOP_ALL_CRUISES.")
            if self.signal_stop.is_set():
                GLOBALS.logger.log("Sygnał STOP_ALL_CRUISES został już wysłany.")
                return
            self.signal_stop.set()
        except Exception as e:
            GLOBALS.logger.error(e)

    def start(self):
        """
        Starts the PortCaptain thread to listen for input from the user.
        """
        threading.Thread(target=self.read_input, args=(self.end_thread,)).start()

    def stop(self):
        """
        Starts the PortCaptain thread to listen for input from the user.
        """
        self.end_thread.set()

    @staticmethod
    def read_input(end_thread):
        """
        Reads input from the user to control the simulation.

        Listens for specific key presses:
        - 'r': Sends a stop signal to the port captain.
        - 'd': Sends a depart now signal to the port captain.
        """
        try:
            while GLOBALS.trips_count < GLOBALS.max_trips and not GLOBALS.port_captain.signal_stop.is_set() and not end_thread.is_set():
                if sys.stdin in select.select([sys.stdin], [], [], 1)[0]:
                    char = sys.stdin.read(1)
                    if char == 'r':
                        GLOBALS.port_captain.send_stop_signal()
                    elif char == 'd':
                        GLOBALS.port_captain.send_depart_now_signal()
        except Exception as e:
            GLOBALS.logger.error(e)
        finally:
            return
