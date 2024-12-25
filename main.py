from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

from enemy import Boss, Enemy
from gun import Gun
from score_and_lvl import ScoreManager
from terrain import MeshTerrain
from random import random
from landscale import Map
from UrsinaLighting import LitDirectionalLight, LitPointLight, LitSpotLight, LitObject, LitInit
from ursina.shaders import lit_with_shadows_shader

import random
from dialog import Dialog
from gamestate import game_state
# Словарь диалогов

# Возможные состояния игры



app = Ursina()
lit = LitInit()

# player = FirstPersonController(model='cube', z=-10, color=color.orange, origin_y=-.5, speed=8, collider='box')

subject = FirstPersonController(
    model='cube',
    x=50,
    z=50,
    color=color.orange,
    origin_y=-.5,
    speed=8,
    collider='box',
    texture=r'textures\t.jpeg'
)


subject.collider = BoxCollider(subject, Vec3(0, 1, 0), Vec3(1, 2, 1))

subject.gravity = 0.0
# subject.x = 15
# subject.z = 15

pX = subject.x
pZ = subject.z

scene.fog_density = (0, 95)
scene.fog_color = color.gray

Audio('assets/thykier-the-limit.mp3', True)
grass_audio = Audio('assets/step.ogg', autoplay=False, loop=False)
water_swim = Audio('assets/water-swim.mp3', autoplay=False, loop=False)

arm_texture = load_texture('assets/arm_texture.png')
skyboxTexture = Texture("textures/skybox.jpg")


map = Map(1371)
terrain = MeshTerrain(map.landscale_mask)

skybox = Sky(model="sphere", double_sided=True, texture=skyboxTexture, rotation=(0, 90, 0))
water = LitObject(position=(floor(terrain.subWidth / 2), -0.1, floor(terrain.subWidth / 2)), scale=terrain.subWidth,
                  water=True, cubemapIntensity=0.75, collider='box', texture_scale=(terrain.subWidth, terrain.subWidth),
                  ambientStrength=0.5)


# Объект очков и уровня
score_manager = ScoreManager()


# Функция для обновления очков и уровня
def update_score(points):
    score_manager.update_score(points)


# Создания первого оружия
gun = Gun(parent=camera, model='assets/uploads_files_2614590_Shotgun_Model.obj',
          texture=r'textures\Shotgun_HDRP_BaseMap.png')
gun.muzzle_flash = Entity(parent=gun, z=1, world_scale=.05, model='quad', color=color.yellow, enabled=False)

# Добавление вспышки при выстреле
shootables_parent = Entity()
mouse.traverse_target = shootables_parent


def remove_enemy(enemy):
    """Удаляет врага или босса из игры."""
    if isinstance(enemy, Boss):
        boss.remove(enemy)  # Удалить из списка боссов
    else:
        enemies.remove(enemy)  # Удалить из списка врагов


# Создание врагов
enemies = []
boss = []
dialogs = []




# button = Button(scale=(1.5,.2), position=(0, -0.35), text='')  # Текст изначально пуст

# full_text = """StartSttStartSt"""
# button.text = full_text
# Функция для анимации печатания
# def typewriter_animation(button, text, delay=0.1):
#     # Печатает текст с задержкой для анимации
#     for i in range(1, len(text) + 1):
#         button.text = text[:i]
#         invoke(lambda:  '', delay=0.1) # Задержка между символами для анимации

# Функция для обновления текста и добавления анимации
# def update_text_with_animation():
#     # Разбиваем текст на несколько строк, если нужно
#     wrapped_text = '\n'.join([full_text[i:i+30] for i in range(0, len(full_text), 30)])  # Разбивает текст на строки по 30 символов

#     # Запуск анимации печатания
#     typewriter_animation(button, wrapped_text)

# Запуск анимации
# update_text_with_animation()




# Пауза и управление
def pause_input(key):
    if key == 'escape':
        quit()


# def input(key):
#     terrain.input(key)


count = 0

def update():
    global enemies, boss, dialogs, game_state
    global count, pX, pZ

    count += 1
    if count == 4:
        count = 0
        terrain.update(subject.position, camera)

    # Change subset position based on subject position.
    if abs(subject.x - pX) > 1 or abs(subject.z - pZ) > 1:
        pX = subject.x
        pZ = subject.z

        if subject.y >= 0 and grass_audio.playing == False:
            grass_audio.pitch = random.random() + 0.7
            grass_audio.play()
        elif subject.y < 0 and water_swim.playing == False:
            water_swim.pitch = random.random() + 0.3
            water_swim.play()

    blockFound = False
    height = 1.76

    x = floor(subject.x + 0.5)
    z = floor(subject.z + 0.5)
    y = floor(subject.y + 0.5)
    for step in range(-2, 2):
        if terrain.td.get((x, y + step, z)) == "t":
            # ***
            # Now make sure there isn't a block on top...
            if terrain.td.get((x, y + step + 1, z)) != "t":
                target = y + step + height
                blockFound = True
                break
            else:
                target = y + step + height + 1
                blockFound = True
                break
    if blockFound == True:
        # Step up or down :>
        subject.y = lerp(subject.y, target, 6 * time.dt)
    else:
        subject.y -= 9.8 * time.dt


    # Проверка выстрела и задержки
    if game_state == 'dialog':

        if score_manager.score == 0:
            if len(enemies) == 0:
                camera.enabled = False
                enemies = [Enemy(speed=0, score_manager=score_manager, on_death_callback=remove_enemy, player=subject,
                                shootables_parent=shootables_parent, lst_enemies=enemies,x=60,z=60)]

            distance = ((subject.x - enemies[0].x)**2 + (subject.z - enemies[0].z)**2)**0.5
            if distance < 5 and len(dialogs) == 0:  # Если игрок достаточно близко
                dialogs = [Dialog(character=enemies[0], player=subject, dialog_dict={'1':'Тесак: Паша, ты #$*%!','2':'Паша: Нет, я #$%@^$!','3':'Тесак: #$#%%# мой @#%$ #@$%^', '4':'Паша: Я готов'})]
            
            if len(dialogs) > 0:
                if dialogs[0].update() == 1:
                    dialogs = []
                    destroy(enemies[0])
                    enemies = []
                    game_state = 'gameplay'

    if game_state == 'gameplay':
        
        if held_keys['left mouse'] and not gun.is_shooting:
            gun.is_shooting = True
            gun.shoot()  # Выстрел

            # Наносим урон
            if mouse.hovered_entity and hasattr(mouse.hovered_entity, 'hp'):
                mouse.hovered_entity.hp -= 34
                mouse.hovered_entity.blink(color.red)

        if len(enemies) == 0 and score_manager.level < 5:
            enemies = [Enemy(score_manager=score_manager, on_death_callback=remove_enemy, player=subject,
                            shootables_parent=shootables_parent, lst_enemies=enemies, x=random.uniform(10, 100),
                            z=random.uniform(10, 100)) for _ in range(4)]
        elif len(boss) == 0 and score_manager.level == 5:
            boss = [Boss(speed=1, score_manager=score_manager, on_death_callback=remove_enemy, player=subject,
                        shootables_parent=shootables_parent, x=random.uniform(10, 100), z=random.uniform(10, 100)) for
                    _ in
                    range(1)]

        if score_manager.score > 1000:
            Boss(speed=1, score_manager=score_manager, on_death_callback=remove_enemy, player=subject,
                shootables_parent=shootables_parent, x=random.uniform(10, 100), z=random.uniform(10, 100))


# Принятие входяящих клавиш с клавиатуры
pause_handler = Entity(ignore_paused=True, input=pause_input)

terrain.genTerrain()

app.run()
