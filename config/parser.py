import random


class ConfigParser:
    """Parse and validate maze configuration files."""

    def __init__(self, config_file: str) -> None:
        """Initialize parser with config file path."""
        self.config_file = config_file

    def parse(self) -> dict[str, object]:
        """Read configuration file and return parsed values."""
        config: dict[str, object] = {}

        with open(self.config_file, "r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                key, value = self._parse_line(line, line_number)
                config[key] = self._convert_value(key, value, line_number)

        self._validate(config)
        return config

    def _parse_line(
        self,
        line: str,
        line_number: int,
    ) -> tuple[str, str]:
        """Split configuration line into key and value."""
        if "=" not in line:
            raise ValueError(
                f"Line {line_number}: invalid syntax, expected KEY=VALUE"
            )

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()

        if not key:
            raise ValueError(f"Line {line_number}: empty config key")

        return key, value

    def _convert_value(
        self,
        key: str,
        value: str,
        line_number: int,
    ) -> object:
        """Convert configuration values to proper Python types."""
        if key in ("WIDTH", "HEIGHT"):
            return self._convert_int(key, value, line_number)

        if key == "SEED":
            if not value:
                return random.randint(1, 1000000)

            return self._convert_int(key, value, line_number)

        if key in ("ENTRY", "EXIT"):
            return self._convert_coordinates(key, value, line_number)

        if key == "OUTPUT_FILE":
            if not value:
                raise ValueError(
                    f"Line {line_number}: OUTPUT_FILE must not be empty"
                    )

            return value

        if key == "PERFECT":
            if value == "True":
                return True

            if value == "False":
                return False

            raise ValueError(
                f"Line {line_number}: PERFECT must be True or False"
            )

        raise ValueError(f"Line {line_number}: unknown config key '{key}'")

    def _convert_int(
        self,
        key: str,
        value: str,
        line_number: int,
    ) -> int:
        """Convert string value to integer."""
        if not value:
            raise ValueError(f"Line {line_number}: {key} must not be empty")

        try:
            return int(value)

        except ValueError as error:
            raise ValueError(
                f"Line {line_number}: {key} must be an integer"
            ) from error

    def _convert_coordinates(
        self,
        key: str,
        value: str,
        line_number: int,
    ) -> tuple[int, int]:
        """Convert x,y string into coordinate tuple."""
        parts = value.split(",")

        if len(parts) != 2:
            raise ValueError(
                f"Line {line_number}: {key} must be in x,y format"
            )

        x_text = parts[0].strip()
        y_text = parts[1].strip()

        if not x_text or not y_text:
            raise ValueError(
                f"Line {line_number}: {key} coordinates must not be empty"
            )

        try:
            return int(x_text), int(y_text)

        except ValueError as error:
            raise ValueError(
                f"Line {line_number}: {key} coordinates must be integers"
            ) from error

    def _validate(self, config: dict[str, object]) -> None:
        """Validate configuration values and constraints."""
        required_keys = [
            "WIDTH",
            "HEIGHT",
            "ENTRY",
            "EXIT",
            "OUTPUT_FILE",
            "PERFECT",
        ]

        if "SEED" not in config:
            config["SEED"] = random.randint(1, 1000000)

        for required_key in required_keys:
            if required_key not in config:
                raise ValueError(f"Missing required key: {required_key}")

        width = config["WIDTH"]
        height = config["HEIGHT"]
        seed = config["SEED"]
        entry = config["ENTRY"]
        exit_ = config["EXIT"]
        output_file = config["OUTPUT_FILE"]
        perfect = config["PERFECT"]

        if not isinstance(width, int):
            raise ValueError("WIDTH must be an integer")

        if not isinstance(height, int):
            raise ValueError("HEIGHT must be an integer")

        if not isinstance(seed, int):
            raise ValueError("SEED must be an integer")

        if width < 13 or height < 9:
            raise ValueError(
                "Maze is too small. Minimum size for 42 pattern is 13x9"
            )

        if not isinstance(entry, tuple) or len(entry) != 2:
            raise ValueError("ENTRY must be in x,y format")

        if not isinstance(exit_, tuple) or len(exit_) != 2:
            raise ValueError("EXIT must be in x,y format")

        entry_x, entry_y = entry
        exit_x, exit_y = exit_

        if not isinstance(entry_x, int) or not isinstance(entry_y, int):
            raise ValueError("ENTRY coordinates must be integers")

        if not isinstance(exit_x, int) or not isinstance(exit_y, int):
            raise ValueError("EXIT coordinates must be integers")

        if entry_x < 0 or entry_x >= width:
            raise ValueError("ENTRY x coordinate is outside maze bounds")

        if entry_y < 0 or entry_y >= height:
            raise ValueError("ENTRY y coordinate is outside maze bounds")

        if exit_x < 0 or exit_x >= width:
            raise ValueError("EXIT x coordinate is outside maze bounds")

        if exit_y < 0 or exit_y >= height:
            raise ValueError("EXIT y coordinate is outside maze bounds")

        if entry == exit_:
            raise ValueError("ENTRY and EXIT must be different")

        if not isinstance(output_file, str) or not output_file:
            raise ValueError("OUTPUT_FILE must not be empty")

        if not isinstance(perfect, bool):
            raise ValueError("PERFECT must be True or False")
