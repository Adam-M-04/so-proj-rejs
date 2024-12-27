import threading
import time
import random
import src.globals as GLOBALS

class Passenger(threading.Thread):
    def __init__(self, passenger_id):
        """
        Initializes passenger with a given passenger id.
        :param passenger_id: ID of the passenger.
        """
        super().__init__()
        self.passenger_id = passenger_id
        self.boarded = False
        self._stop_event = threading.Event()

    def attempt_boarding(self):
        try:
            print(f"Pasażer {self.passenger_id} czeka na wejście na mostek.")
            GLOBALS.bridge_semaphore.acquire()
            if not self.is_stopped():
                print(f"Pasażer {self.passenger_id} wchodzi na mostek.")

                """ Simulate boarding time """
                time.sleep(random.uniform(0.1, 0.5))
                if not self.is_stopped() and GLOBALS.ship.board_passenger(self):
                    self.boarded = True

        finally:
            GLOBALS.bridge_semaphore.release()

    def stop_boarding(self):
        self._stop_event.set()
        GLOBALS.bridge_semaphore.release()

    def start_boarding(self):
        self._stop_event.clear()
        self.start()

    def is_stopped(self):
        """
        Checks if the stop event is set.
        :return: True if the stop event is set, False otherwise.
        """
        return self._stop_event.is_set()

    def waiting_for_boarding(self):
        return self.is_alive() and not self.is_stopped() and not self.boarded

    def run(self):
        if not self.boarded:
            self.attempt_boarding()
