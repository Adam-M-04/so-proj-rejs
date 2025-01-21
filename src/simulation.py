import multiprocessing
import src.globals as GLOBALS

from src.SimulationDisplay import SimulationDisplay
from src.objects.Bridge import enter_bridge
from src.objects.passenger import passenger
from src.objects.ship_captain import ship_captain


def simulation(display: SimulationDisplay):
    """
    Runs the simulation with the given display.

    :param display: The SimulationDisplay instance to use for displaying the simulation.
    """
    manager = multiprocessing.Manager()
    passengers_in_port: manager.List[int] = manager.list(range(1, GLOBALS.passengers_num + 1))
    passengers_on_bridge = manager.Queue(maxsize=GLOBALS.bridge_capacity)
    passengers_walking_bridge: manager.List[int] = manager.list([])
    passengers_on_ship = manager.list()
    passengers_after_trip = manager.list()

    # True - boarding ship, False - leaving ship
    bridge_direction = multiprocessing.Value('b', True)
    bridge_semaphore = manager.Semaphore(GLOBALS.bridge_capacity)
    ship_lock = manager.Lock()
    trips_count = multiprocessing.Value('i', 0)
    trip_completed = multiprocessing.Value('b', True)
    trip_time_tracker = multiprocessing.Value('d', -1)
    bridge_cleared = manager.Event()
    bridge_close = multiprocessing.Event()

    GLOBALS.port_captain.start()

    display.start(passengers_in_port, passengers_on_bridge, passengers_walking_bridge, passengers_on_ship, passengers_after_trip, trip_time_tracker)

    processes = []

    # Create the bridge process
    processes.append(multiprocessing.Process(target=enter_bridge, args=(
        passengers_on_bridge, GLOBALS.port_captain.boarding_allowed, passengers_on_ship, GLOBALS.ship_capacity, ship_lock, passengers_in_port,
        bridge_semaphore, bridge_direction, passengers_after_trip, passengers_walking_bridge, bridge_cleared, GLOBALS.logger.get_queue(), bridge_close, trip_completed)))
    # Create the ship process
    processes.append(multiprocessing.Process(target=ship_captain, name='ship', args=(
        passengers_on_ship, GLOBALS.max_trips, GLOBALS.trip_time, GLOBALS.ship_departing_interval, GLOBALS.port_captain.boarding_allowed, passengers_on_bridge,
        bridge_direction, bridge_semaphore, bridge_cleared, trips_count, GLOBALS.logger.get_queue(), GLOBALS.port_captain.signal_stop, bridge_close, trip_completed, trip_time_tracker)))

    # Create passenger processes
    for passenger_id in passengers_in_port:
        processes.append(multiprocessing.Process(target=passenger, args=(
            passenger_id, passengers_in_port, bridge_semaphore, passengers_on_bridge, GLOBALS.port_captain.boarding_allowed,
            passengers_after_trip, GLOBALS.logger.get_queue(), bridge_close)))

    # Start processes
    for process in processes:
        process.start()

    # Wait for processes to finish
    for process in processes:
        process.join()

    GLOBALS.port_captain.stop()
