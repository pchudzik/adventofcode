"""
--- Day 21: RPG Simulator 20XX ---

Little Henry Case got a new video game for Christmas. It's an RPG, and he's stuck on a boss. He needs to know what
equipment to buy at the shop. He hands you the controller.

In this game, the player (you) and the enemy (the boss) take turns attacking. The player always goes first. Each attack
reduces the opponent's hit points by at least 1. The first character at or below 0 hit points loses.

Damage dealt by an attacker each turn is equal to the attacker's damage score minus the defender's armor score. An
attacker always does at least 1 damage. So, if the attacker has a damage score of 8, and the defender has an armor score
of 3, the defender loses 5 hit points. If the defender had an armor score of 300, the defender would still lose 1 hit
point.

Your damage score and armor score both start at zero. They can be increased by buying items in exchange for gold. You
start with no items and have as much gold as you need. Your total damage or armor is equal to the sum of those stats
from all of your items. You have 100 hit points.

Here is what the item shop is selling:

Weapons:    Cost  Damage  Armor
Dagger        8     4       0
Shortsword   10     5       0
Warhammer    25     6       0
Longsword    40     7       0
Greataxe     74     8       0

Armor:      Cost  Damage  Armor
Leather      13     0       1
Chainmail    31     0       2
Splintmail   53     0       3
Bandedmail   75     0       4
Platemail   102     0       5

Rings:      Cost  Damage  Armor
Damage +1    25     1       0
Damage +2    50     2       0
Damage +3   100     3       0
Defense +1   20     0       1
Defense +2   40     0       2
Defense +3   80     0       3

You must buy exactly one weapon; no dual-wielding. Armor is optional, but you can't use more than one. You can buy 0-2
rings (at most one for each hand). You must use any items you buy. The shop only has one of each item, so you can't buy,
for example, two rings of Damage +3.

For example, suppose you have 8 hit points, 5 damage, and 5 armor, and that the boss has 12 hit points, 7 damage, and 2
armor:

The player deals 5-2 = 3 damage; the boss goes down to 9 hit points.
The boss deals 7-5 = 2 damage; the player goes down to 6 hit points.
The player deals 5-2 = 3 damage; the boss goes down to 6 hit points.
The boss deals 7-5 = 2 damage; the player goes down to 4 hit points.
The player deals 5-2 = 3 damage; the boss goes down to 3 hit points.
The boss deals 7-5 = 2 damage; the player goes down to 2 hit points.
The player deals 5-2 = 3 damage; the boss goes down to 0 hit points.
In this scenario, the player wins! (Barely.)

You have 100 hit points. The boss's actual stats are in your puzzle input. What is the least amount of gold you can
spend and still win the fight?

Your puzzle answer was 121.

--- Part Two ---

Turns out the shopkeeper is working with the boss, and can persuade you to buy whatever items he wants. The other rules
still apply, and he still only has one of each item.

What is the most amount of gold you can spend and still lose the fight?

Your puzzle answer was 201.
"""


class Character:
    def __init__(self, hit_points, damage, armor, inventory_cost=0):
        self.hit_points = hit_points
        self.damage = damage
        self.armor = armor
        self.inventory_cost = inventory_cost

    def attack(self, other_character):
        damage = self.damage - other_character.armor
        other_character.hit_points -= damage if damage >= 1 else 1

        return self.is_alive and other_character.is_alive

    @property
    def is_alive(self):
        return self.hit_points > 0


def encounter(character1, character2):
    both_live = character1.attack(character2)

    if both_live:
        both_live = character2.attack(character1)

    if not both_live:
        return character1 if character1.is_alive else character2


class Inventory:
    def __init__(self, cost, damage, armor):
        self.cost = cost
        self.damage = damage
        self.armor = armor


weapons = [
    Inventory(cost, damage, 0) for cost, damage in [
        (8, 4),
        (10, 5),
        (25, 6),
        (40, 7),
        (74, 8)
    ]
]

armors = [
    Inventory(cost, 0, armor) for cost, armor in [
        (0, 0),
        (13, 1),
        (31, 2),
        (53, 3),
        (75, 4),
        (102, 5)
    ]
]

rings = [
    Inventory(cost, damage, armor) for cost, damage, armor in [
        (0, 0, 0),
        (0, 0, 0),
        (25, 1, 0),
        (50, 2, 0),
        (100, 3, 0),
        (20, 0, 1),
        (40, 0, 2),
        (80, 0, 3)
    ]
]


def character_variant(hit_points):
    for weapon in weapons:
        for armor in armors:
            for left_hand_ring in rings:
                for right_hand_ring in [ring for ring in rings if ring != left_hand_ring]:
                    equipment = [weapon, armor, left_hand_ring, right_hand_ring]
                    yield Character(
                        hit_points=hit_points,
                        damage=sum(e.damage for e in equipment),
                        armor=sum(e.armor for e in equipment),
                        inventory_cost=sum(e.cost for e in equipment))


def simulate_battle(character1, character2):
    winner = None

    while winner is None:
        winner = encounter(character1, character2)

    return winner


def find_winners(boss_stats, is_player_winner=True):
    for player in character_variant(100):
        boss = Character(**boss_stats)
        winner = simulate_battle(player, boss)
        expected_winner = player if is_player_winner else boss
        if winner == expected_winner:
            yield player


def find_cheapest_winning_inventory(victors):
    return min(victor.inventory_cost for victor in victors)


def find_most_expensive_losing_inventory(losers):
    return max(loser.inventory_cost for loser in losers)


if __name__ == "__main__":
    boss_stats = {
        "hit_points": 103,
        "damage": 9,
        "armor": 2
    }

    player_victors = find_winners(boss_stats, is_player_winner=True)
    player_losers = find_winners(boss_stats, is_player_winner=False)
    print("Cheapest inventory: {}".format(find_cheapest_winning_inventory(player_victors)))
    print("Most expensive losing inventory: {}".format(find_most_expensive_losing_inventory(player_losers)))
