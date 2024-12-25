from ursina import *
from enemy import Enemy
import random
from dialog import Dialog
def setup_epilog(enemy, subject, score_manager, shootables_parent, remove_enemy_callback):

    # Флаг для отслеживания начального состояния
    game_started = False

    # Создание начального врага
    initial_enemy = enemy

    def start_dialog():
        Dialog(character=initial_enemy, player=initial_enemy.player, dialog_dict={'1':'43242','2':'42432','3':'fsewfew'}).start_dialog()


    def update():
        nonlocal game_started
        if not game_started:
            # Проверяем расстояние до начального врага
            distance = ((subject.x - initial_enemy.x)**2 + (subject.z - initial_enemy.z)**2)**0.5
            if distance < 5:  # Если игрок достаточно близко
                return start_dialog()
            return []  # Пока игра не началась, возвращаем пустой список врагов

        return None  # Если игра началась, не создаем новых врагов

    return update
