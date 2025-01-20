from time import sleep

from src.LogService import LogService
from src.ReaderService import ReaderService
from src.SimulationDisplay import SimulationDisplay
from src.simulation import simulation
import src.globals as GLOBALS

def main():
    try:
        # Create a shared LogService instance
        GLOBALS.logger = LogService()
        GLOBALS.logger.start()

        GLOBALS.use_defaults = ReaderService.read_boolean("Czy chcesz użyć domyślnych parametrów symulacji?", 1)
        if not GLOBALS.use_defaults:
            GLOBALS.ship_capacity = int(ReaderService.read_number(1, 600, "Podaj ile pasażerów mieści się na statku", GLOBALS.ship_capacity))
            GLOBALS.ship_departing_interval = int(ReaderService.read_number(1, 3600, "Podaj co ile sekund odpływa statek", GLOBALS.ship_departing_interval))
            GLOBALS.bridge_capacity = int(ReaderService.read_number(1, GLOBALS.ship_capacity, "Podaj maksymalną liczbę pasażerów jednocześnie przebywających na mostku", min(GLOBALS.bridge_capacity, GLOBALS.ship_capacity)))
            GLOBALS.passengers_num = int(ReaderService.read_number(0, 10000, "Podaj ile pasażerów czeka dziś na rejs", GLOBALS.passengers_num))
            GLOBALS.max_trips = int(ReaderService.read_number(1, 100, "Podaj ile maksymalnie kursów może zrobić dzisiaj statek", GLOBALS.max_trips))
            GLOBALS.trip_time = int(ReaderService.read_number(1, 600, "Podaj czas trwania rejsu", GLOBALS.trip_time))

        GLOBALS.logger.log("Start symulacji...")

        display = SimulationDisplay(refresh_interval=0.1)

        simulation(display)

        GLOBALS.logger.log("Koniec symulacji...")

        sleep(1)
        display.stop()
    except Exception as e:
        GLOBALS.logger.error(e)
    finally:
        GLOBALS.logger.stop()

if __name__ == "__main__":
    main()
