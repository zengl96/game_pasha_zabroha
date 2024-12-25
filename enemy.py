from ursina import *
import random


# Создаем врагов
class Enemy(Entity):
    speed = 1.8

    def __init__(self, shootables_parent, player, score_manager, on_death_callback=None,speed=None,**kwargs):
        super().__init__(parent=shootables_parent, texture=f"textures/{random.randint(1, 5)}.jpg", model='cube',
                         scale_y=5, scale_x=2.5, scale_z=2.5, origin_y=-.5,
                         color=color.light_gray, collider='box', **kwargs)
        self.player = player
        self.health_bar = Entity(parent=self, y=1.2, model='cube', color=color.red, world_scale=(1.5, .1, .1))
        self.max_hp = 100
        self.hp = self.max_hp
        self.on_death_callback = on_death_callback
        self.score_manager = score_manager

        if speed != None:
            self.speed = speed
            
    def update(self):
        dist = distance_xz(self.player.position, self.position)
        if dist > 90:  # 40
            return

        self.health_bar.alpha = max(0, self.health_bar.alpha - time.dt)

        self.look_at_2d(self.player.position, 'y')
        hit_info = raycast(self.world_position + Vec3(0, 1, 0), self.forward, 1000, ignore=(self,))
        if hit_info.entity >= self.player:  # ==
            if dist > 2:
                self.position += self.forward * time.dt * self.speed

    def dead(self):
        target_rotation = self.rotation_z - 90
        duration = 0.5  # Общее время падения
        self.speed = 0
        # Плавная анимация поворота
        self.animate('rotation_z', target_rotation, duration=duration, curve=curve.in_out_quad)

        # Удаляем объект после анимации
        if self.on_death_callback:
            invoke(self.on_death_callback, self, delay=duration)

        invoke(lambda: destroy(self), delay=duration + 0.1)

    def add_points(self):
        self.score_manager.update_score(25)

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        self._hp = value
        if value <= 0:
            self.dead()
            self.add_points()  # Добавляем 10 очков за уничтожение врага
            return

        self.health_bar.world_scale_x = self.hp / self.max_hp * 1.5
        self.health_bar.alpha = 1


class Boss(Enemy):
    def __init__(self, speed, shootables_parent, player, score_manager, on_death_callback=None, **kwargs):
        super().__init__(
            shootables_parent=shootables_parent,
            player=player,
            score_manager=score_manager,
            on_death_callback=on_death_callback,
            **kwargs
        )
        self.max_hp = 500
        self.hp = self.max_hp
        self.speed = speed
        self.scale = Vec3(5, 5, 5)
        self.color = color.red

    def add_points(self):
        self.score_manager.update_score(1000)
