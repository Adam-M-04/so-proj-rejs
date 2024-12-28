import threading
import time

from src.stop_boarding_passengers import stop_boarding_passengers


class Ship:
    cruise_duration = 5 # in seconds
    cruise_in_progress = False

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
        if len(self.boarded_passengers) == 0:
            print("Statek pusty, rejs odwołany", flush=True)
            return

        print("Statek wypływa z portu.", flush=True)
        self.return_event.clear()
        self.cruise_in_progress = True
        threading.Timer(Ship.cruise_duration, self.return_to_port).start()
        return

    def return_to_port(self):
        """
        Returns the ship to port.
        """
        if self.cruise_in_progress:
            self.cruise_in_progress = False
            print("Statek wrócił do portu.", flush=True)
            self.unload_all_passengers()
            self.return_event.set()
        return