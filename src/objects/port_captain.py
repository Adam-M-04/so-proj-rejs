import os
import sys
import select
from src.objects.SharedMemory import create_shared_memory, write_to_shared_memory, read_from_shared_memory

import src.globals as GLOBALS

class PortCaptain:
    def __init__(self):
        """
        Initializes the PortCaptain with shared memory objects for signals.
        """
        self.signal_stop = create_shared_memory(1)
        self.end_thread = create_shared_memory(1)
        self.boarding_allowed = create_shared_memory(1)

    def send_depart_now_signal(self):
        """
        Sends a signal to the ship captain to depart immediately by setting the boarding allowed flag to 0.
        """
        GLOBALS.logger.log("Wysyłanie sygnału DEPART_NOW.")
        write_to_shared_memory(self.boarding_allowed, 0, 0)

    def send_stop_signal(self):
        """
        Sends a signal to stop further cruises by setting the stop signal flag to 1.
        """
        try:
            GLOBALS.logger.log("Wysyłanie sygnału STOP_ALL_CRUISES.")
            if read_from_shared_memory(self.signal_stop):
                GLOBALS.logger.log("Sygnał STOP_ALL_CRUISES został już wysłany.")
                return
            write_to_shared_memory(self.signal_stop, 0, 1)
        except Exception as e:
            GLOBALS.logger.error(e)

    def start(self):
        """
        Starts the PortCaptain process to listen for input from the user in a separate process.
        """
        try:
            pid = os.fork()
            if pid == 0:
                self.read_input()
                os._exit(0)
        except OSError as e:
            return None

    def stop(self):
        """
        Stops the PortCaptain process by setting the end thread flag to 1.
        """
        write_to_shared_memory(self.end_thread, 1, 1)

    def read_input(self):
        """
        Reads input from the user to control the simulation.

        Listens for specific key presses:
        - 'r': Sends a stop signal to the port captain.
        - 'd': Sends a depart now signal to the port captain.
        """
        try:
            while GLOBALS.trips_count < GLOBALS.max_trips and not read_from_shared_memory(self.signal_stop) and not read_from_shared_memory(self.end_thread):
                if sys.stdin in select.select([sys.stdin], [], [], 1)[0]:
                    char = sys.stdin.read(1)
                    if char == 'r':
                        self.send_stop_signal()
                    elif char == 'd':
                        self.send_depart_now_signal()
        except Exception as e:
            GLOBALS.logger.error(e)
        finally:
            return