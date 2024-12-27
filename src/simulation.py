import threading
import src.globals as GLOBALS
from src.objects.passenger import Passenger
from src.objects.ship import Ship
from src.objects.ship_captain import ShipCaptain

def handle_trip():
    # Passengers go to the bridge
    for passenger in GLOBALS.passengers:
        passenger.start_boarding()

    # Passengers going off the bridge
    for passenger in GLOBALS.passengers:
        passenger.thread.join()

    # The bridge is clear, ths ship can depart
    GLOBALS.ship.depart()

def simulation():
    GLOBALS.ship = Ship(GLOBALS.ship_capacity)
    GLOBALS.bridge_semaphore = threading.Semaphore(GLOBALS.bridge_capacity)
    GLOBALS.captain = ShipCaptain(GLOBALS.ship)
    GLOBALS.passengers = [Passenger(i + 1) for i in range(GLOBALS.passengers_num)]
    GLOBALS.boarding_allowed = threading.Event()

    # Iterate each ship trip
    while GLOBALS.trips_count < GLOBALS.max_trips:
        handle_trip()

        GLOBALS.trips_count += 1

    #
    # # Simulate passengers boarding the ship
    # for _ in range(5):
    #     GLOBALS.ship.board_passenger()
    #
    # # Start departure in a separate thread
    # def depart_ship():
    #     GLOBALS.captain.depart()
    #
    # departure_thread = threading.Thread(target=depart_ship)
    # departure_thread.start()
    #
    # # Simulate clearing the bridge
    # time.sleep(2)
    # with GLOBALS.bridge_semaphore:
    #     print("Manually clearing the bridge...")
    #
    # departure_thread.join()
    #
    # print("\nShipCaptain test completed.\n")