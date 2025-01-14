import threading
import time

import src.globals as GLOBALS
from enum import Enum

from src.LogService import BaseLogger
from src.ReaderService import ReaderService
from src.stop_boarding_passengers import stop_boarding_passengers

class ShipStatus(Enum):
    BOARDING_IN_PROGRESS = 1
    DEPARTING = 2
    IN_CRUISE = 3
    OFFBOARDING = 4

class Ship(BaseLogger):
    status = ShipStatus.BOARDING_IN_PROGRESS

    def __init__(self, capacity):
        """
        Initializes the ship with a given passenger capacity.
        :param capacity: Maximum number of passengers the ship can hold.
        """
        super().__init__("Statek")
        self.cruise_duration = int(ReaderService.read_number(1, 3600, "Podaj ile sekund trwa rejs", 10))
        self.capacity = capacity
        self.boarded_passengers = []
        self.lock = threading.Lock()
        self.return_event = threading.Event()
        self.departure_time = None

    def board_passenger(self, passenger):
        """
        Attempts to add a passenger to the ship.
        :return: True if boarding was successful, False if the ship is full.
        """
        with self.lock:
            if not self.is_full():
                self.boarded_passengers.append(passenger)
                self.log(f"Pasażer {passenger.passenger_id} wszedł na statek. Obecny stan: {self.str_state()}.")
                return True
            else:
                self.log("Statek jest pełny. Pasażer nie może wejść.")
                stop_boarding_passengers()
                return False

    def offboard_passenger(self, passenger):
        """
        Remove a passenger from the ship.
        """
        with self.lock:
            if passenger in self.boarded_passengers:
                self.boarded_passengers.remove(passenger)
                self.log(f"Pasażer {passenger.passenger_id} schodzi na mostek. Obecny stan: {self.str_state()}.")

    def str_state(self):
        """
        Returns the current state of the ship in terms of boarded passengers.

        :return: A string representing the number of boarded passengers and the ship's capacity. Example: "5/10"
        """
        return f"{len(self.boarded_passengers)}/{self.capacity}"

    def unload_all_passengers(self, trip_success=True):
        """
        Removes all passengers from the ship.
        """
        self.log(f"Wszyscy pasażerowie wysiadają.")
        tmp_boarded = self.boarded_passengers.copy()
        for passenger in tmp_boarded:
            passenger.trip_completed = trip_success
            passenger.start_offboarding()

        for passenger in tmp_boarded:
            passenger.thread.join()

    def is_full(self):
        """
        Checks if the ship is full.
        :return: True if the ship is full, False otherwise.
        """
        return len(self.boarded_passengers) >= self.capacity

    def depart(self):
        """
        Initiates the departure process.
        """
        if self.status != ShipStatus.BOARDING_IN_PROGRESS or GLOBALS.port_captain.signal_stop.is_set():
            return
        self.log("Czas na odpłynięcie.")
        self.status = ShipStatus.DEPARTING
        stop_boarding_passengers()
        GLOBALS.captain.allow_departure.wait()
        if len(self.boarded_passengers) == 0:
            self.log("Statek pusty, rejs odwołany")
            self.return_event.set()
            return

        self.log(f"Statek wypływa z portu. {len(self.boarded_passengers)} pasażerów na pokładzie")
        self.status = ShipStatus.IN_CRUISE
        self.departure_time = time.time()
        threading.Timer(GLOBALS.ship.cruise_duration, self.return_to_port).start()
        return

    def return_to_port(self):
        """
        Returns the ship to port.
        """
        if self.status == ShipStatus.IN_CRUISE:
            self.status = ShipStatus.OFFBOARDING
            self.log("Statek wrócił do portu.")
            self.unload_all_passengers()
            self.return_event.set()
            self.departure_time = None
        return

    def prepare_for_trip(self):
        """
        Prepares the ship for a new trip by setting the status to boarding in progress and clearing the return event.
        """
        self.status = ShipStatus.BOARDING_IN_PROGRESS
        self.return_event.clear()

    def get_trip_progress(self):
        """
        Gets the progress of the current trip.

        :return: The elapsed time of the trip if in cruise, otherwise 0.
        """
        if self.status == ShipStatus.IN_CRUISE and self.departure_time:
            elapsed_time = time.time() - self.departure_time
            return min(elapsed_time, GLOBALS.ship.cruise_duration)
        return 0

    def print_ship_status(self):
        """
        Prints the current status of the ship.
        """
        if self.status == ShipStatus.IN_CRUISE:
            progress = self.get_trip_progress()
            return f"trwa rejs {progress:.1f}s/{self.cruise_duration}s"
        if self.status == ShipStatus.BOARDING_IN_PROGRESS:
            return "załadunek pasażerów"
        if self.status == ShipStatus.DEPARTING:
            return "czas odpływać"
        if self.status == ShipStatus.OFFBOARDING:
            return "pasażerowie wysiadają"