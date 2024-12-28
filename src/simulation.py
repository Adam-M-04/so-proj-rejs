import threading
import src.globals as GLOBALS

def handle_trip():
    GLOBALS.logger.log(f"#{GLOBALS.trips_count + 1} Rejs")
    GLOBALS.captain.allow_departure.clear()
    GLOBALS.ship.prepare_for_trip()

    # Set timer for the ship to depart
    threading.Timer(GLOBALS.ship_departing_interval, GLOBALS.ship.depart).start()

    # Passengers go to the bridge
    for passenger in GLOBALS.passengers:
        passenger.start_boarding()

    # Passengers going off the bridge
    for passenger in GLOBALS.passengers:
        passenger.thread.join()

    # The bridge is clear, ths ship can depart
    GLOBALS.captain.depart()

    # Wait for the ship to return to the port
    GLOBALS.ship.return_event.wait()
    # Cycle is over

def simulation():
    # Iterate each ship trip
    while GLOBALS.trips_count < GLOBALS.max_trips and not GLOBALS.port_captain.signal_stop.is_set():
        handle_trip()

        GLOBALS.trips_count += 1