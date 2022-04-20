import pytest
import random
from unittest import mock

import pytest

from _22_rpg_wizard import Enemy, \
    Player, \
    MagicMissileSpell, \
    DrainSpell, \
    ShieldSpell, \
    PoisonSpell, \
    RechargeSpell, \
    SpellBook, \
    encounter


def test_magic_missile_spell_damage(any_player):
    enemy = Enemy(20, 0)
    missile = MagicMissileSpell()

    missile.apply(any_player, enemy)

    assert enemy.hit_points == 20 - 4
    assert missile.is_active is False


def test_drain_spell(any_player):
    enemy = Enemy(100, 10)
    player_initial_health = any_player.hit_points
    enemy_initial_health = enemy.hit_points
    drain = DrainSpell()

    drain.apply(any_player, enemy)
    assert any_player.hit_points == player_initial_health + 2
    assert enemy.hit_points == enemy_initial_health - 2
    assert drain.is_active is False


def test_shield_spell():
    enemy = Enemy(100, 10)
    player = Player(100, 100, None, level='easy')
    shield = ShieldSpell()

    # cast turn
    shield.apply(player, enemy)
    assert player.armor == 0

    for x in range(6):
        shield.apply(player, enemy)

    # wears off
    shield.apply(player, enemy)
    assert player.armor == 0
    assert shield.is_active is False


def test_poison_spell():
    enemy = Enemy(100, 10)
    enemy_initial_health = enemy.hit_points
    player = Player(100, 100, None, level='easy')
    poison = PoisonSpell()

    poison.apply(player, enemy)
    assert enemy.hit_points == enemy_initial_health

    for x in range(6):
        poison.apply(player, enemy)
        assert enemy.hit_points == enemy_initial_health - 3 * (x + 1)

    # wears off
    poison.apply(player, enemy)
    assert enemy.hit_points == enemy_initial_health - 3 * 6
    assert player.armor == 0
    assert poison.is_active is False


def test_recharge_spell():
    enemy = Enemy(100, 10)
    player = Player(100, 100, None, level='easy')
    player_initial_mana = player.mana
    recharge = RechargeSpell()

    recharge.apply(player, enemy)
    assert player.mana == player_initial_mana

    for x in range(5):
        recharge.apply(player, enemy)
        assert player.mana == player_initial_mana + 101 * (x + 1)

    # wears off
    recharge.apply(player, enemy)
    assert player.mana == player_initial_mana + 5 * 101
    assert recharge.is_active is False


def test_deal_damage_to_player():
    player = Player(100, 100, None)

    player.deal_damage(5)

    assert player.hit_points == 95

    player.armor = 7
    player.deal_damage(5)

    assert player.hit_points == 94


@pytest.mark.parametrize(
    "casted_spell, when_will_pass, expected_active_effects", [
        (MagicMissileSpell, 1, {MagicMissileSpell}),
        (DrainSpell, 1, {DrainSpell}),
        (PoisonSpell, 6, {PoisonSpell}),
        (ShieldSpell, 6, {ShieldSpell}),
        (RechargeSpell, 5, {RechargeSpell})
    ])
def test_spell_book_active_effects(casted_spell, when_will_pass, expected_active_effects, any_player, any_enemy):
    spell_book = SpellBook()
    casted = spell_book.cast(casted_spell)

    assert set(map(type, spell_book.active_effects)) == expected_active_effects

    for x in range(when_will_pass + 1):
        casted.apply(any_player, any_enemy)

    assert len(spell_book.active_effects) == 0


@pytest.mark.parametrize(
    "casted_spells, expected_available_spells", [
        ([], {MagicMissileSpell, DrainSpell, ShieldSpell, PoisonSpell, RechargeSpell}),
        ([MagicMissileSpell], {MagicMissileSpell, DrainSpell, ShieldSpell, PoisonSpell, RechargeSpell}),
        ([DrainSpell], {MagicMissileSpell, DrainSpell, ShieldSpell, PoisonSpell, RechargeSpell}),
        ([PoisonSpell], {MagicMissileSpell, DrainSpell, ShieldSpell, RechargeSpell}),
        ([ShieldSpell], {MagicMissileSpell, DrainSpell, PoisonSpell, RechargeSpell}),
        ([RechargeSpell], {MagicMissileSpell, DrainSpell, PoisonSpell, ShieldSpell})
    ])
def test_spell_book_available_spells(casted_spells, expected_available_spells, any_player, any_enemy):
    spell_book = SpellBook()
    for spell in casted_spells:
        casted = spell_book.cast(spell)
        casted.apply(any_player, any_enemy)

    assert set(spell_book.available_spells) == expected_available_spells


@pytest.mark.parametrize(
    "spell, active_turns", [
        (ShieldSpell, 6),
        (DrainSpell, 7),
        (RechargeSpell, 7)
    ])
def test_available_spells_when_last_active_turn_shield(spell, active_turns):
    enemy = Enemy(100, 10)
    player = Player(100, 100, None)

    spell_book = SpellBook()
    shield = spell_book.cast(spell)

    for x in range(active_turns):
        shield.apply(player, enemy)

    assert spell_book.available_spells.index(spell) >= 0


def test_spell_book_next_spell(any_player, any_enemy):
    class SpellMatcher:
        def __eq__(self, other):
            assert set(other) == {MagicMissileSpell, DrainSpell}
            return True

    spell_book = SpellBook()
    for spell in {MagicMissileSpell, DrainSpell, ShieldSpell, PoisonSpell, RechargeSpell}:
        casted = spell_book.cast(spell)
        casted.apply(any_player, any_enemy)

    with mock.patch.object(random, "choice") as choice:
        spell_book.next_spell()
        choice.assert_called_with(SpellMatcher())


def test_effects_are_applied_before_enemy_turn():
    player = mock.MagicMock()
    enemy = mock.MagicMock()

    encounter(player, enemy)

    player.apply_effects.assert_called_once_with(enemy)


@pytest.mark.parametrize(
    "spell, spell_name", [
        (MagicMissileSpell(), "MagicMissileSpell"),
        (DrainSpell(), "DrainSpell"),
        (ShieldSpell(), "ShieldSpell"),
        (PoisonSpell(), "PoisonSpell"),
        (RechargeSpell(), "RechargeSpell"),
    ]
)
def test_spell_name(spell, spell_name):
    assert spell.name == spell_name


@pytest.fixture
def any_player():
    return Player(100, 100, None)


@pytest.fixture
def any_enemy():
    return Enemy(100, 100)
