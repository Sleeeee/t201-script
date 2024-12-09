class Utils:
    def validate_input(self, message: str) -> bool:
        """
        Asks for the user to confirm their input
        PRE : None
        POST : Returns True if the user inputs y/Y / False if the user inputs n/N / stays in the loop otherwise
        """
        input_upper = input(f"[t201-script] {message} [y/n]").upper()
        while input_upper not in ("Y", "N"):
            input_upper = input(f"[t201-script] Invalid option. {message} [y/n]").upper()
        return input_upper == "Y"
