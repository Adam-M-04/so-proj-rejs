import os
import random
from time import sleep

from src.objects.SharedMemory import append_to_shared_memory, write_to_shared_memory, read_from_shared_memory, \
    count_passengers_in_shared_memory, remove_from_shared_memory


def walk_bridge(passenger_id, bridge_direction, ship_lock, boarding_allowed, passengers_on_ship, ship_capacity, passengers_in_port, passengers_after_trip, bridge_semaphore, passengers_walking_bridge, bridge_cleared, log_method, trip_completed):
    """
    Handles the process of a passenger walking across the bridge.

    Args:
        passenger_id (int): The ID of the passenger.
        bridge_direction (multiprocessing.Value): The direction of the bridge (True for boarding, False for disembarking).
        ship_lock (multiprocessing.Lock): Lock to synchronize access to the ship.
        boarding_allowed (mmap.mmap): Shared memory for the flag indicating if boarding is allowed.
        passengers_on_ship (mmap.mmap): Shared memory for passengers currently on the ship.
        ship_capacity (int): The maximum capacity of the ship.
        passengers_in_port (mmap.mmap): Shared memory for passengers currently in the port.
        passengers_after_trip (mmap.mmap): Shared memory for passengers who have completed the trip.
        bridge_semaphore (multiprocessing.Semaphore): Semaphore to control access to the bridge.
        passengers_walking_bridge (mmap.mmap): Shared memory for passengers currently walking on the bridge.
        bridge_cleared (multiprocessing.Event): Event to signal that the bridge is cleared.
        log_method (function): Logging method from Log service.
        trip_completed (mmap.mmap): Shared memory for the flag indicating if the trip is completed.
    """
    sleep(random.uniform(1, 2))
    bridge_direction_value = read_from_shared_memory(bridge_direction, 'i')
    if bridge_direction_value:
        with ship_lock:
            if boarding_allowed and count_passengers_in_shared_memory(passengers_on_ship) < ship_capacity:
                log_method(f"Pasażer {passenger_id} wchodzi na statek")
                append_to_shared_memory(passengers_on_ship, passenger_id)
            else:
                log_method(f"Statek pełny! Pasażer {passenger_id} schodzi z mostku do portu")
                write_to_shared_memory(boarding_allowed, 0, 0)
                append_to_shared_memory(passengers_in_port, passenger_id)
    else:
        if read_from_shared_memory(trip_completed):
            append_to_shared_memory(passengers_after_trip, passenger_id)
        else:
            append_to_shared_memory(passengers_in_port, passenger_id)
        log_method(f"Pasażer {passenger_id} zszedł z mostku")
    remove_from_shared_memory(passengers_walking_bridge, passenger_id)
    bridge_semaphore.release()
    if count_passengers_in_shared_memory(passengers_walking_bridge) == 0:
        bridge_cleared.set()

def enter_bridge(passengers_on_bridge, boarding_allowed, passengers_on_ship, ship_capacity, ship_lock, passengers_in_port, bridge_semaphore, bridge_direction, passengers_after_trip, passengers_walking_bridge, bridge_cleared, log_method, bridge_close, trip_completed):
    """
    Manages the entry of passengers onto the bridge and initiates the walking process.

    Args:
        passengers_on_bridge (multiprocessing.Connection): Connection object for reading passengers waiting to enter the bridge.
        boarding_allowed (mmap.mmap): Shared memory for the flag indicating if boarding is allowed.
        passengers_on_ship (mmap.mmap): Shared memory for passengers currently on the ship.
        ship_capacity (int): The maximum capacity of the ship.
        ship_lock (multiprocessing.Lock): Lock to synchronize access to the ship.
        passengers_in_port (mmap.mmap): Shared memory for passengers currently in the port.
        bridge_semaphore (multiprocessing.Semaphore): Semaphore to control access to the bridge.
        bridge_direction (mmap.mmap): Shared memory for the direction of the bridge (True for boarding, False for disembarking).
        passengers_after_trip (mmap.mmap): Shared memory for passengers who have completed the trip.
        passengers_walking_bridge (mmap.mmap): Shared memory for passengers currently walking on the bridge.
        bridge_cleared (multiprocessing.Event): Event to signal that the bridge is cleared.
        log_method (function): Logging method from Log service.
        bridge_close (multiprocessing.Event): Event to signal that the bridge is closed.
        trip_completed (mmap.mmap): Shared memory for the flag indicating if the trip is completed.
    """
    while not bridge_close.is_set():
        if passengers_on_bridge.poll():
            bridge_cleared.clear()
            passenger_id = passengers_on_bridge.recv()
            append_to_shared_memory(passengers_walking_bridge, passenger_id)

            try:
                pid = os.fork()
                if pid == 0:  # Child process
                    walk_bridge(passenger_id, bridge_direction, ship_lock, boarding_allowed, passengers_on_ship,
                                ship_capacity, passengers_in_port,
                                passengers_after_trip, bridge_semaphore, passengers_walking_bridge, bridge_cleared,
                                log_method, trip_completed)
                    os._exit(0)
            except OSError as e:
                return None
        else:
            sleep(0.1)