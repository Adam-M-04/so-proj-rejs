import threading
import time
import random
import src.globals as GLOBALS

class Passenger(threading.Thread):
    def __init__(self, passenger_id):
        super().__init__()
        self.passenger_id = passenger_id
        self.boarded = False

    def attempt_boarding(self):
        try:
            print(f"Pasażer {self.passenger_id} czeka na wejście na mostek.")
            GLOBALS.bridge_semaphore.acquire()
            print(f"Pasażer {self.passenger_id} wchodzi na mostek.")

            """ Simulate boarding time """
            time.sleep(random.uniform(0.1, 0.5))
            self.boarded = True

            print(f"Pasażer {self.passenger_id} wszedł na statek.")
        finally:
            GLOBALS.bridge_semaphore.release()

    def run(self):
        self.attempt_boarding()
