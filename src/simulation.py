import threading
import src.globals as GLOBALS

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
    # Iterate each ship trip
    while GLOBALS.trips_count < GLOBALS.max_trips:
        handle_trip()

        GLOBALS.trips_count += 1