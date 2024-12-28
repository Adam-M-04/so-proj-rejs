import threading

from src.LogService import LogService
from src.objects.passenger import Passenger
from src.objects.port_captain import PortCaptain
from src.objects.ship import Ship
from src.objects.ship_captain import ShipCaptain

logger: LogService = LogService()

bridge_capacity = 3
bridge_semaphore: threading.Semaphore = threading.Semaphore(bridge_capacity)

ship_capacity = 5
ship_departing_interval = 6
ship: Ship = Ship(ship_capacity)

passengers_num = 12
passengers: list[Passenger] = [Passenger(i + 1) for i in range(passengers_num)]

trips_count = 0
max_trips = 3

captain: ShipCaptain = ShipCaptain()
port_captain: PortCaptain = PortCaptain()

boarding_allowed = threading.Event()
