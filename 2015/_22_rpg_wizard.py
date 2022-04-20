import random
import sys

"""
--- Day 22: Wizard Simulator 20XX ---

Little Henry Case decides that defeating bosses with swords and stuff is boring. Now he's playing the game with a
wizard. Of course, he gets stuck on another boss and needs your help again.

In this version, combat still proceeds with the player and the boss taking alternating turns. The player still goes
first. Now, however, you don't get any equipment; instead, you must choose one of your spells to cast. The first
character at or below 0 hit points loses.

Since you're a wizard, you don't get to wear armor, and you can't attack normally. However, since you do magic damage,
your opponent's armor is ignored, and so the boss effectively has zero armor as well. As before, if armor (from a spell,
in this case) would reduce damage below 1, it becomes 1 instead - that is, the boss' attacks always deal at least 1
damage.

On each of your turns, you must select one of your spells to cast. If you cannot afford to cast any spell, you lose.
Spells cost mana; you start with 500 mana, but have no maximum limit. You must have enough mana to cast a spell, and its
cost is immediately deducted when you cast it. Your spells are Magic Missile, Drain, Shield, Poison, and Recharge.

Magic Missile costs 53 mana. It instantly does 4 damage.

Drain costs 73 mana. It instantly does 2 damage and heals you for 2 hit points.

Shield costs 113 mana. It starts an effect that lasts for 6 turns. While it is active, your armor is increased by 7.

Poison costs 173 mana. It starts an effect that lasts for 6 turns. At the start of each turn while it is active, it
deals the boss 3 damage.

Recharge costs 229 mana. It starts an effect that lasts for 5 turns. At the start of each turn while it is active, it
gives you 101 new mana.

Effects all work the same way. Effects apply at the start of both the player's turns and the boss' turns. Effects are
created with a timer (the number of turns they last); at the start of each turn, after they apply any effect they have,
their timer is decreased by one. If this decreases the timer to zero, the effect ends. You cannot cast a spell that
would start an effect which is already active. However, effects can be started on the same turn they end.

For example, suppose the player has 10 hit points and 250 mana, and that the boss has 13 hit points and 8 damage:

-- Player turn --
- Player has 10 hit points, 0 armor, 250 mana
- Boss has 13 hit points
Player casts Poison.

-- Boss turn --
- Player has 10 hit points, 0 armor, 77 mana
- Boss has 13 hit points
Poison deals 3 damage; its timer is now 5.
Boss attacks for 8 damage.

-- Player turn --
- Player has 2 hit points, 0 armor, 77 mana
- Boss has 10 hit points
Poison deals 3 damage; its timer is now 4.
Player casts Magic Missile, dealing 4 damage.

-- Boss turn --
- Player has 2 hit points, 0 armor, 24 mana
- Boss has 3 hit points
Poison deals 3 damage. This kills the boss, and the player wins.
Now, suppose the same initial conditions, except that the boss has 14 hit points instead:

-- Player turn --
- Player has 10 hit points, 0 armor, 250 mana
- Boss has 14 hit points
Player casts Recharge.

-- Boss turn --
- Player has 10 hit points, 0 armor, 21 mana
- Boss has 14 hit points
Recharge provides 101 mana; its timer is now 4.
Boss attacks for 8 damage!

-- Player turn --
- Player has 2 hit points, 0 armor, 122 mana
- Boss has 14 hit points
Recharge provides 101 mana; its timer is now 3.
Player casts Shield, increasing armor by 7.

-- Boss turn --
- Player has 2 hit points, 7 armor, 110 mana
- Boss has 14 hit points
Shield's timer is now 5.
Recharge provides 101 mana; its timer is now 2.
Boss attacks for 8 - 7 = 1 damage!

-- Player turn --
- Player has 1 hit point, 7 armor, 211 mana
- Boss has 14 hit points
Shield's timer is now 4.
Recharge provides 101 mana; its timer is now 1.
Player casts Drain, dealing 2 damage, and healing 2 hit points.

-- Boss turn --
- Player has 3 hit points, 7 armor, 239 mana
- Boss has 12 hit points
Shield's timer is now 3.
Recharge provides 101 mana; its timer is now 0.
Recharge wears off.
Boss attacks for 8 - 7 = 1 damage!

-- Player turn --
- Player has 2 hit points, 7 armor, 340 mana
- Boss has 12 hit points
Shield's timer is now 2.
Player casts Poison.

-- Boss turn --
- Player has 2 hit points, 7 armor, 167 mana
- Boss has 12 hit points
Shield's timer is now 1.
Poison deals 3 damage; its timer is now 5.
Boss attacks for 8 - 7 = 1 damage!

-- Player turn --
- Player has 1 hit point, 7 armor, 167 mana
- Boss has 9 hit points
Shield's timer is now 0.
Shield wears off, decreasing armor by 7.
Poison deals 3 damage; its timer is now 4.
Player casts Magic Missile, dealing 4 damage.

-- Boss turn --
- Player has 1 hit point, 0 armor, 114 mana
- Boss has 2 hit points
Poison deals 3 damage. This kills the boss, and the player wins.

You start with 50 hit points and 500 mana points. The boss's actual stats are in your puzzle input. What is the least
amount of mana you can spend and still win the fight? (Do not include mana recharge effects as "spending" negative
mana.)

Your puzzle answer was 953.

--- Part Two ---

On the next run through the game, you increase the difficulty to hard.

At the start of each player turn (before any other effects apply), you lose 1 hit point. If this brings you to or below
0 hit points, you lose.

With the same starting stats for you and the boss, what is the least amount of mana you can spend and still win the
fight?

Your puzzle answer was 1289.
"""


