import time
from time import sleep
import struct
from src.SimulationDisplay import count_passengers_in_shared_memory
from src.objects.SharedMemory import read_from_shared_memory, write_to_shared_memory, remove_from_shared_memory, shared_memory_to_array


def is_signal_stop_set(shared_memory):
    """
    Checks if the stop signal is set in the shared memory.

    Args:
        shared_memory (mmap.mmap): The shared memory object.

    Returns:
        bool: True if the stop signal is set, False otherwise.
    """
    shared_memory.seek(0)
    return struct.unpack('b', shared_memory.read(1))[0] == 1

def ship_captain(passengers_on_ship, max_trips, trip_time, ship_departing_interval, boarding_allowed, passengers_on_bridge_w, bridge_direction, bridge_semaphore, bridge_cleared, trips_count, log_method, signal_stop, bridge_close, trip_completed, trip_time_tracker):
    """
    Manages the boarding of passengers on the ship and the execution of trips.

    Args:
        passengers_on_ship (mmap.mmap): Shared memory for passengers currently on the ship.
        max_trips (int): Maximum number of trips the ship will make.
        trip_time (float): Duration of each trip in seconds.
        ship_departing_interval (float): Time interval for boarding before the ship departs.
        boarding_allowed (mmap.mmap): Shared memory for the flag indicating if boarding is allowed.
        passengers_on_bridge_w (int): File descriptor for reading passengers waiting to enter the bridge.
        bridge_direction (mmap.mmap): Shared memory for the direction of the bridge (True for boarding, False for disembarking).
        bridge_semaphore (multiprocessing.Semaphore): Semaphore to control access to the bridge.
        bridge_cleared (multiprocessing.Event): Event to signal that the bridge is cleared.
        trips_count (mmap.mmap): Shared memory for the number of trips completed.
        log_method (function): Logging method from Log service.
        signal_stop (mmap.mmap): Shared memory for the flag indicating if the stop signal is set.
        bridge_close (multiprocessing.Event): Event to signal that the bridge is closed.
        trip_completed (mmap.mmap): Shared memory for the flag indicating if the trip is completed.
        trip_time_tracker (mmap.mmap): Shared memory for the trip time tracker.
    """
    while read_from_shared_memory(trips_count) < max_trips and not read_from_shared_memory(signal_stop):
        log_method(f"Rejs nr {read_from_shared_memory(trips_count) + 1}")
        start_time = time.time()
        write_to_shared_memory(bridge_direction, 0, 1)
        write_to_shared_memory(boarding_allowed, 0, 1)
        write_to_shared_memory(trip_completed, 0, 0)

        while (time.time() - start_time) < ship_departing_interval and read_from_shared_memory(boarding_allowed):
            sleep(0.1)

        write_to_shared_memory(boarding_allowed, 0, 0)
        log_method("Czas na wypłynięcie statku")

        bridge_cleared.wait()

        log_method("Mostek pusty, statek gotowy do odpłynięcia")

        if read_from_shared_memory(signal_stop):
            log_method("Rejs odwołany.")
        elif count_passengers_in_shared_memory(passengers_on_ship) > 0:
            log_method(f"Statek odpływa z {count_passengers_in_shared_memory(passengers_on_ship)} pasażerami na pokładzie.")
            write_to_shared_memory(trip_time_tracker, 0, int(time.time()), 'd')
            sleep(trip_time)
            write_to_shared_memory(trip_completed, 0, 1)
            write_to_shared_memory(trip_time_tracker, 0, -1, 'd')
            log_method("Statek powrócił do portu")
        else:
            log_method("Brak pasażerów na statku, rejs odwołany.")

        write_to_shared_memory(bridge_direction, 0, 0)

        arr = shared_memory_to_array(passengers_on_ship)
        for passenger_id in arr:
            bridge_semaphore.acquire()
            remove_from_shared_memory(passengers_on_ship, passenger_id)
            passengers_on_bridge_w.send(passenger_id)
            log_method(f"Pasażer {passenger_id} schodzi na mostek.")
            sleep(0.1)

        bridge_cleared.wait()

        write_to_shared_memory(trips_count, 0, read_from_shared_memory(trips_count) + 1)

    bridge_close.set()