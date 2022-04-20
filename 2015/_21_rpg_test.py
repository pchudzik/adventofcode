from _21_rpg import Character, encounter, simulate_battle


def test_encounter():
    player = Character(8, 5, 5)
    boss = Character(12, 7, 2)

    assert encounter(player, boss) is None
    assert boss.hit_points == 9
    assert player.hit_points == 6

    assert encounter(player, boss) is None
    assert boss.hit_points == 6
    assert player.hit_points == 4

    assert encounter(player, boss) is None
    assert boss.hit_points == 3
    assert player.hit_points == 2

    assert encounter(player, boss) is player
    assert boss.hit_points == 0
    assert player.hit_points == 2


def test_simulate_battle():
    player = Character(8, 5, 5)
    boss = Character(12, 7, 2)

    assert simulate_battle(player, boss) == player
