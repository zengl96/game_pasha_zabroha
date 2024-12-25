from ursina import Text, color
from enemy import Enemy


class ScoreManager:
    def __init__(self):
        self.score = 0
        self.level = 1
        self.score_text = Text(f'Score: {self.score}', position=(-0.85, 0.45), scale=2, color=color.white)
        self.level_text = Text(f'Level: {self.level}', position=(-0.85, 0.4), scale=2, color=color.white)

    def update_score(self, points):
        self.score += points
        self.score_text.text = f'Score: {self.score}'
        self.check_level_up()

    def check_level_up(self):
        if self.score >= self.level * 100:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.level_text.text = f'Level: {self.level}'
        self.increase_enemy_speed()
        if self.level > 4:
            alert_text = Text(f'Босс!!', position=(0, 0.4), scale=2, color=color.red)
            alert_text.fade_out(duration=3)

    def increase_enemy_speed(self):
        Enemy.speed *= 1.03
