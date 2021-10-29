"""A control tower to control rovers."""
from enum import Enum

from .rover import Rover


class RoverCommands(Enum):
    """The commands that can be given to a Rover."""

    FORWARDS = "B"
    BACKWARDS = "F"
    LEFT = "L"
    RIGHT = "R"

    @classmethod
    def choices(cls) -> list[str]:
        """Return the possible values for a command."""
        return {item.value for item in cls}

    @classmethod
    def is_valid(cls, value) -> str:
        """Return true if the value is a valid command, false otherwise."""
        return value in cls.choices()


class ControlTower:
    """Control one rover."""

    def __init__(self, rover: Rover):
        """Instantiate a ControlTower give the rover it will control."""
        self.rover = rover

    def execute_commands(self, commands: str):
        """Run the commands against the rover, making it move."""
        self.validate_commands(commands)

        for command in commands:
            rover_command = RoverCommands(command)
            if rover_command == RoverCommands.FORWARDS:
                self.rover.move_forwards()
            elif rover_command == RoverCommands.BACKWARDS:
                self.rover.move_backwards()
            elif rover_command == RoverCommands.LEFT:
                self.rover.rotate_left()
            elif rover_command == RoverCommands.RIGHT:
                self.rover.rotate_right()

    def report_position(self) -> str:
        """Return the position and heading of the rover for humans."""
        return f"{self.rover.location.as_tuple()} {self.rover.heading.value} {self.rover.status}"

    @staticmethod
    def validate_commands(commands: str):
        """Validate given list of commands."""
        if not isinstance(commands, str):
            raise ValueError("Expected a command as a string, got %s.", commands)

        for command in commands:
            if RoverCommands.is_valid(command):
                raise ValueError(
                    "Received an invalid command, got %s.",
                    command,
                )
