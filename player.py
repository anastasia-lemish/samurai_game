from pygame import *
import pyganim
import os
import blocks
import monsters
from main_file import *
from pygame.sprite import Sprite

# Основные константы:
MOVE_SPEED = 7
MOVE_EXTRA_SPEED = 3  # ускорение
WIDTH = 57
HEIGHT = 80
COLOR = (136, 136, 136)
JUMP_POWER = 10
JUMP_EXTRA_POWER = 3  # дополнительная сила прыжка
GRAVITY = 0.35  # Гравитация
ANIMATION_DELAY = 0.1
ANIMATION_SUPER_SPEED_DELAY = 0.05  # скорость смены кадров при ускорении
ICON_DIR = os.path.dirname(__file__)  # Полный путь к каталогу с файлами

# Создание группы спрайтов: персонажи и анимированные персонажи
characters = pygame.sprite.Group()
animatedCharacters = pygame.sprite.Group()

# Сгенерируем списки кадров анимации движения спрайта игрока:
# вправо, влево, прыжок-влево, прыжок-вправо, прыжок, на месте, удар
ANIMATION_RIGHT = [('{}/player/r{}.png'.format(ICON_DIR, i)) for i in range(1, 6)]
ANIMATION_LEFT = [('{}/player/l{}.png'.format(ICON_DIR, i)) for i in range(1, 6)]
ANIMATION_JUMP_LEFT = [('%s/player/jl.png' % ICON_DIR, 0.1)]
ANIMATION_JUMP_RIGHT = [('%s/player/jr.png' % ICON_DIR, 0.1)]
ANIMATION_JUMP = [('%s/player/j.png' % ICON_DIR, 0.1)]
ANIMATION_STAY = [('%s/player/0.png' % ICON_DIR, 0.1)]
ANIMATION_HIT = [('%s/player/j.png' % ICON_DIR, 0.1)]


