from time import sleep

from src.SimulationDisplay import SimulationDisplay
from src.simulation import simulation
# import src.globals as GLOBALS

def main():
    try:
        # GLOBALS.logger.log("Start symulacji...")

        display = SimulationDisplay(refresh_interval=0.1)

        simulation(display)

        # GLOBALS.logger.log("Koniec symulacji...")
        # GLOBALS.logger.close()

        # sleep(1)
        display.stop()
    except Exception as e:
        print("Wystąpił błąd w trakcie trwania symulacji...")
        # GLOBALS.logger.error(e)
        # GLOBALS.logger.close()

if __name__ == "__main__":
    main()