class Spell:
    def __init__(self, cost, timer):
        self.cost = cost
        self.initial_timer = timer
        self.timer = timer

    @property
    def is_active(self):
        return self.timer > 0

    @property
    def can_cast(self):
        return self.is_active and (self.initial_timer > self.timer or self.initial_timer == 1)

    def apply(self, player, enemy):
        if self.can_cast:
            self._player_effect(player)
            self._enemy_effect(enemy)
        self.timer -= 1

    @property
    def name(self):
        return type(self).__name__

    def _player_effect(self, player):
        raise NotImplementedError()

    def _enemy_effect(self, enemy):
        raise NotImplementedError()


class MagicMissileSpell(Spell):
    cost = 53

    def __init__(self):
        Spell.__init__(self, MagicMissileSpell.cost, 1)

    def _player_effect(self, player):
        pass

    def _enemy_effect(self, enemy):
        enemy.deal_damage(4)


class DrainSpell(Spell):
    cost = 73

    def __init__(self):
        Spell.__init__(self, DrainSpell.cost, 1)

    def _player_effect(self, player):
        player.hit_points += 2

    def _enemy_effect(self, enemy):
        enemy.deal_damage(2)


class ShieldSpell(Spell):
    cost = 113

    def __init__(self):
        Spell.__init__(self, ShieldSpell.cost, 7)

    def _player_effect(self, player):
        player.armor = 7

        if self.timer <= 1:
            player.armor = 0

    def _enemy_effect(self, enemy):
        pass


class PoisonSpell(Spell):
    cost = 173

    def __init__(self):
        Spell.__init__(self, PoisonSpell.cost, 7)

    def _player_effect(self, player):
        pass

    def _enemy_effect(self, enemy):
        enemy.deal_damage(3)


class RechargeSpell(Spell):
    cost = 229

    def __init__(self):
        Spell.__init__(self, RechargeSpell.cost, 6)

    def _player_effect(self, player):
        player.mana += 101

    def _enemy_effect(self, enemy):
        pass


