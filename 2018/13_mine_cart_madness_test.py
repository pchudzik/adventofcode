import pytest
import random
import importlib

module = importlib.import_module("13_mine_cart_madness")
parse = module.parse
carts_move_order = module.carts_move_order
Direction = module.Direction
Cart = module.Cart
Track = module.Track
detect_collisions = module.detect_collisions
simulator = module.simulator
simulator_last_cart_standing = module.simulator_last_cart_standing

looped_track = r"""/->-\        
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/   
"""


def test_focus_on_cart():
    carts = parse(looped_track)

    assert len(carts) == 2
    first_cart = [cart for cart in carts if cart.position == (2, 0)][0]
    second_cart = [cart for cart in carts if cart.position == (9, 3)][0]
    assert first_cart is not None
    assert second_cart is not None
    assert first_cart.direction == Direction.east
    assert second_cart.direction == Direction.south


def test_carts_move_order():
    cart1 = Cart((0, 1), Direction.north)
    cart2 = Cart((0, 3), Direction.north)
    cart3 = Cart((1, 0), Direction.north)
    cart4 = Cart((1, 1), Direction.north)
    cart5 = Cart((2, 3), Direction.north)
    carts = [cart2, cart5, cart1, cart4, cart3]
    random.shuffle(carts)

    sorted_carts = carts_move_order(carts)

    assert sorted_carts == [cart1, cart2, cart3, cart4, cart5]


@pytest.mark.parametrize("position, expected_moves", [
    ((0, 2), {Direction.north: (0, 1), Direction.south: (0, 3)}),  # straight vertical
    ((12, 2), {Direction.north: (12, 1), Direction.south: (12, 3)}),  # straight vertical
    ((9, 1), {Direction.west: (8, 1), Direction.east: (10, 1)}),  # straight horizontal
    ((6, 5), {Direction.west: (5, 5), Direction.east: (7, 5)}),  # straight horizontal
    ((0, 0), {Direction.west: (0, 1), Direction.north: (1, 0)}),  # curve: /
    ((12, 4), {Direction.east: (12, 3), Direction.south: (11, 4)}),  # curve: /
    ((4, 0), {Direction.north: (3, 0), Direction.east: (4, 1)}),  # curve \
    ((0, 4), {Direction.south: (1, 4), Direction.west: (0, 3)}),  # curve \
    ((7, 4), {Direction.west: (7, 3), Direction.south: (8, 4)})
])
def test_track_possible_moves_when_straight(position, expected_moves):
    track = Track(looped_track)

    assert track.possible_moves(position) == expected_moves


def test_track_possible_moves_intersection():
    track = Track(looped_track)
    assert track.possible_moves((4, 2)) == {
        Direction.north: (4, 1),
        Direction.east: (5, 2),
        Direction.south: (4, 3),
        Direction.west: (3, 2)
    }


@pytest.mark.parametrize(
    "start_position, start_direction, end_position, end_direction", [
        ((2, 0), Direction.east, (3, 0), Direction.east),
        ((2, 0), Direction.west, (1, 0), Direction.west),
        ((0, 1), Direction.north, (0, 0), Direction.north),
        ((0, 1), Direction.south, (0, 2), Direction.south),

        ((0, 0), Direction.north, (1, 0), Direction.east),
        ((0, 0), Direction.west, (0, 1), Direction.south),
        ((12, 4), Direction.east, (12, 3), Direction.north),
        ((12, 4), Direction.south, (11, 4), Direction.west),

        ((4, 0), Direction.north, (3, 0), Direction.west),
        ((4, 0), Direction.east, (4, 1), Direction.south),
        ((0, 4), Direction.west, (0, 3), Direction.north),
        ((0, 4), Direction.south, (1, 4), Direction.east),
    ])
def test_move_cart_straight(start_position, start_direction, end_position, end_direction):
    track = Track(looped_track)
    cart = Cart(start_position, start_direction)

    cart.move(track)

    assert cart.position == end_position
    assert cart.direction == end_direction


@pytest.mark.parametrize(
    "intersection_number, end_position, end_direction", [
        (0, (3, 2), Direction.west),
        (1, (4, 1), Direction.north),
        (2, (5, 2), Direction.east),
        (3, (3, 2), Direction.west),
        (4, (4, 1), Direction.north),
        (5, (5, 2), Direction.east)
    ])
def test_move_cart_intersection_heading_north(intersection_number, end_position, end_direction):
    track = Track(looped_track)
    cart = Cart((4, 2), Direction.north)
    cart.intersection_number = intersection_number

    cart.move(track)

    assert cart.position == end_position
    assert cart.direction == end_direction


@pytest.mark.parametrize(
    "intersection_number, end_position, end_direction", [
        (0, (5, 2), Direction.east),
        (1, (4, 3), Direction.south),
        (2, (3, 2), Direction.west),
        (3, (5, 2), Direction.east),
        (4, (4, 3), Direction.south),
        (5, (3, 2), Direction.west)
    ])
def test_move_cart_intersection_heading_south(intersection_number, end_position, end_direction):
    track = Track(looped_track)
    cart = Cart((4, 2), Direction.south)
    cart.intersection_number = intersection_number

    cart.move(track)

    assert cart.position == end_position
    assert cart.direction == end_direction


@pytest.mark.parametrize(
    "intersection_number, end_position, end_direction", [
        (0, (4, 1), Direction.north),
        (1, (5, 2), Direction.east),
        (2, (4, 3), Direction.south),
        (3, (4, 1), Direction.north),
        (4, (5, 2), Direction.east),
        (5, (4, 3), Direction.south),
    ])
def test_move_cart_intersection_heading_east(intersection_number, end_position, end_direction):
    track = Track(looped_track)
    cart = Cart((4, 2), Direction.east)
    cart.intersection_number = intersection_number

    cart.move(track)

    assert cart.position == end_position
    assert cart.direction == end_direction


@pytest.mark.parametrize(
    "intersection_number, end_position, end_direction", [
        (0, (4, 3), Direction.south),
        (1, (3, 2), Direction.west),
        (2, (4, 1), Direction.north),
        (3, (4, 3), Direction.south),
        (4, (3, 2), Direction.west),
        (5, (4, 1), Direction.north),
    ])
def test_move_cart_intersection_heading_west(intersection_number, end_position, end_direction):
    track = Track(looped_track)
    cart = Cart((4, 2), Direction.west)
    cart.intersection_number = intersection_number

    cart.move(track)

    assert cart.position == end_position
    assert cart.direction == end_direction


def test_detect_collision():
    carts_no_collision = [
        Cart((0, 0), Direction.east),
        Cart((1, 0), Direction.west)
    ]

    carts_with_collision = [
        Cart((1, 0), Direction.east),
        Cart((1, 0), Direction.west)
    ]

    assert detect_collisions(carts_no_collision) == []

    collisions = detect_collisions(carts_with_collision)
    assert len(collisions) == 1
    assert collisions[0] == (1, 0)


def test_simulator():
    track = Track(looped_track)
    carts = parse(looped_track)

    collision = simulator(track, carts)

    assert collision == (7, 3)


def test_simulator_last_cart_standing():
    puzzle = r"""/>-<\  
|   |  
| /<+-\
| | | v
\>+</ |
  |   ^
  \<->/"""
    track = Track(puzzle)
    carts = parse(puzzle)

    last_cart = simulator_last_cart_standing(track, carts)

    assert last_cart == (6, 4)
