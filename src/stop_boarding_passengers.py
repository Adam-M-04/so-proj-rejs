import src.globals as GLOBALS

def stop_boarding_passengers():
    """
    Stops all passengers from boarding the ship if the ship is in the boarding process.
    Logs the action and stops each passenger that is waiting for boarding.
    """
    from src.objects.ship import ShipStatus

    try:
        # Stop all passengers from boarding
        if GLOBALS.ship.status == ShipStatus.BOARDING_IN_PROGRESS:
            GLOBALS.logger.log("Wstrzymywanie ładowania pasażerów...")
        for passenger in GLOBALS.passengers:
            if passenger.waiting_for_boarding():
                passenger.stop_boarding()
    except Exception as e:
        GLOBALS.logger.error(e)
