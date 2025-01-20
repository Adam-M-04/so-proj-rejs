import random
import threading
import time
from time import sleep

from src.LogService import LogService
from src.globals import max_trips


def walk_bridge(passenger_id, bridge_direction, ship_lock, boarding_allowed, passengers_on_ship, ship_capacity, passengers_in_port, passengers_after_trip, bridge_semaphore, passengers_walking_bridge, bridge_cleared, logger_queue):
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
        passengers_after_trip.append(passenger_id)
        LogService.log_static(f"Pasażer {passenger_id} zszedł z mostku", logger_queue)
    passengers_walking_bridge.remove(passenger_id)
    bridge_semaphore.release()
    if len(passengers_walking_bridge) == 0:
        bridge_cleared.set()

def enter_bridge(passengers_on_bridge, boarding_allowed, passengers_on_ship, ship_capacity, ship_lock, passengers_in_port, bridge_semaphore, bridge_direction, passengers_after_trip, passengers_walking_bridge, bridge_cleared, logger_queue, bridge_close):
    while not bridge_close.is_set():
        if not passengers_on_bridge.empty():
            bridge_cleared.clear()
            passenger_id = passengers_on_bridge.get()
            passengers_walking_bridge.append(passenger_id)

            thread = threading.Thread(target=walk_bridge, args=(passenger_id, bridge_direction, ship_lock, boarding_allowed, passengers_on_ship, ship_capacity, passengers_in_port,
                                                                passengers_after_trip, bridge_semaphore, passengers_walking_bridge, bridge_cleared, logger_queue))
            thread.start()
        else:
            time.sleep(0.1)