class Player(Sprite):
    """Создание главного персонажа.
            Запускает анимацию в соответствии с заданным направлением.
    """

    def __init__(self, x, y):
        """Создает спрайт игрока, """
        Sprite.__init__(self)
        self.startX = x
        self.startY = y
        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        self.image = Surface((WIDTH, HEIGHT))
        self.image.fill(COLOR)
        self.rect = Rect(x, y, WIDTH, HEIGHT)
        self.player_bottom = self.rect.bottom
        self.image.set_colorkey(COLOR)

        # по умолчанию игрок еще не победитель
        self.winner = False
        #        Анимация движения вправо
        playerAnim, playerAnimFastSpeed = self.createAnimDirection(ANIMATION_RIGHT)
        self.playerAnimRight = pyganim.PygAnimation(playerAnim)
        self.playerAnimRightSuperSpeed = pyganim.PygAnimation(playerAnimFastSpeed)

        #        Анимация движения влево
        playerAnim, playerAnimFastSpeed = self.createAnimDirection(ANIMATION_LEFT)
        self.playerAnimLeft = pyganim.PygAnimation(playerAnim)
        self.playerAnimLeftSuperSpeed = pyganim.PygAnimation(playerAnimFastSpeed)

        ##Создаем остальные переменные анимации
        self.playerAnimStay = pyganim.PygAnimation(ANIMATION_STAY)
        self.playerAnimStay.blit(self.image, (0, 0))  # По-умолчанию, стоим
        self.playerAnimJumpLeft = pyganim.PygAnimation(ANIMATION_JUMP_LEFT)
        self.playerAnimJumpRight = pyganim.PygAnimation(ANIMATION_JUMP_RIGHT)
        self.playerAnimJump = pyganim.PygAnimation(ANIMATION_JUMP)
        self.playerAnimHit = pyganim.PygAnimation(ANIMATION_HIT)

        # Запустим анимацию

        self.playerAnimRight.play()
        self.playerAnimRightSuperSpeed.play()
        self.playerAnimLeft.play()
        self.playerAnimLeftSuperSpeed.play()
        self.playerAnimStay.play()
        self.playerAnimJumpLeft.play()
        self.playerAnimJumpRight.play()
        self.playerAnimJump.play()
        self.playerAnimHit.play()

    def createAnimDirection(self, direct):
        """Создает список из кортежей кадра анимации и скорости"""
        playerAnim = []
        playerAnimFastSpeed = []
        for anim in direct:
            playerAnim.append((anim, ANIMATION_DELAY))
            playerAnimFastSpeed.append((anim, ANIMATION_SUPER_SPEED_DELAY))
        return playerAnim, playerAnimFastSpeed

    def update(self, left, right, up, running, platforms, hit):
        """Обновляет положение стпрайта игрока и обновляет кадры анимации
            в соответствии с тем, какие клавиши нажаты"""
        if up:
            if self.onGround:
                self.yvel = -JUMP_POWER
                if running and (left or right):
                    self.yvel -= JUMP_EXTRA_POWER
                self.image.fill(COLOR)
                self.playerAnimJump.blit(self.image, (0, 0))

        if left:
            self.xvel = -MOVE_SPEED
            self.image.fill(COLOR)
            if running:
                self.xvel -= MOVE_EXTRA_SPEED
                if not up:
                    self.playerAnimLeftSuperSpeed.blit(self.image, (0, 0))
            else:
                if not up:
                    self.playerAnimLeft.blit(self.image, (0, 0))
            if up:
                self.playerAnimJumpLeft.blit(self.image, (0, 0))

        if right:
            self.xvel = MOVE_SPEED
            self.image.fill(COLOR)
            if running:
                self.xvel += MOVE_EXTRA_SPEED
                if not up:
                    self.playerAnimRightSuperSpeed.blit(self.image, (0, 0))
            else:
                if not up:
                    self.playerAnimRight.blit(self.image, (0, 0))
            if up:
                self.playerAnimJumpRight.blit(self.image, (0, 0))

        if hit:
            self.image.fill(COLOR)
            self.playerAnimHit.blit(self.image, (0, 0))

        if not (left or right or hit):
            self.xvel = 0
            if not up:
                self.image.fill(COLOR)
                self.playerAnimStay.blit(self.image, (0, 0))

        if not self.onGround:
            self.yvel += GRAVITY

        self.onGround = False
        self.rect.y += self.yvel

        self.collide(0, self.yvel, platforms)

        self.rect.x += self.xvel
        self.collide(self.xvel, 0, platforms)

    def collide(self, xvel, yvel, platforms):
        """Обработчик столкновений с другими спрайтами"""
        for platform in platforms:
            if sprite.collide_rect(self, platform):
                if isinstance(platform, blocks.TeleportBlock):  # если спрайт игрока пересекается с телепортом
                    self.teleporting(platform.goX, platform.goY)  # переместить игрока на новые координаты
                elif isinstance(platform, blocks.Princess):  # если коснулись принцессы
                    current_level = what_lvl()
                    current_level = str(current_level + 1)  # переход на следущий уровень
                    if current_level == '11':
                        current_level = '1'
                    with open('settings.txt', 'w') as f:
                        f.writelines(current_level)
                    self.winner = True  # переход на новый уровень

                # В случае столкновения игрока со спрайтом лавы или колючкой,
                # то перемещает игрока на начало уровня:
                elif isinstance(platform, blocks.Lava) or \
                        isinstance(platform, blocks.ThornBlock):
                    self.die()

                # Обработка движения. Движение игрока может происходить только в одну сторону
                else:
                    if xvel > 0:  # если движется вправо
                        self.rect.right = platform.rect.left  # то не движется вправо

                    if xvel < 0:  # если движется влево
                        self.rect.left = platform.rect.right  # то не движется влево

                    if yvel > 0:  # если падает вниз
                        self.rect.bottom = platform.rect.top  # то не падает вниз
                        self.onGround = True  # и становится на что-то твердое
                        self.yvel = 0  # и энергия падения пропадает
                    if yvel < 0:  # если движется вверх
                        self.rect.top = platform.rect.bottom  # то не движется вверх
                        self.yvel = 0  # и энергия прыжка пропадает

    def teleporting(self, goX, goY):
        """Перемещает игрока на указанные координаты"""
        self.rect.x = goX
        self.rect.y = goY

    def die(self):
        """Перемещает игрока на начало уровня"""
        self.teleporting(40, 800)


def what_lvl():
    """Возвращает число текущего уровня, записанное в файле настроек"""
    global current_level
    with open('settings.txt', 'r') as file:
        set = file.readlines()
    for line in set:
        current_level = int(line)
    file.close()
    return current_level
