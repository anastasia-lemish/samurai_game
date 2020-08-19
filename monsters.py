from pygame import *
import pyganim
import os

from pygame.sprite import *

# Основные константы
MONSTER_WIDTH = 49
MONSTER_HEIGHT = 80
MONSTER_COLOR = (0, 0, 0)
ICON_DIR = os.path.dirname(__file__)  # Полный путь к каталогу с файлами

# Сгенерируем список кадров анимации спрайта монстров
ANIMATION_MONSTERHORYSONTAL = [('{}/monsters/{}.png'.format(ICON_DIR, i)) for i in range(1, 11)]


class Monster(sprite.Sprite):
    """Класс для создания экземпляров спрайтов-монстов.
        Обновляет расположение спрайтов. Обрабатывает столкновения с платформами """

    def __init__(self, x, y, left, up, maxLengthLeft, maxLengthUp):
        sprite.Sprite.__init__(self)
        self.image = Surface((MONSTER_WIDTH, MONSTER_HEIGHT))
        self.image.fill(MONSTER_COLOR)
        self.rect = Rect(x, y, MONSTER_WIDTH, MONSTER_HEIGHT)
        self.image.set_colorkey(MONSTER_COLOR)
        self.startX = x  # начальные координаты
        self.startY = y
        self.maxLengthLeft = maxLengthLeft  # максимальное расстояние, которое может пройти в одну сторону
        self.maxLengthUp = maxLengthUp  # максимальное расстояние, которое может пройти в одну сторону, вертикаль
        self.xvel = left  # cкорость передвижения по горизонтали, 0 - стоит на месте
        self.yvel = up  # скорость движения по вертикали, 0 - не двигается
        animation_shots = []
        for anim in ANIMATION_MONSTERHORYSONTAL:
            animation_shots.append((anim, 0.3))
        self.animation_shots = pyganim.PygAnimation(animation_shots)
        self.animation_shots.play()

    def update(self, platforms):
        """Обновляет расположение спрайтов монстров"""
        self.image.fill(MONSTER_COLOR)
        self.animation_shots.blit(self.image, (0, 0))
        self.rect.y += self.yvel
        self.rect.x += self.xvel
        self.collide(platforms)

        if (abs(self.startX - self.rect.x) > self.maxLengthLeft):
            self.xvel = -self.xvel  # если прошли максимальное растояние, то идет в обратную сторону по горизонтали
        if (abs(self.startY - self.rect.y) > self.maxLengthUp):
            self.yvel = -self.yvel  # если прошли максимальное растояние, то идет в обратную сторону по вертикали

    def collide(self, platforms):
        """Обрабатывает столкновения с платформами и персонажем"""
        for p in platforms:
            if sprite.collide_rect(self, p) and self != p:  # если с чем-то или кем-то столкнулись
                self.xvel = - self.xvel  # то поворачиваем в обратную сторону
                self.yvel = - self.yvel
