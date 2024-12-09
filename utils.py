class Utils:
    def validate_input(self, message):
        input_upper = input(f"[t201-script] {message} [y/n]").upper()
        while input_upper not in ("Y", "N"):
            input_upper = input(f"[t201-script] Invalid option. {message} [y/n]").upper()
        return input_upper == "Y"
