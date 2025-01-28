class ReaderService:
    @staticmethod
    def read_number(min_value: float, max_value: float, message: str, default_value: float) -> float:
        """
        Reads a number from the user within the specified range, with a default value.

        Clears the console, displays a message, and prompts the user to input a number.
        If the input is within the specified range, it returns the number.
        If the input is invalid or out of range, it prompts the user again.

        :param min_value: The minimum value of the range.
        :param max_value: The maximum value of the range.
        :param message: The message to display to the user.
        :param default_value: The default value.
        :return: The number provided by the user within the range.
        """
        print("\033[H\033[J", end="")
        while True:
            try:
                number = float(input(f"{message} <{min_value} - {max_value}> [domyślnie {default_value}]: "))
                if min_value <= number <= max_value:
                    return number
                else:
                    print(f"Podałeś liczbę spoza zakresu <{min_value} - {max_value}>.")
            except ValueError:
                print("Niepoprawna wartość. Wprowadź liczbę.")

    @staticmethod
    def read_boolean(message: str, default_value: float) -> bool:
        """
        Reads a boolean from the user, with a default value.

        Clears the console, displays a message, and prompts the user to input 'T' or 'N'.
        If the input is 'T', it returns True.
        If the input is 'N', it returns False.
        If the input is invalid, it prompts the user again.

        :param message: The message to display to the user.
        :param default_value: The default value.
        :return: The boolean value provided by the user.
        """
        print("\033[H\033[J", end="")
        while True:
            try:
                input_val = input(f"{message} <T - tak/N - nie> [domyślnie {'Tak' if default_value else 'Nie'}]: ").lower()
                if input_val == "t":
                    return True
                elif input_val == "n":
                    return False
                else:
                    print(f"Podałeś niepoprawną wartość. Wprowadź 'T' lub 'N'.")
            except ValueError:
                print("Niepoprawna wartość.")