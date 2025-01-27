from time import sleep
import struct

import mmap

from src.objects.SharedMemory import read_from_shared_memory, is_passenger_in_shared_memory, \
    remove_from_shared_memory


def passenger(passenger_id, passengers_in_port, bridge_semaphore, passengers_on_bridge_w, boarding_allowed, passengers_after_trip, log_method, bridge_close):
    """
     Simulates a passenger attempting to board the ship.

     Args:
         passenger_id (int): The ID of the passenger.
         passengers_in_port (mmap.mmap): Shared memory for passengers currently in the port.
         bridge_semaphore (multiprocessing.Semaphore): Semaphore to control access to the bridge.
         passengers_on_bridge_w: File descriptor for writing passengers waiting to enter the bridge.
         boarding_allowed (mmap.mmap): Shared memory for the flag indicating if boarding is allowed.
         passengers_after_trip (mmap.mmap): Shared memory for passengers who have completed the trip.
         log_method: Logging method from Log service
         bridge_close (multiprocessing.Event): Event to signal that the bridge is closed.
     """

    while not is_passenger_in_shared_memory(passengers_after_trip, passenger_id) and not bridge_close.is_set():
        if not read_from_shared_memory(boarding_allowed) or not is_passenger_in_shared_memory(passengers_in_port, passenger_id):
            sleep(1)
            continue
        bridge_semaphore.acquire()
        if not read_from_shared_memory(boarding_allowed) or bridge_close.is_set():
            bridge_semaphore.release()
            continue
        log_method(f"Pasażer {passenger_id} wchodzi na mostek")

        remove_from_shared_memory(passengers_in_port, passenger_id)
        passengers_on_bridge_w.send(passenger_id)

