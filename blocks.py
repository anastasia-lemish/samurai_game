from pygame import *
import os
import pyganim
import pygame

# Основные константы
PLATFORM_WIDTH = 40
PLATFORM_HEIGHT = 40
PLATFORM_COLOR = (0, 0, 0)
ICON_DIR = os.path.dirname(__file__)  # Полный путь к каталогу с файлами

# Загрузим анимацию, сгенерировав списки из кадров
ANIMATION_BLOCKTELEPORT = [('{}/blocks/portal{}.png'.format(ICON_DIR, i)) for i in range(1, 6)]
ANIMATION_PRINCESS = [
    ('%s/blocks/princess1.png' % ICON_DIR),
    ('%s/blocks/princess2.png' % ICON_DIR)]
ANIMATION_LAVA = [('{}/blocks/lava{}.png'.format(ICON_DIR, i)) for i in range(2, 6)]


class Platform(sprite.Sprite):
    """Основной класс для всех поверхностей,
    по которым персонаж будет ходить"""

    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(PLATFORM_COLOR)
        self.image = image.load("%s/blocks/platform.png" % ICON_DIR)
        self.image.set_colorkey(PLATFORM_COLOR)
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


class Ground(sprite.Sprite):
    """Класс для всех поверхностей"""

    def __init__(self, x, y, imagename):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(PLATFORM_COLOR)
        self.image = image.load(imagename % ICON_DIR)
        self.image.set_colorkey(PLATFORM_COLOR)
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


class BgDecoration(Platform):
    """На основе этого класса мы будем создавать
        фоновые декорации"""

    def __init__(self, x, y, imagename, width, height):
        sprite.Sprite.__init__(self)
        self.image = Surface((width, height))
        self.image.fill(PLATFORM_COLOR)
        self.image = image.load(imagename % ICON_DIR)
        self.image.set_colorkey(PLATFORM_COLOR)
        self.rect = Rect(x, y, width, height)


class ThornBlock(Platform):
    """Клас блоков-колючек"""

    def __init__(self, x, y, imagename):
        Platform.__init__(self, x, y)
        self.image = image.load(imagename % ICON_DIR)


class TeleportBlock(Platform):
    """Класс для создания анимированного телепорта.
        При соприкосновении с персонажем перемещает его на указанные координаты"""

    def __init__(self, x, y, goX, goY):
        Platform.__init__(self, x, y)
        self.goX = goX  # координаты назначения перемещения
        self.goY = goY  # координаты назначения перемещения
        animation_shots = []
        for anim in ANIMATION_BLOCKTELEPORT:
            animation_shots.append((anim, 0.3))
        self.animation_shots = pyganim.PygAnimation(animation_shots)
        self.animation_shots.play()

    def update(self):
        """Обновляет изображение"""
        self.image = Surface((67, 80))
        self.image.set_colorkey((0, 0, 0))
        self.animation_shots.blit(self.image, (0, 0))


class Princess(Platform):
    """Класс для создания экземпляра анимированной принцессы."""

    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        animation_shots = []
        for anim in ANIMATION_PRINCESS:
            animation_shots.append((anim, 0.3))
        self.animation_shots = pyganim.PygAnimation(animation_shots)
        self.animation_shots.play()

    def update(self):
        """Обновляет изображение"""
        self.image = Surface((35, 80))
        self.image.set_colorkey((0, 0, 0))
        self.animation_shots.blit(self.image, (0, 0))


class Lava(Platform):
    """Класс для создания экземпляра анимированной лавы"""

    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        animation_shots = []
        for anim in ANIMATION_LAVA:
            animation_shots.append((anim, 0.8))
        self.animation_shots = pyganim.PygAnimation(animation_shots)
        self.animation_shots.play()

    def update(self):
        """Обновляет изображение"""
        self.image.fill(PLATFORM_COLOR)
        self.animation_shots.blit(self.image, (0, 0))


class LevelName(sprite.Sprite):
    """Класс, генерирующий называние уровня"""

    def __init__(self, x, y, text_level):
        sprite.Sprite.__init__(self)
        name = 'Уровень {}'.format(text_level)
        self.fontObj = pygame.font.Font('font.ttf', 45)
        self.image = self.fontObj.render(name, True, (255, 255, 255), (0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect = Rect(x, y, 1, 1)
