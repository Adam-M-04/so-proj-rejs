import src.globals as GLOBALS

def stop_boarding_passengers():
    # Stop all passengers from boarding
    print("Wstrzymywanie ładowania pasażerów...")
    for passenger in GLOBALS.passengers:
        if passenger.waiting_for_boarding():
            passenger.stop_boarding()