class ConfigParser:

    def __init__(self, config_file: str) -> None:
        self.config_file = config_file

    def parse(self) -> dict[str, object]:

        config: dict[str, object] = {}
        with open(self.config_file, "r", encoding="utf-8") as file:
            for line in file:

                line = line.strip()
                if not line:
                    continue
                if line.startswith("#"):
                    continue
                key, value = self._parse_line(line)

                config[key] = self._convert_value(key, value)

        self._validate(config)
        return config

    def _parse_line(self, line: str) -> tuple[str, str]:

        if "=" not in line:
            raise ValueError

        key, value = line.split("=", 1)

        key = key.strip()
        value = value.strip()

        return key, value

    def _convert_value(self, key: str, value: str) -> object:

        if key in ("WIDTH", "HEIGHT", "SEED"):
            return int(value)

        elif key in ("ENTRY", "EXIT"):
            parts = value.split(",")
            if len(parts) != 2:
                raise ValueError

            x = int(parts[0])
            y = int(parts[1])
            return (x, y)

        elif key == "OUTPUT_FILE":
            return str(value)

        else:
            raise ValueError

    def _validate(self, config: dict[str, object]) -> None:
        required_keys = [
            "WIDTH",
            "HEIGHT",
            "SEED",
            "ENTRY",
            "EXIT",
            "OUTPUT_FILE",
        ]

        for required_key in required_keys:
            if required_key not in config:
                raise ValueError

        width = config["WIDTH"]
        height = config["HEIGHT"]
        entry = config["ENTRY"]
        exit_ = config["EXIT"]
        output_file = config["OUTPUT_FILE"]

        if not isinstance(width, int) or not isinstance(height, int):
            raise ValueError

        if width < 2 or height < 2:
            raise ValueError

        if not isinstance(entry, tuple) or not isinstance(exit_, tuple):
            raise ValueError

        entry_x, entry_y = entry
        exit_x, exit_y = exit_

        if entry_x < 0 or entry_x >= width:
            raise ValueError

        if entry_y < 0 or entry_y >= height:
            raise ValueError

        if exit_x < 0 or exit_x >= width:
            raise ValueError

        if exit_y < 0 or exit_y >= height:
            raise ValueError

        if entry == exit_:
            raise ValueError

        if not isinstance(output_file, str) or not output_file:
            raise ValueError