class Enemy:
    def __init__(self, hit_points, damage):
        self.hit_points = hit_points
        self.damage = damage

    def attack(self, player):
        player.deal_damage(self.damage)
        return self.is_alive and player.is_alive

    def deal_damage(self, damage):
        self.hit_points -= damage

    @property
    def is_alive(self):
        return self.hit_points > 0


class Player:
    def __init__(self, hit_points, mana, spell_book, level='easy', max_mana_to_spend=sys.maxsize):
        self.hit_points = hit_points
        self.mana = mana
        self.spell_book = spell_book
        self.spend_mana = 0
        self.casted_spells = []
        self.armor = 0
        self.level = level
        self.max_mana_spend = max_mana_to_spend

    def attack(self, enemy):
        if self.level == 'hard':
            self.hit_points -= 1

        if not self.is_alive:
            return False

        next_spell = self.spell_book.next_spell()

        self.__record_spell(next_spell)

        if self.is_alive:
            self.apply_effects(enemy)

        return self.is_alive and enemy.is_alive

    @property
    def is_alive(self):
        return self.hit_points > 0 and self.mana > 0 and self.spend_mana < self.max_mana_spend

    def deal_damage(self, value):
        damage = value - self.armor
        self.hit_points -= damage if damage > 1 else 1

    def __record_spell(self, next_spell):
        self.mana -= next_spell.cost
        self.spend_mana += next_spell.cost
        self.casted_spells += [next_spell]

    def apply_effects(self, enemy):
        for effect in self.spell_book.active_effects:
            effect.apply(self, enemy)

        return self.is_alive and enemy.is_alive


class SpellBook:
    all_spells = (MagicMissileSpell, DrainSpell, ShieldSpell, PoisonSpell, RechargeSpell)

    def __init__(self):
        self.active_spells = []

    @property
    def active_effects(self):
        self.active_spells = list(filter(lambda s: s.is_active, self.active_spells))
        return tuple(self.active_spells)

    @property
    def available_spells(self):
        return tuple(filter(
            lambda spell: spell not in map(type, filter(lambda s: s.timer > 1, self.active_spells)),
            SpellBook.all_spells))

    def next_spell(self):
        next = random.choice(self.available_spells)()
        self.active_spells += [next]
        return next

    def cast(self, spell):
        casted_spell = spell()
        self.active_spells += [casted_spell]
        return casted_spell


def encounter(player, enemy):
    both_live = player.attack(enemy)

    if both_live:
        both_live = player.apply_effects(enemy)

    if both_live:
        both_live = enemy.attack(player)

    if not both_live:
        return player if player.is_alive else enemy


def encounter_simulator(number_of_simulations, level='easy'):
    winning_player = None

    for encounter_index in range(number_of_simulations):
        max_mana_spend = sys.maxsize
        if winning_player:
            max_mana_spend = winning_player.spend_mana

        player = Player(50, 500, SpellBook(), level=level, max_mana_to_spend=max_mana_spend)
        enemy = Enemy(55, 8)
        result = encounter(player, enemy)
        while not result:
            result = encounter(player, enemy)
            if winning_player and player.spend_mana > winning_player.spend_mana:
                break

        if result is player and (not winning_player or result.spend_mana < winning_player.spend_mana):
            winning_player = result
            print("Player[{}] on {} level won with spending {} on {}".format(
                encounter_index,
                level,
                player.spend_mana,
                list(map(lambda s: s.name, player.casted_spells))
            ))
    return winning_player


if __name__ == "__main__":
    winner = encounter_simulator(1000000, level='easy')
    least_spend_encounter = winner
    print("Part 1 result: Player on easy level won with spending {} on {}".format(
        least_spend_encounter.spend_mana,
        list(map(lambda s: s.name, least_spend_encounter.casted_spells))
    ))

    winner = encounter_simulator(1000000, level='hard')
    least_spend_encounter = winner
    print("Part 2 result: Player on hard level won with spending {} on {}".format(
        least_spend_encounter.spend_mana,
        list(map(lambda s: s.name, least_spend_encounter.casted_spells))
    ))
