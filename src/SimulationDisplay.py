import os
import time
from time import sleep
import threading
import src.globals as GLOBALS

from src.objects.SharedMemory import count_passengers_in_shared_memory, read_from_shared_memory

os.environ['TERM'] = 'xterm-256color'


class SimulationDisplay:
    def __init__(self, refresh_interval: float = 1):
        """
        Initializes the SimulationDisplay with a given refresh interval.

        :param refresh_interval: Time interval (in seconds) between display refreshes.
        """
        self.thread = None
        self.refresh_interval = refresh_interval
        self.stopped = threading.Event()

    def start(self, *args):
        """
        Starts the display thread.
        """
        self.stopped.clear()
        self.thread = threading.Thread(target=self.display, args=args)
        self.thread.start()

    def stop(self):
        """
        Stops the display thread.
        """
        self.stopped.set()
        self.thread.join()

    def display(self, *args):
        """
        Continuously updates the display until stopped.
        """
        while not self.stopped.is_set():
            self.update_display(*args)
            sleep(self.refresh_interval)

    @staticmethod
    def clear():
        """
        Clears the terminal.
        """
        print("\033[H\033[J", end="")

    def print_actions(self):
        """
        Prints the available actions for the user.
        """
        print("\n=== AKCJE ===")
        print("r + enter - zatrzymaj rejs")
        print("d + enter - natychmiastowy odpływ")

    def update_display(self, passengers_in_port, passengers_on_bridge_r, passengers_walking_bridge, passengers_on_ship, passengers_after_trip, trip_time_tracker):
        """
        Clears the terminal and displays the updated simulation data.

        :param passengers_in_port: Shared memory object for passengers in port.
        :param passengers_on_bridge_r: Shared memory object for passengers on bridge (read end).
        :param passengers_walking_bridge: Shared memory object for passengers walking on the bridge.
        :param passengers_on_ship: Shared memory object for passengers on the ship.
        :param passengers_after_trip: Shared memory object for passengers after the trip.
        :param trip_time_tracker: Shared memory object for tracking trip time.
        """
        try:
            self.clear()
            self.print_actions()

            passengers_in_port = count_passengers_in_shared_memory(passengers_in_port)
            passengers_on_bridge = count_passengers_in_shared_memory(passengers_walking_bridge)
            passengers_on_ship = count_passengers_in_shared_memory(passengers_on_ship)
            passengers_after_cruise = count_passengers_in_shared_memory(passengers_after_trip)
            total = GLOBALS.passengers_num

            print("\n=== PASAŻEROWIE W PORCIE ===")
            print("\nPort (oczekujący na rejs)")
            print(f"[{'X' * passengers_in_port}{' ' * (total - passengers_in_port)}] {passengers_in_port}/{total}")

            print("\nMostek")
            print(f"[{'X' * passengers_on_bridge}{' ' * (GLOBALS.bridge_capacity - passengers_on_bridge)}] {passengers_on_bridge}/{GLOBALS.bridge_capacity}")

            trip_time_value = read_from_shared_memory(trip_time_tracker, 'd')
            if trip_time_value > 0:
                trip_time_value = round(time.time() - trip_time_value, 1)
            else:
                trip_time_value = -1
            print(f"\nStatek {f'(trwa rejs: {trip_time_value}/{GLOBALS.trip_time}s)' if (0 <= trip_time_value <= GLOBALS.trip_time) else ''}")
            print(f"[{'X' * passengers_on_ship}{' ' * (GLOBALS.ship_capacity - passengers_on_ship)}] {passengers_on_ship}/{GLOBALS.ship_capacity}")

            print("\nPort (po rejsie)")
            print(f"[{'X' * passengers_after_cruise}{' ' * (total - passengers_after_cruise)}] {passengers_after_cruise}/{total}")
        except:
            self.stop()