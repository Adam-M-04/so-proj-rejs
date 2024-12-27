import threading

from src.stop_boarding_passengers import stop_boarding_passengers


class Ship:
    def __init__(self, capacity):
        """
        Initializes the ship with a given passenger capacity.
        :param capacity: Maximum number of passengers the ship can hold.
        """
        self.capacity = capacity
        self.boarded_passengers = []
        self.lock = threading.Lock()

    def board_passenger(self, passenger):
        """
        Attempts to add a passenger to the ship.
        :return: True if boarding was successful, False if the ship is full.
        """
        with self.lock:
            if not self.is_full():
                self.boarded_passengers.append(passenger)
                print(f"Pasażer {passenger.passenger_id} wszedł na statek. Obecny stan: {len(self.boarded_passengers)}/{self.capacity}.")
                return True
            else:
                print("Statek jest pełny. Pasażer nie może wejść.")
                stop_boarding_passengers()
                return False

    def unload_all_passengers(self):
        """
        Removes all passengers from the ship.
        """
        with self.lock:
            print(f"Wszyscy pasażerowie wysiadają. {len(self.boarded_passengers)} pasażerów wychodzi ze statku.")
            self.boarded_passengers = []

    def is_full(self):
        """
        Checks if the ship is full.
        :return: True if the ship is full, False otherwise.
        """
        return len(self.boarded_passengers) >= self.capacity
