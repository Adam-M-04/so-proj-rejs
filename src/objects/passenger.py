from time import sleep

from src.LogService import LogService


def passenger(passenger_id, passengers_in_port, bridge_semaphore, passengers_on_bridge, boarding_allowed, passengers_after_trip, logger_queue, bridge_close):
    """
    Simulates a passenger attempting to board the ship.

    Args:
        passenger_id (int): The ID of the passenger.
        passengers_in_port (multiprocessing.List): List of passengers currently in the port.
        bridge_semaphore (multiprocessing.Semaphore): Semaphore to control access to the bridge.
        passengers_on_bridge (multiprocessing.Queue): Queue of passengers waiting to enter the bridge.
        boarding_allowed (multiprocessing.Value): Flag indicating if boarding is allowed.
        passengers_after_trip (multiprocessing.List): List of passengers who have completed the trip.
        logger_queue (multiprocessing.Queue): Queue for logging messages.
        bridge_close (multiprocessing.Event): Event to signal that the bridge is closed.
    """
    while passenger_id not in passengers_after_trip and not bridge_close.is_set():
        if not boarding_allowed.value or passenger_id not in passengers_in_port:
            sleep(1)
            continue
        bridge_semaphore.acquire()
        if not boarding_allowed.value or bridge_close.is_set():
            bridge_semaphore.release()
            continue
        LogService.log_static(f"Pasażer {passenger_id} wchodzi na mostek", logger_queue)
        passengers_in_port.remove(passenger_id)
        passengers_on_bridge.put(passenger_id)
