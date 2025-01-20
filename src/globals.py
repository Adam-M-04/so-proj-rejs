# from src.LogService import LogService

# from src.LogService import LogService
from src.ReaderService import ReaderService
# from src.objects.passenger import Passenger
from src.objects.port_captain import PortCaptain
# from src.objects.ship import Ship
# from src.objects.ship_captain import ShipCaptain
#
# logger: LogService = LogService()
#
# use_defaults = ReaderService.read_boolean("Czy chcesz użyć domyślnych parametrów symulacji?", 1)
#
# ship_capacity = 5 if use_defaults else int(ReaderService.read_number(1, 600, "Podaj ile pasażerów mieści się na statku", 5))
# ship_departing_interval = 8 if use_defaults else int(ReaderService.read_number(1, 3600, "Podaj co ile sekund odpływa statek", 8))
# ship: Ship = Ship(ship_capacity)
#
# bridge_capacity = min(3, ship_capacity) if use_defaults else int(ReaderService.read_number(1, ship_capacity, "Podaj maksymalną liczbę pasażerów jednocześnie przebywających na mostku", min(3, ship_capacity)))
# bridge_semaphore: threading.Semaphore = threading.Semaphore(bridge_capacity)
#
# passengers_num = 12 if use_defaults else int(ReaderService.read_number(0, 10000, "Podaj ile pasażerów czeka dziś na rejs", 12))
# passengers: list[Passenger] = [Passenger(i + 1) for i in range(passengers_num)]
#
# trips_count = 0
# max_trips = 3 if use_defaults else int(ReaderService.read_number(1, 100, "Podaj ile maksymalnie kursów może zrobić dzisiaj statek", 3))
#
# captain: ShipCaptain = ShipCaptain()
# port_captain: PortCaptain = PortCaptain()
#
# boarding_allowed = threading.Event()
#
# logger.log("Parametry symulacji wczytane: "
#            f"statek mieści {ship_capacity} pasażerów, odpływa co {ship_departing_interval}s, czas rejsu {ship.cruise_duration}s, "
#            f"mostek mieści {bridge_capacity} pasażerów, "
#            f"pasażerowie: {passengers_num}, "
#            f"maksymalnie {max_trips} kursów.")

logger = None

use_defaults = False

passengers_num = 12
trips_count = 0
max_trips = 3
ship_capacity = 5
bridge_capacity = 3
ship_departing_interval = 7
trip_time = 4

port_captain: PortCaptain = PortCaptain()
