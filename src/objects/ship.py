import threading

class Ship:
    def __init__(self, capacity):
        """
        Initializes the ship with a given passenger capacity.
        :param capacity: Maximum number of passengers the ship can hold.
        """
        self.capacity = capacity
        self.onboard = 0
        self.lock = threading.Lock()

    def board_passenger(self):
        """
        Attempts to add a passenger to the ship.
        :return: True if boarding was successful, False if the ship is full.
        """
        with self.lock:
            if not self.is_full():
                self.onboard += 1
                print(f"Passenger boarded the ship. Current onboard: {self.onboard}/{self.capacity}.")
                return True
            else:
                print("Ship is full. Passenger cannot board.")
                return False

    def unload_all_passengers(self):
        """
        Removes all passengers from the ship.
        """
        with self.lock:
            print(f"Unloading all passengers. {self.onboard} passengers are leaving the ship.")
            self.onboard = 0

    def is_full(self):
        """
        Checks if the ship is full.
        :return: True if the ship is full, False otherwise.
        """
        with self.lock:
            return self.onboard >= self.capacity
