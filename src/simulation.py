import multiprocessing
import threading
import src.globals as GLOBALS
import sys
import select

from src.objects.Bridge import enter_bridge
from src.objects.passenger import passenger
from src.objects.ship import ship


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
    except Exception as e:
        GLOBALS.logger.error(e)
    finally:
        return

def simulation():
    """
   Runs the simulation of ship trips until the maximum number of trips is reached or a stop signal is received.
   Handles the boarding, departure, and return of the ship for each trip.
   """
    # try:
    #     input_thread = threading.Thread(target=read_input)
    #     input_thread.start()
    #     # Iterate each ship trip
    #     while GLOBALS.trips_count < GLOBALS.max_trips and not GLOBALS.port_captain.signal_stop.is_set():
    #         handle_trip()
    #
    #         GLOBALS.trips_count += 1
    # except Exception as e:
    #     GLOBALS.logger.error(e)

    manager = multiprocessing.Manager()
    passengers_in_port: manager.List[int] = manager.list(range(1, GLOBALS.passengers_num + 1))
    passengers_on_bridge = manager.Queue(maxsize=GLOBALS.bridge_capacity)
    passengers_walking_bridge: manager.List[int] = manager.list([])
    passengers_on_ship = manager.list()
    passengers_after_trip = manager.list()
    boarding_allowed = multiprocessing.Value('b', False)
    # True - boarding ship, False - leaving ship
    bridge_direction = multiprocessing.Value('b', True)
    bridge_semaphore = manager.Semaphore(GLOBALS.bridge_capacity)
    ship_lock = manager.Lock()
    trips_count = multiprocessing.Value('i', 0)
    bridge_cleared = manager.Event()

    processes = []

    processes.append(multiprocessing.Process(target=enter_bridge, args=(
        passengers_on_bridge, boarding_allowed, passengers_on_ship, GLOBALS.ship_capacity, ship_lock, passengers_in_port,
        bridge_semaphore,
        bridge_direction, passengers_after_trip, passengers_walking_bridge, bridge_cleared, trips_count)))
    processes.append(multiprocessing.Process(target=ship, args=(
        passengers_on_ship, GLOBALS.max_trips, GLOBALS.trip_time, GLOBALS.ship_departing_interval, boarding_allowed, passengers_on_bridge,
        bridge_direction, bridge_semaphore, bridge_cleared, trips_count)))

    # Passengers go to the bridge
    for passenger_id in passengers_in_port:
        process = multiprocessing.Process(target=passenger, args=(
        passenger_id, passengers_in_port, bridge_semaphore, passengers_on_bridge, boarding_allowed,
        passengers_after_trip))
        processes.append(process)

    for process in processes:
        process.start()

    for process in processes:
        process.join()

