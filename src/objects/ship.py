import threading
import src.globals as GLOBALS
from enum import Enum

from src.stop_boarding_passengers import stop_boarding_passengers

class ShipStatus(Enum):
    BOARDING_IN_PROGRESS = 1
    DEPARTING = 2
    IN_CRUISE = 3
    OFFBOARDING = 4

class Ship:
    cruise_duration = 5 # in seconds
    status = ShipStatus.BOARDING_IN_PROGRESS

    def __init__(self, capacity):
        """
        Initializes the ship with a given passenger capacity.
        :param capacity: Maximum number of passengers the ship can hold.
        """
        self.capacity = capacity
        self.boarded_passengers = []
        self.lock = threading.Lock()
        self.return_event = threading.Event()

    def board_passenger(self, passenger):
        """
        Attempts to add a passenger to the ship.
        :return: True if boarding was successful, False if the ship is full.
        """
        with self.lock:
            if not self.is_full():
                self.boarded_passengers.append(passenger)
                print(f"Pasażer {passenger.passenger_id} wszedł na statek. Obecny stan: {self.str_state()}.", flush=True)
                return True
            else:
                print("Statek jest pełny. Pasażer nie może wejść.", flush=True)
                stop_boarding_passengers()
                return False

    def offboard_passenger(self, passenger):
        """
        Remove a passenger from the ship.
        """
        with self.lock:
            if passenger in self.boarded_passengers:
                self.boarded_passengers.remove(passenger)
                print(f"Pasażer {passenger.passenger_id} schodzi na mostek. Obecny stan: {self.str_state()}.", flush=True)

    def str_state(self):
        return f"{len(self.boarded_passengers)}/{self.capacity}"

    def unload_all_passengers(self):
        """
        Removes all passengers from the ship.
        """
        print(f"Wszyscy pasażerowie wysiadają.", flush=True)
        tmp_boarded = self.boarded_passengers.copy()
        for passenger in tmp_boarded:
            passenger.start_offboarding()

        for passenger in tmp_boarded:
            passenger.thread.join()

        self.boarded_passengers = []

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
        print("\nCzas na odpłynięcie.", flush=True)
        self.status = ShipStatus.DEPARTING
        stop_boarding_passengers()
        GLOBALS.captain.allow_departure.wait()
        if len(self.boarded_passengers) == 0:
            print("Statek pusty, rejs odwołany", flush=True)
            return

        print(f"Statek wypływa z portu. {len(self.boarded_passengers)} pasażerów na pokładzie", flush=True)
        self.status = ShipStatus.IN_CRUISE
        threading.Timer(Ship.cruise_duration, self.return_to_port).start()
        return

    def return_to_port(self):
        """
        Returns the ship to port.
        """
        if self.status == ShipStatus.IN_CRUISE:
            self.status = ShipStatus.OFFBOARDING
            print("\nStatek wrócił do portu.", flush=True)
            self.unload_all_passengers()
            self.return_event.set()
        return

    def prepare_for_trip(self):
        self.status = ShipStatus.BOARDING_IN_PROGRESS
        self.return_event.clear()