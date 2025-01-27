import os
import multiprocessing
import src.globals as GLOBALS

from src.SimulationDisplay import SimulationDisplay
from src.objects.Bridge import enter_bridge
from src.objects.SharedMemory import create_shared_memory, write_to_shared_memory, append_to_shared_memory
from src.objects.passenger import passenger
from src.objects.ship_captain import ship_captain


def simulation(display: SimulationDisplay):
    """
    Runs the simulation with the given display.

    :param display: The SimulationDisplay instance to use for displaying the simulation.
    """
    # Shared memory for lists and values
    passengers_in_port_shm = create_shared_memory(GLOBALS.passengers_num)
    passengers_on_bridge_r, passengers_on_bridge_w = multiprocessing.Pipe(duplex=True)
    passengers_walking_bridge_shm = create_shared_memory(GLOBALS.bridge_capacity)
    passengers_on_ship_shm = create_shared_memory(GLOBALS.ship_capacity)
    passengers_after_trip_shm = create_shared_memory(GLOBALS.passengers_num)

    bridge_direction_shm = create_shared_memory(1)
    trips_count_shm = create_shared_memory(1)
    trip_completed_shm = create_shared_memory(1)
    trip_time_tracker_shm = create_shared_memory(2)

    # Initialize shared memory values
    write_to_shared_memory(bridge_direction_shm, 0, 1)
    write_to_shared_memory(trips_count_shm, 0, 0)
    write_to_shared_memory(trip_completed_shm, 0, 1)
    write_to_shared_memory(trip_time_tracker_shm, 0, -1, 'd')

    # Semaphore and event
    bridge_semaphore = multiprocessing.Semaphore(GLOBALS.bridge_capacity)
    ship_lock = multiprocessing.Lock()
    bridge_cleared = multiprocessing.Event()
    bridge_cleared.set()
    bridge_close = multiprocessing.Event()

    GLOBALS.port_captain.start()

    display.start(passengers_in_port_shm, passengers_on_bridge_r, passengers_walking_bridge_shm, passengers_on_ship_shm, passengers_after_trip_shm, trip_time_tracker_shm)

    processes = []

    def fork_process(target, args):
        pid = os.fork()
        if pid == 0:
            target(*args)
            os._exit(0)
        else:
            return pid

    # Create the bridge process
    processes.append(fork_process(enter_bridge, (
        passengers_on_bridge_r, GLOBALS.port_captain.boarding_allowed, passengers_on_ship_shm, GLOBALS.ship_capacity,
        ship_lock, passengers_in_port_shm,
        bridge_semaphore, bridge_direction_shm, passengers_after_trip_shm, passengers_walking_bridge_shm,
        bridge_cleared, GLOBALS.logger.log, bridge_close, trip_completed_shm)))

    # Create the ship process
    processes.append(fork_process(ship_captain, (
        passengers_on_ship_shm, GLOBALS.max_trips, GLOBALS.trip_time, GLOBALS.ship_departing_interval,
        GLOBALS.port_captain.boarding_allowed, passengers_on_bridge_w,
        bridge_direction_shm, bridge_semaphore, bridge_cleared, trips_count_shm, GLOBALS.logger.log,
        GLOBALS.port_captain.signal_stop, bridge_close, trip_completed_shm, trip_time_tracker_shm)))

    # Create passenger processes
    for i in range(GLOBALS.passengers_num):
        append_to_shared_memory(passengers_in_port_shm, i + 1)
        processes.append(fork_process(passenger, (
            i + 1, passengers_in_port_shm, bridge_semaphore, passengers_on_bridge_w, GLOBALS.port_captain.boarding_allowed,
            passengers_after_trip_shm, GLOBALS.logger.log, bridge_close)))

    for pid in processes:
        os.waitpid(pid, 0)

    # Close shared memory
    passengers_in_port_shm.close()
    os.close(passengers_on_bridge_r)
    os.close(passengers_on_bridge_w)
    passengers_walking_bridge_shm.close()
    passengers_on_ship_shm.close()
    passengers_after_trip_shm.close()
    bridge_direction_shm.close()
    trips_count_shm.close()
    trip_completed_shm.close()
    trip_time_tracker_shm.close()

    # GLOBALS.port_captain.stop()
