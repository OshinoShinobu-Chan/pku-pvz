from zombie import Zombie

class ShiGongJiangShi(Zombie):
    def __init__(self, pos, json_path, name, tick, life, item_name):
        super().__init__(pos, json_path, name, tick, life, item_name)
        self.real_life = 270
        self.interval = 6

    def update(self, event, status):
        if self.life <= 0:
            super().remove(status)
            return False
        if self.check_lose(status):
            return True
        if self.life <= self.real_life:
            self.interval = 3

        if status.global_ticks % self.interval != 0:
            return True
        self.can_move = super().check_move(status)
        self.move(status)
        self.attack(status)
        return True

    def attack(self, status):
        status.zombies_harm[self.left_index[0]][self.left_index[1]] += 3