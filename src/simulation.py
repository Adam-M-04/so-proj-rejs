import threading
import src.globals as GLOBALS
import sys
import select

def read_input():
    """
    Reads input from the user to control the simulation.

    Listens for specific key presses:
    - 'r': Sends a stop signal to the port captain.
    - 'd': Sends a depart now signal to the port captain.
    """
    try:
        while GLOBALS.trips_count < GLOBALS.max_trips and not GLOBALS.port_captain.signal_stop.is_set():
            if sys.stdin in select.select([sys.stdin], [], [], 1)[0]:
                char = sys.stdin.read(1)
                if char == 'r':
                    GLOBALS.port_captain.send_stop_signal()
                elif char == 'd':
                    GLOBALS.port_captain.send_depart_now_signal()
    finally:
        return

def handle_trip():
    """
    Handles a single trip of the ship.
    Prepares the ship for the trip, manages the boarding process, and waits for the ship to return to port.
    """
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
    """
   Runs the simulation of ship trips until the maximum number of trips is reached or a stop signal is received.
   Handles the boarding, departure, and return of the ship for each trip.
   """

    input_thread = threading.Thread(target=read_input)
    input_thread.start()
    # Iterate each ship trip
    while GLOBALS.trips_count < GLOBALS.max_trips and not GLOBALS.port_captain.signal_stop.is_set():
        handle_trip()

        GLOBALS.trips_count += 1