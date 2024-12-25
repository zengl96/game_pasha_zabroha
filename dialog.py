from ursina import *
import math


class Dialog(Entity):
    def __init__(self, character, player, dialog_dict):
        self.character = character
        self.player = player
        self.dialog_dict = dialog_dict
        self.dialog_index = -1
        self.player = player
        self.camera = camera
        self._ = True
        self.player.speed = 0
        self.player.camera_pivot.z = -5.5  # move the camera behind the player model
        self.player.camera_pivot.y = 5.5 
        self.player.camera_pivot.x = 5.5 
        self.camera.rotation_y -= 25
        self.camera.enabled = False
        self.button = Button(scale=(1.5,.2), position=(0, -0.35), text='')
        side_texture = Entity(
            parent=self.button,
            model='quad',
            texture=character.texture,  # Путь к вашей текстуре
            scale=(0.1, 0.8),  # Размер текстуры
            position=(-0.4, 0)  # Размещение текстуры справа от кнопки
        )
        side_texture2 = Entity(
            parent=self.button,
            model='quad',
            texture=player.texture,  # Путь к вашей текстуре
            scale=(0.1, 0.8),  # Размер текстуры
            position=(0.4, 0)  # Размещение текстуры справа от кнопки
        )

    def show_next_dialog(self):
        if self.dialog_index < len(self.dialog_dict):
            self.button.text = list(self.dialog_dict.values())[self.dialog_index]
        else:
            return self.end_dialog()  

    def end_dialog(self):
        # Убираем диалоговое окно
        destroy(self.button)
        self.player.camera_pivot.z = 0  # move the camera behind the player model
        self.player.camera_pivot.y = 2 
        self.player.camera_pivot.x = 0 
        self.camera.rotation_y += 25
        self.camera.enabled = True
        self.player.speed = 8 # Устанавливаем скорость персонажа на обычную (или на нужное вам значение)

        return 1

    def update(self):
        if held_keys['e'] and self._ == True:
            self.dialog_index += 1
            self._ = False
            return self.show_next_dialog()
        if not held_keys['e']:
            self._ = True