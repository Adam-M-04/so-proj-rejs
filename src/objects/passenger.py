import threading
import time
import random
import src.globals as GLOBALS
from enum import Enum

class PassengerStatus(Enum):
    AWAITING_BOARDING = 1
    BOARDED = 2
    ON_BRIDGE = 3
    FINISHED = 4

class Passenger:
    def __init__(self, passenger_id):
        """
        Initializes passenger with a given passenger id.
        :param passenger_id: ID of the passenger.
        """
        super().__init__()
        self.passenger_id = passenger_id
        self.status = PassengerStatus.AWAITING_BOARDING
        self._stop_event = threading.Event()
        self.thread = None

    @staticmethod
    def simulate_board_walk():
        """ Simulate boarding time """
        time.sleep(random.uniform(1, 3))

    def attempt_boarding(self):
        try:
            print(f"Pasażer {self.passenger_id} czeka na wejście na mostek.", flush=True)
            GLOBALS.bridge_semaphore.acquire()

            if not self.is_stopped():
                print(f"Pasażer {self.passenger_id} wchodzi na mostek.", flush=True)

                self.simulate_board_walk()
                if not self.is_stopped() and GLOBALS.ship.board_passenger(self):
                    self.status = PassengerStatus.BOARDED

        finally:
            GLOBALS.bridge_semaphore.release()

    def stop_boarding(self):
        self._stop_event.set()
        # GLOBALS.bridge_semaphore.release()

    def start_boarding(self):
        self._stop_event.clear()
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def is_boarded(self):
        return self.status != PassengerStatus.AWAITING_BOARDING

    def offboarding(self):
        try:
            print(f"Pasażer {self.passenger_id} czeka na zejście ze statku.", flush=True)
            GLOBALS.bridge_semaphore.acquire()

            GLOBALS.ship.offboard_passenger(self)
            self.simulate_board_walk()
            self.status = PassengerStatus.FINISHED
            print(f"Pasażer {self.passenger_id} schodzi z mostku.", flush=True)
        finally:
            GLOBALS.bridge_semaphore.release()

    def start_offboarding(self):
        self._stop_event.clear()
        self.thread = threading.Thread(target=self.offboarding)
        self.thread.start()

    def is_stopped(self):
        """
        Checks if the stop event is set.
        :return: True if the stop event is set, False otherwise.
        """
        return self._stop_event.is_set()

    def waiting_for_boarding(self):
        return not self.is_stopped() and not self.is_boarded()

    def run(self):
        if not self.is_boarded():
            self.attempt_boarding()
