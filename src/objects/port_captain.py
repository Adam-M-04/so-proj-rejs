import src.globals as GLOBALS

class PortCaptain:
    def __init__(self):
        """
        Initializes the PortCaptain with a reference to the ShipCaptain.
        """
        # self.signal_stop = False

    @staticmethod
    def send_depart_now_signal():
        """
        Sends a signal to the ship captain to depart immediately.
        """
        print("KapitanPortu: Wysyłanie sygnału DEPART_NOW.")
        GLOBALS.captain.handle_signal("DEPART_NOW")

    def send_stop_signal(self):
        """
        Sends a signal to stop further cruises.
        """
        # print("KapiatanPortu: Wysyłanie sygnału STOP_ALL_CRUISES.")
        # self.signal_stop = True
