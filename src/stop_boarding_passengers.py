import src.globals as GLOBALS

def stop_boarding_passengers():
    from src.objects.ship import ShipStatus

    # Stop all passengers from boarding
    if GLOBALS.ship.status == ShipStatus.BOARDING_IN_PROGRESS:
        print("Wstrzymywanie ładowania pasażerów...")
    for passenger in GLOBALS.passengers:
        if passenger.waiting_for_boarding():
            passenger.stop_boarding()