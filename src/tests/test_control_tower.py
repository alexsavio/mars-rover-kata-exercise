"""Tests for the and RoverCommand ControlTower classes."""

from contextlib import contextmanager

import pytest

from mars_rover.rover import Rover, Heading
from mars_rover.control_tower import ControlTower


@pytest.fixture
def rover(request) -> Rover:
    """Return a Rover in the given coordinates and heading."""
    coordinates = request.param[0]
    heading = request.param[1]
    return Rover.from_coordinates(coordinates, heading)


@contextmanager
def does_not_raise():
    """Yield for a test that is not expected to raise."""
    yield


@pytest.mark.parametrize(
    "rover",
    [
        ((0, 0), Heading.N),
        ((0, 1), Heading.W),
        ((-1, -1), Heading.W),
        ((1, 0), Heading.E),
        ((0, -2), Heading.S),
    ],
    indirect=True,
)
def test_instantiation(rover: Rover):
    """Test that a ControlTower is correctly instantiated."""
    tower = ControlTower(rover)
    assert tower
    assert tower.rover == rover


@pytest.mark.parametrize(
    "initial_coordinates,initial_heading,expected_report",
    [
        ((0, 0), Heading.N, "(0, 0) NORTH OK"),
        ((0, 1), Heading.W, "(0, 1) WEST OK"),
        ((-1, -1), Heading.W, "(-1, -1) WEST OK"),
        ((1, 0), Heading.E, "(1, 0) EAST OK"),
        ((0, -2), Heading.S, "(0, -2) SOUTH OK"),
    ],
)
def test_report_position(
    initial_coordinates: tuple[int, int],
    initial_heading: Heading,
    expected_report: str,
):
    """Test that a ControlTower reports the rover position in the correct format."""
    rover = Rover.from_coordinates(initial_coordinates, initial_heading)
    tower = ControlTower(rover)
    assert tower
    assert tower.report_position() == expected_report


@pytest.mark.parametrize(
    "commands,expectation",
    [
        ("FLFFFRFLB", does_not_raise()),
        ("FLFFFRFLBA", pytest.raises(ValueError)),
        (list("FLFFFRFLB"), pytest.raises(ValueError)),
        ("FLFFFRFLB"[::-1], does_not_raise()),
        ("FRFLB", does_not_raise()),
        ("B", does_not_raise()),
    ],
)
def test_validate_commands(commands: str, expectation):
    """Test that a ControlTower validates commands correctly."""
    rover = Rover.from_coordinates((0, 0), Heading.N)
    tower = ControlTower(rover)
    with expectation:
        tower.validate_commands(commands)


@pytest.mark.parametrize(
    "initial_coordinates,initial_heading,commands,final_coordinates,final_heading",
    [
        ((0, 0), Heading.N, "FLFFFRFLB", (-2, 2), Heading.W),
        ((0, 1), Heading.W, "FLFFFRFLBB", (-2, 0), Heading.S),
        ((-1, -1), Heading.W, "FLFFFRFLB"[::-1], (-3, -3), Heading.S),
        ((1, 0), Heading.E, "FRFLB", (1, -1), Heading.E),
        ((0, -2), Heading.S, "B", (0, -1), Heading.S),
    ],
)
def test_execute_commands(
    initial_coordinates: tuple[int, int],
    initial_heading: Heading,
    commands: str,
    final_coordinates: tuple[int, int],
    final_heading: Heading,
):
    """Test that a ControlTower executes commands correctly."""
    rover = Rover.from_coordinates(initial_coordinates, initial_heading)
    tower = ControlTower(rover)
    tower.execute_commands(commands)
    assert tower.rover.location.as_tuple() == final_coordinates
    assert tower.rover.heading == final_heading


@pytest.mark.parametrize(
    "initial_coordinates,initial_heading,obstacles,commands,final_coordinates,final_heading,final_status",
    [
        ((0, 0), Heading.N, {(0, 3)}, "FFFF", (0, 2), Heading.N, "STUCK"),
        # ((0, 1), Heading.W, 'FLFFFRFLBB', (-2, 0), Heading.S),
        # ((-1, -1), Heading.W, 'FLFFFRFLB'[::-1], (-3, -3), Heading.S),
        # ((1, 0), Heading.E, 'FRFLB', (1, -1), Heading.E),
        # ((0, -2), Heading.S, 'B', (0, -1), Heading.S),
    ],
)
def test_execute_commands_with_obstacles(
    initial_coordinates: tuple[int, int],
    initial_heading: Heading,
    obstacles: set[tuple[int, int]],
    commands: str,
    final_coordinates: tuple[int, int],
    final_heading: Heading,
    final_status: str,
):
    """Test that a ControlTower executes commands correctly."""
    rover = Rover.from_coordinates(initial_coordinates, initial_heading, obstacles)
    tower = ControlTower(rover)
    tower.execute_commands(commands)
    assert tower.rover.location.as_tuple() == final_coordinates
    assert tower.rover.heading == final_heading
    assert tower.rover.status == final_status


@pytest.mark.parametrize(
    "initial_coordinates,initial_heading,obstacles,commands,expected_report",
    [
        ((0, 0), Heading.N, {(0, 3)}, "FFFF", "(0, 2) NORTH STUCK"),
        ((0, 1), Heading.W, {}, "FLFFFRFLBB", "(-2, 0) SOUTH OK"),
    ],
)
def test_report_position_with_obstacles(
    initial_coordinates: tuple[int, int],
    initial_heading: Heading,
    obstacles: set[tuple[int, int]],
    commands: str,
    expected_report: str,
):
    """Test that a ControlTower reports the position of a rover correctly."""
    rover = Rover.from_coordinates(initial_coordinates, initial_heading, obstacles)
    tower = ControlTower(rover)
    tower.execute_commands(commands)
    assert tower.report_position() == expected_report
