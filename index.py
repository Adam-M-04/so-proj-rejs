import threading
import src.globals as GLOBALS
from src.objects.passenger import Passenger

def main():
    num_passengers = 10
    bridge_capacity = 3

    GLOBALS.bridge_semaphore = threading.Semaphore(bridge_capacity)

    passengers = [Passenger(i) for i in range(1, num_passengers + 1)]

    print("Application starting...\n")

    for passenger in passengers:
        passenger.start()

    for passenger in passengers:
        passenger.join()

    print("\nApplication ended.")

if __name__ == "__main__":
    main()
