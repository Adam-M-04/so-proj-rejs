import os
import time
import threading
import src.globals as GLOBALS

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
            time.sleep(self.refresh_interval)

    @staticmethod
    def clear():
        """
        Clears the terminal.
        """
        print("\033[H\033[J", end="")

    def print_actions(self):
        print("\n=== AKCJE ===")
        print("r + enter - zatrzymaj rejs")
        print("d + enter - natychmiastowy odpływ")

    def update_display(self, passengers_in_port, passengers_on_bridge, passengers_walking_bridge, passengers_on_ship, passengers_after_trip):
        """
        Clears the terminal and displays the updated simulation data.
        """
        self.clear()
        self.print_actions()

        passengers_in_port = len(passengers_in_port)
        passengers_on_bridge = len(passengers_walking_bridge) + passengers_on_bridge.qsize()
        passengers_on_ship = len(passengers_on_ship)
        passengers_after_cruise = len(passengers_after_trip)
        total = GLOBALS.passengers_num

        print("\n=== PASAŻEROWIE W PORCIE ===")
        print("\nPort (oczekujący na rejs)")
        print(f"[{'X' * passengers_in_port}{' ' * (total - passengers_in_port)}] {passengers_in_port}/{total}")

        print("\nMostek")
        print(f"[{'X' * passengers_on_bridge}{' ' * (GLOBALS.bridge_capacity - passengers_on_bridge)}] {passengers_on_bridge}/{GLOBALS.bridge_capacity}")

        print(f"\nStatek")
        print(f"[{'X' * passengers_on_ship}{' ' * (GLOBALS.ship_capacity - passengers_on_ship)}] {passengers_on_ship}/{GLOBALS.ship_capacity}")

        print("\nPort (po rejsie)")
        print(f"[{'X' * passengers_after_cruise}{' ' * (total - passengers_after_cruise)}] {passengers_after_cruise}/{total}")
