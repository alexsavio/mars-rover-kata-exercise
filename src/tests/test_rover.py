"""Tests for the Rover class."""

import pytest

from mars_rover.rover import Rover, Heading, Location


@pytest.mark.parametrize(
    "coordinates,heading,expected",
    [
        ((0, 0), Heading.N, (0, 1)),
        ((0, 1), Heading.W, (-1, 1)),
        ((-1, -1), Heading.W, (-2, -1)),
        ((1, 0), Heading.E, (2, 0)),
        ((0, -2), Heading.S, (0, -3)),
    ],
)
def test_move_forwards(
    coordinates: tuple[int, int],
    heading: Heading,
    expected: tuple[int, int],
):
    """Test that the Rover moves forwards correctly."""
    location = Location(*coordinates)
    rover = Rover(location, heading)
    rover.move_forwards()
    assert rover.location.as_tuple() == expected
    assert rover.heading == rover.heading


@pytest.mark.parametrize(
    "coordinates,heading,expected",
    [
        ((0, 0), Heading.N, (0, -1)),
        ((0, 1), Heading.W, (1, 1)),
        ((-1, -1), Heading.W, (0, -1)),
        ((1, 0), Heading.E, (0, 0)),
        ((0, -2), Heading.S, (0, -1)),
    ],
)
def test_move_backwards(
    coordinates: tuple[int, int],
    heading: Heading,
    expected: tuple[int, int],
):
    """Test that the Rover moves backwards correctly."""
    location = Location(*coordinates)
    rover = Rover(location, heading)
    rover.move_backwards()
    assert rover.location.as_tuple() == expected
    assert rover.heading == rover.heading


@pytest.mark.parametrize(
    "coordinates,heading,expected",
    [
        ((0, 0), Heading.N, Heading.W),
        ((0, 1), Heading.W, Heading.S),
        ((-1, -1), Heading.W, Heading.S),
        ((1, 0), Heading.E, Heading.N),
        ((0, -2), Heading.S, Heading.E),
    ],
)
def test_rotate_left(
    coordinates: tuple[int, int],
    heading: Heading,
    expected: tuple[int, int],
):
    """Test that the Rover rotates left correctly."""
    location = Location(*coordinates)
    rover = Rover(location, heading)
    rover.rotate_left()
    assert rover.location.as_tuple() == coordinates
    assert rover.heading == expected


@pytest.mark.parametrize(
    "coordinates,heading,expected",
    [
        ((0, 0), Heading.N, Heading.E),
        ((0, 1), Heading.W, Heading.N),
        ((-1, -1), Heading.W, Heading.N),
        ((1, 0), Heading.E, Heading.S),
        ((0, -2), Heading.S, Heading.W),
    ],
)
def test_rotate_right(
    coordinates: tuple[int, int],
    heading: Heading,
    expected: tuple[int, int],
):
    """Test that the Rover rotates right correctly."""
    location = Location(*coordinates)
    rover = Rover(location, heading)
    rover.rotate_right()
    assert rover.location.as_tuple() == coordinates
    assert rover.heading == expected


@pytest.mark.parametrize(
    "coordinates,heading,obstacles,expected",
    [
        ((0, 0), Heading.N, {(-1, 1), (-1, -1)}, (0, 1)),
        ((0, 1), Heading.W, {(-1, 0), (-1, -1)}, (-1, 1)),
        ((-1, -1), Heading.W, {(-1, 1), (-1, -1)}, (-2, -1)),
        ((1, 0), Heading.E, {(-1, 1), (-1, -1)}, (2, 0)),
        ((0, -2), Heading.S, {(-1, 1), (-1, -1)}, (0, -3)),
        ((0, 0), Heading.N, {(0, 1), (-1, -1)}, (0, 0)),
        ((0, 1), Heading.W, {(-1, 1), (-1, -1)}, (0, 1)),
    ],
)
def test_move_forwards_with_obstacles(
    coordinates: tuple[int, int],
    heading: Heading,
    obstacles: set[tuple[int, int]],
    expected: tuple[int, int],
):
    """Test that the Rover moves forwards correctly."""
    location = Location(*coordinates)
    rover = Rover(location, heading, obstacles)
    rover.move_forwards()
    assert rover.location.as_tuple() == expected
    assert rover.heading == rover.heading
