from ursina import *
from ursina.shaders import lit_with_shadows_shader


class Gun(Entity):

    def __init__(self, texture, model, **kwargs):
        super().__init__(**kwargs)
        self.is_shooting = False
        self.bob_amplitude = 0.005
        self.bob_frequency = 4

        self.arm = Entity(
            parent=camera,
            model=model,
            texture=texture,
            rotation=Vec3(0, 85, 4),
            position=Vec3(0.35, -0.6, 1),
            scale=1.5,
            shader=lit_with_shadows_shader,
            fllipped_faces=True,
            double_sided=False,
            on_cooldown=False
        )

    def active(self):
        self.arm.position = Vec3(0.35, -0.6, 1)

    def shoot(self):

        self.arm.rotation_z += 15
        self.muzzle_flash.enabled = True
        invoke(self.muzzle_flash.disable, delay=0.05)
        invoke(lambda: setattr(self.arm, 'rotation_z', self.arm.rotation_z - 15), delay=0.2)
        invoke(setattr, self, 'is_shooting', False, delay=0.5)

    def update(self):
        t = time.time() * self.bob_frequency
        self.arm.rotation_z += sin(t) * self.bob_amplitude * 10
        self.arm.rotation_x += cos(t) * self.bob_amplitude * 5

        if any(held_keys[k] for k in ['w', 'a', 's', 'd']):
            self.bob_amplitude = 0.03
            self.active()
        else:
            self.bob_amplitude = 0.005

