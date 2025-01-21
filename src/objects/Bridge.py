import random
import threading
import time
from time import sleep

from src.LogService import LogService

def walk_bridge(passenger_id, bridge_direction, ship_lock, boarding_allowed, passengers_on_ship, ship_capacity, passengers_in_port, passengers_after_trip, bridge_semaphore, passengers_walking_bridge, bridge_cleared, logger_queue, trip_completed):
    """
    Handles the process of a passenger walking across the bridge.

    Args:
        passenger_id (int): The ID of the passenger.
        bridge_direction (multiprocessing.Value): The direction of the bridge (True for boarding, False for disembarking).
        ship_lock (multiprocessing.Lock): Lock to synchronize access to the ship.
        boarding_allowed (multiprocessing.Value): Flag indicating if boarding is allowed.
        passengers_on_ship (multiprocessing.List): List of passengers currently on the ship.
        ship_capacity (int): The maximum capacity of the ship.
        passengers_in_port (multiprocessing.List): List of passengers currently in the port.
        passengers_after_trip (multiprocessing.List): List of passengers who have completed the trip.
        bridge_semaphore (multiprocessing.Semaphore): Semaphore to control access to the bridge.
        passengers_walking_bridge (multiprocessing.List): List of passengers currently walking on the bridge.
        bridge_cleared (multiprocessing.Event): Event to signal that the bridge is cleared.
        logger_queue (multiprocessing.Queue): Queue for logging messages.
        trip_completed (multiprocessing.Value): Flag indicating if the trip is completed.
    """
    sleep(random.uniform(1, 2))
    if bridge_direction.value:
        with ship_lock:
            if boarding_allowed and len(passengers_on_ship) < ship_capacity:
                LogService.log_static(f"Pasażer {passenger_id} wchodzi na statek", logger_queue)
                passengers_on_ship.append(passenger_id)
            else:
                LogService.log_static(f"Statek pełny! Pasażer {passenger_id} schodzi z mostku do portu", logger_queue)
                boarding_allowed.value = False
                passengers_in_port.append(passenger_id)
    else:
        if trip_completed.value:
            passengers_after_trip.append(passenger_id)
        else:
            passengers_in_port.append(passenger_id)
        LogService.log_static(f"Pasażer {passenger_id} zszedł z mostku", logger_queue)
    passengers_walking_bridge.remove(passenger_id)
    bridge_semaphore.release()
    if len(passengers_walking_bridge) == 0:
        bridge_cleared.set()

def enter_bridge(passengers_on_bridge, boarding_allowed, passengers_on_ship, ship_capacity, ship_lock, passengers_in_port, bridge_semaphore, bridge_direction, passengers_after_trip, passengers_walking_bridge, bridge_cleared, logger_queue, bridge_close, trip_completed):
    """
    Manages the entry of passengers onto the bridge and initiates the walking process.

    Args:
        passengers_on_bridge (multiprocessing.Queue): Queue of passengers waiting to enter the bridge.
        boarding_allowed (multiprocessing.Value): Flag indicating if boarding is allowed.
        passengers_on_ship (multiprocessing.List): List of passengers currently on the ship.
        ship_capacity (int): The maximum capacity of the ship.
        ship_lock (multiprocessing.Lock): Lock to synchronize access to the ship.
        passengers_in_port (multiprocessing.List): List of passengers currently in the port.
        bridge_semaphore (multiprocessing.Semaphore): Semaphore to control access to the bridge.
        bridge_direction (multiprocessing.Value): The direction of the bridge (True for boarding, False for disembarking).
        passengers_after_trip (multiprocessing.List): List of passengers who have completed the trip.
        passengers_walking_bridge (multiprocessing.List): List of passengers currently walking on the bridge.
        bridge_cleared (multiprocessing.Event): Event to signal that the bridge is cleared.
        logger_queue (multiprocessing.Queue): Queue for logging messages.
        bridge_close (multiprocessing.Event): Event to signal that the bridge is closed.
        trip_completed (multiprocessing.Value): Flag indicating if the trip is completed.
    """
    while not bridge_close.is_set():
        if not passengers_on_bridge.empty():
            bridge_cleared.clear()
            passenger_id = passengers_on_bridge.get()
            passengers_walking_bridge.append(passenger_id)

            thread = threading.Thread(target=walk_bridge, args=(passenger_id, bridge_direction, ship_lock, boarding_allowed, passengers_on_ship, ship_capacity, passengers_in_port,
                                                                passengers_after_trip, bridge_semaphore, passengers_walking_bridge, bridge_cleared, logger_queue, trip_completed))
            thread.start()
        else:
            time.sleep(0.1)