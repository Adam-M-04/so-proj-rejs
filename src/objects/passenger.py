import threading
import time
import random
import src.globals as GLOBALS
from enum import Enum

from src.LogService import BaseLogger


class PassengerStatus(Enum):
    AWAITING_BOARDING = 1
    BOARDED = 2
    ON_BRIDGE = 3
    FINISHED = 4

class Passenger(BaseLogger):
    def __init__(self, passenger_id):
        """
        Initializes passenger with a given passenger id.
        :param passenger_id: ID of the passenger.
        """
        super().__init__("Pasażer")
        self.passenger_id = passenger_id
        self.trip_completed = False
        self.status = PassengerStatus.AWAITING_BOARDING
        self._stop_event = threading.Event()
        self.thread = None

    @staticmethod
    def simulate_board_walk():
        """ Simulate boarding time """
        time.sleep(random.uniform(1, 3))

    def attempt_boarding(self):
        """
        Attempts to board the passenger onto the ship.
        Acquires the bridge semaphore, simulates the boarding walk, and updates the passenger status.
        """
        try:
            self.log(f"Pasażer {self.passenger_id} czeka na wejście na mostek.")
            GLOBALS.bridge_semaphore.acquire()

            if not self.is_stopped():
                self.status = PassengerStatus.ON_BRIDGE
                self.log(f"Pasażer {self.passenger_id} wchodzi na mostek.")

                self.simulate_board_walk()
                if not self.is_stopped() and GLOBALS.ship.board_passenger(self):
                    self.status = PassengerStatus.BOARDED

        finally:
            GLOBALS.bridge_semaphore.release()
            if self.status != PassengerStatus.BOARDED:
                self.status = PassengerStatus.AWAITING_BOARDING

    def stop_boarding(self):
        """
        Stops the boarding process for the passenger by setting the stop event.
        """
        self._stop_event.set()
        # GLOBALS.bridge_semaphore.release()

    def start_boarding(self):
        """
        Starts the boarding process for the passenger by clearing the stop event and starting a new thread.
        """
        if self.is_boarded():
            return
        self._stop_event.clear()
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def is_boarded(self):
        """
        Checks if the passenger has boarded the ship.

        :return: True if the passenger has boarded, False otherwise.
        """
        return self.status != PassengerStatus.AWAITING_BOARDING

    def offboarding(self):
        """
        Offboards the passenger from the ship.
        Acquires the bridge semaphore, simulates the offboarding walk, and updates the passenger status.
        """
        try:
            self.log(f"Pasażer {self.passenger_id} czeka na zejście ze statku.")
            GLOBALS.bridge_semaphore.acquire()
            self.status = PassengerStatus.ON_BRIDGE

            GLOBALS.ship.offboard_passenger(self)
            self.simulate_board_walk()
            self.status = PassengerStatus.FINISHED if self.trip_completed else PassengerStatus.AWAITING_BOARDING
            self.log(f"Pasażer {self.passenger_id} schodzi z mostku.")
        finally:
            GLOBALS.bridge_semaphore.release()

    def start_offboarding(self):
        """
        Starts the offboarding process for the passenger by clearing the stop event and starting a new thread.
        """
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
        """
        Checks if the passenger is waiting for boarding and not stopped.

        :return: True if the passenger is waiting for boarding and not stopped, False otherwise.
        """
        return not self.is_stopped() and not self.is_boarded()

    def run(self):
        """
        Runs the boarding process for the passenger.
        """
        try:
            if not self.is_boarded():
                self.attempt_boarding()
        except Exception as e:
            GLOBALS.logger.error(e)
