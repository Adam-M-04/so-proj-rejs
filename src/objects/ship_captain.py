import time

from src.LogService import LogService


def ship_captain(passengers_on_ship, max_trips, trip_time, ship_departing_interval, boarding_allowed, passengers_on_bridge, bridge_direction, bridge_semaphore, bridge_cleared, trips_count, logger_queue, signal_stop, bridge_close, trip_completed, trip_time_tracker):
    """Board passengers on the ship and make trips."""
    while trips_count.value < max_trips and not signal_stop.is_set():
        LogService.log_static(f"Rejs nr {trips_count.value + 1}", logger_queue)
        start_time = time.time()
        bridge_direction.value = True
        boarding_allowed.value = True
        trip_completed.value = False

        while (time.time() - start_time) < ship_departing_interval:
            time.sleep(0.1)

        boarding_allowed.value = False
        LogService.log_static("Czas na wypłynięcie statku", logger_queue)

        bridge_cleared.wait()

        LogService.log_static("Mostek pusty, statek gotowy do odpłynięcia", logger_queue)

        if signal_stop.is_set():
            LogService.log_static("Rejs odwołany.", logger_queue)
        elif len(passengers_on_ship) > 0:
            LogService.log_static(f"Statek odpływa z {len(passengers_on_ship)} pasażerami na pokładzie.", logger_queue)
            trip_time_tracker.value = time.time()
            time.sleep(trip_time)
            trip_completed.value = True
            trip_time_tracker.value = -1
            LogService.log_static("Statek powrócił do portu", logger_queue)
        else:
            LogService.log_static("Brak pasażerów na statku, rejs odwołany.", logger_queue)

        bridge_direction.value = False
        while len(passengers_on_ship) > 0:
            bridge_semaphore.acquire()
            passenger_id = passengers_on_ship.pop(0)
            passengers_on_bridge.put(passenger_id)
            LogService.log_static(f"Pasażer {passenger_id} schodzi na mostek.", logger_queue)
            time.sleep(0.1)

        bridge_cleared.wait()

        trips_count.value += 1

    bridge_close.set()
