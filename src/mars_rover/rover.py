"""A rover."""

from copy import copy
from enum import Enum
from dataclasses import field, dataclass


class Heading(Enum):
    """The four cardinal directions."""

    N = "NORTH"
    W = "WEST"
    S = "SOUTH"
    E = "EAST"


@dataclass
class Location:
    """A point in a 2 dimensional plane."""

    x: int
    y: int

    def as_tuple(self) -> tuple[int, int]:
        """Return the location as a tuple of coordinates."""
        return (self.x, self.y)


@dataclass
class Rover:
    """Hold the position and direction of a rover, allows it to move."""

    location: Location
    heading: Heading
    obstacles: set[tuple[int, int]] = field(default_factory=set)
    status: str = "OK"

    @classmethod
    def from_coordinates(
        cls,
        coordinates: tuple[int, int],
        heading: Heading,
        obstacles: set[tuple[int, int]] = None,
        status: str = "OK",
    ) -> "Rover":
        """Instantiate a Rover from coordinates tuple."""
        location = Location(*coordinates)
        if not obstacles:
            obstacles = set()
        return Rover(location, heading, obstacles, status)

    def move_forwards(self):
        """Move the Rover forwards in the direction it is facing."""
        next_location = copy(self.location)
        if self.heading == Heading.N:
            next_location.y += 1
        elif self.heading == Heading.S:
            next_location.y -= 1
        elif self.heading == Heading.E:
            next_location.x += 1
        else:
            next_location.x -= 1

        if next_location.as_tuple() not in self.obstacles:
            self.location = next_location
        else:
            self.status = "STUCK"

    def move_backwards(self):
        """Move the Rover backwards to the direction it is facing."""
        if self.heading == Heading.N:
            self.location.y -= 1
        elif self.heading == Heading.S:
            self.location.y += 1
        elif self.heading == Heading.E:
            self.location.x -= 1
        else:
            self.location.x += 1

    def rotate_left(self):
        """Rotate the Rover to the left."""
        if self.heading == Heading.N:
            self.heading = Heading.W
        elif self.heading == Heading.W:
            self.heading = Heading.S
        elif self.heading == Heading.E:
            self.heading = Heading.N
        else:
            self.heading = Heading.E

    def rotate_right(self):
        """Rotate the Rover to the right."""
        if self.heading == Heading.N:
            self.heading = Heading.E
        elif self.heading == Heading.W:
            self.heading = Heading.N
        elif self.heading == Heading.E:
            self.heading = Heading.S
        else:
            self.heading = Heading.W
