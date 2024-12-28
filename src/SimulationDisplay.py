import os
import time
import threading
import src.globals as GLOBALS
from src.objects.passenger import PassengerStatus

os.environ['TERM'] = 'xterm-256color'

class SimulationDisplay:
    def __init__(self, refresh_interval: float = 1):
        self.thread = None
        self.refresh_interval = refresh_interval
        self.stopped = threading.Event()

    def start(self):
        self.stopped.clear()
        self.thread = threading.Thread(target=self.display)
        self.thread.start()

    def stop(self):
        self.stopped.set()
        self.thread.join()

    def display(self):
        """
        Clear the terminal and display the updated simulation data.
        """
        while not self.stopped.is_set():
            self.update_display()
            time.sleep(self.refresh_interval)

    def update_display(self):
        # Clear terminal
        print("\033[H\033[J", end="")

        passengers_in_port = len([p for p in GLOBALS.passengers if p.status == PassengerStatus.AWAITING_BOARDING])
        passengers_on_bridge = len([p for p in GLOBALS.passengers if p.status == PassengerStatus.ON_BRIDGE])
        passengers_on_ship = len([p for p in GLOBALS.passengers if p.status == PassengerStatus.BOARDED])
        passengers_after_cruise = len([p for p in GLOBALS.passengers if p.status == PassengerStatus.FINISHED])
        total = GLOBALS.passengers_num

        print("\n=== PASAŻEROWIE W PORCIE ===")
        print("Port (oczekujący na rejs):")
        print(f"[{'X' * passengers_in_port}{' ' * (total - passengers_in_port)}] {passengers_in_port}/{total}")

        print("Mostek:")
        print(f"[{'X' * passengers_on_bridge}{' ' * (GLOBALS.bridge_capacity - passengers_on_bridge)}] {passengers_on_bridge}/{GLOBALS.bridge_capacity}")

        print("Statek:")
        print(f"[{'X' * passengers_on_ship}{' ' * (GLOBALS.ship_capacity - passengers_on_ship)}] {passengers_on_ship}/{GLOBALS.ship_capacity}")

        print("Port (po rejsie):")
        print(f"[{'X' * passengers_after_cruise}{' ' * (total - passengers_after_cruise)}] {passengers_after_cruise}/{total}")
        print("")