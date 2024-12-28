import threading
import src.globals as GLOBALS
from src.objects.passenger import Passenger
from src.objects.ship import Ship
from src.objects.ship_captain import ShipCaptain

def handle_trip():
    print(f"\n#{GLOBALS.trips_count + 1} Rejs")
    # Set timer for the ship to depart
    threading.Timer(GLOBALS.ship_departing_interval, GLOBALS.ship.depart).start()
    GLOBALS.captain.allow_departure.clear()
    GLOBALS.ship.return_event.clear()

    # Passengers go to the bridge
    for passenger in GLOBALS.passengers:
        passenger.start_boarding()

    # Passengers going off the bridge
    for passenger in GLOBALS.passengers:
        passenger.thread.join()

    # The bridge is clear, ths ship can depart
    GLOBALS.captain.depart()

    # The ship has returned to port
    GLOBALS.ship.return_event.wait()

def simulation():
    GLOBALS.ship = Ship(GLOBALS.ship_capacity)
    GLOBALS.bridge_semaphore = threading.Semaphore(GLOBALS.bridge_capacity)
    GLOBALS.captain = ShipCaptain()
    GLOBALS.passengers = [Passenger(i + 1) for i in range(GLOBALS.passengers_num)]
    GLOBALS.boarding_allowed = threading.Event()

    # Iterate each ship trip
    while GLOBALS.trips_count < GLOBALS.max_trips:
        handle_trip()

        GLOBALS.trips_count += 1