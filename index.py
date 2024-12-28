from time import sleep

from src.SimulationDisplay import SimulationDisplay
from src.simulation import simulation
import src.globals as GLOBALS

def main():
    GLOBALS.logger.log("Start symulacji...")

    display = SimulationDisplay(refresh_interval=0.1)
    display.start()

    simulation()

    GLOBALS.logger.log("Koniec symulacji...")
    GLOBALS.logger.close()

    sleep(1)
    display.stop()

if __name__ == "__main__":
    main()
