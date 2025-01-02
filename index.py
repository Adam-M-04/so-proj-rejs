from time import sleep

from src.SimulationDisplay import SimulationDisplay
from src.simulation import simulation
import src.globals as GLOBALS

def main():
    try:
        GLOBALS.logger.log("Start symulacji...")

        display = SimulationDisplay(refresh_interval=0.1)
        display.start()

        simulation()

        GLOBALS.logger.log("Koniec symulacji...")
        GLOBALS.logger.close()

        sleep(1)
        display.stop()
    except Exception as e:
        GLOBALS.logger.log(f"Wystąpił błąd w trakcie symulacji: {e}")
        GLOBALS.logger.close()

if __name__ == "__main__":
    main()
