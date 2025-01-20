from time import sleep


def passenger(passenger_id, passengers_in_port, bridge_semaphore, passengers_on_bridge, boarding_allowed, passengers_after_trip):
    while passenger_id not in passengers_after_trip:
        if not boarding_allowed.value or passenger_id not in passengers_in_port:
            sleep(1)
            continue
        bridge_semaphore.acquire()
        if not boarding_allowed.value:
            bridge_semaphore.release()
            continue
        print(f"Pasażer {passenger_id} wchodzi na mostek")
        passengers_in_port.remove(passenger_id)
        passengers_on_bridge.put(passenger_id)
