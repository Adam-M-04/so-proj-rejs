import time

def ship(passengers_on_ship, max_trips, trip_time, ship_departing_interval, boarding_allowed, passengers_on_bridge, bridge_direction, bridge_semaphore, bridge_cleared, trips_count):
    """Board passengers on the ship and make trips."""
    while trips_count.value < max_trips:
        print("Rejs nr", trips_count.value + 1)
        start_time = time.time()
        bridge_direction.value = True
        boarding_allowed.value = True

        while (time.time() - start_time) < ship_departing_interval:
            time.sleep(0.1)

        boarding_allowed.value = False
        print("Czas na wypłynięcie statku")

        bridge_cleared.wait()

        print("Mostek pusty, statek gotowy do odpłynięcia")

        if len(passengers_on_ship) > 0:
            print(f"Statek odpływa z {len(passengers_on_ship)} pasażerami na pokładzie.")
            time.sleep(trip_time)
            print("Statek powrócił do portu")

            bridge_direction.value = False
            while len(passengers_on_ship) > 0:
                bridge_semaphore.acquire()
                passenger_id = passengers_on_ship.pop(0)
                passengers_on_bridge.put(passenger_id)
                print(f"Pasażer {passenger_id} schodzi na mostek.")
                time.sleep(0.1)

            bridge_cleared.wait()
        else:
            print("Brak pasażerów na statku, rejs odwołany.")

        trips_count.value += 1