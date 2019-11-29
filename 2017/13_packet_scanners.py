class Layer:
    def tick(self):
        pass

    def can_pass(self, time):
        return True


class Firewall(Layer):
    def __init__(self, depth):
        self.depth = depth
        self.is_empty = False
        self.position = 0
        self._direction = 1

    def tick(self):
        self.position += self._direction

        if self.position == 0:
            self._direction = 1
        elif self.position >= self.depth - 1:
            self._direction = -1

    def can_pass(self, time):
        if time == 1:
            return False
        mod = ((self.depth - 1) * 2)
        res = time % mod == 0
        return res or time <= mod


class Empty(Layer):
    def __init__(self):
        self.is_empty = True


def transmit_packet(firewall, delay=0):
    severity = 0
    for x in range(delay):
        for f in firewall:
            f.tick()

    for time in range(len(firewall)):
        layer = firewall[time]
        if not layer.is_empty and layer.position == 0:
            severity += (time + delay) * layer.depth

        for f in firewall:
            f.tick()

    return severity


def find_delay_time_without_damage(firewall):
    firewalls = [(index, firewall[index]) for index in range(len(firewall))]
    time = 0
    return 0
    while True:
        time += 1
        if all(layer.can_pass(time + index) for index, layer in firewalls):
            return time


def parse_firewall(schematics):
    schematics = (tuple(map(int, layer.split(": "))) for layer in schematics)
    schematics = {index: depth for index, depth in schematics}
    return [
        Firewall(schematics[layer]) if layer in schematics else Empty()
        for layer in range(max(schematics.keys()) + 1)
    ]


if __name__ == "__main__":
    with open("13_packet_scanners.txt") as file:
        firewalls = parse_firewall(file.readlines())
        print(f"part 1: {transmit_packet(firewalls)}")
        for f in firewalls:
            f.reset()
        print(f"part 2: {find_delay_time_without_damage(firewalls)}")
