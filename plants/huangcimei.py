from plant import Plant

class HuangCiMei(Plant):
    def __init__(self, pos, json_path, name, tick, life, sun, to_cold_time, item_name):
        super().__init__(pos, json_path, name, tick, life, sun, to_cold_time, item_name)
        self.status = 0
        self.attack_interval = 300
        self.last_attack_time = tick
    
    def attack(self, status, harm_value):
        self.last_attack_time = status.global_ticks
        for i in range(self.index[0] - 1, self.index[0] + 2):
            for j in range(self.index[1] - 1, self.index[1] + 2):
                if i < 9 and i >= 0 and j < 5 and j >= 0:
                    status.planted_aoe_harm[i][j] += harm_value
    
    def update(self, event, status):
        if not self.is_planted:
            return super().not_planted(event, status)
        if self.status == 0 and status.global_ticks - self.start_tick >= 600:
            self.status = 1
        elif self.status == 1:
            if status.global_ticks - self.start_tick >= 1800:
                self.status = 2
            if status.global_ticks - self.last_attack_time >= self.attack_interval:
                self.attack(status, 30)
        elif self.status == 2 and status.global_ticks - self.last_attack_time >= self.attack_interval:
            self.attack(status, 50)
        return super().check_life(event, status)