from time import sleep

from src.LogService import LogService
from src.SimulationDisplay import SimulationDisplay
from src.simulation import simulation
import src.globals as GLOBALS

def main():
    try:
        # Create a shared LogService instance
        GLOBALS.logger = LogService()
        GLOBALS.logger.start()

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
