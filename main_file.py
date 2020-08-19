import pygame
import sys
from player import *
from blocks import *
from monsters import *

# Основные константы:
WIN_WIDTH = 800  # Ширина создаваемого окна
WIN_HEIGHT = 540  # Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
FILE_DIR = os.path.dirname(__file__)
GAME_NAME = "Игра про Самурая"
level = []
monsters = pygame.sprite.Group()  # Все передвигающиеся объекты
platforms = []  # то, во что мы будем врезаться или опираться
backgrounds_img = pygame.sprite.Group()


class Camera(object):
    """Изменяет отображаемую область игрового поля
        в соответствии с положением игрока"""

    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    """Вычисляет игровую область, которую необходимо отобразить """
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + WIN_WIDTH / 2, -t + WIN_HEIGHT / 2

    l = min(0, l)  # Не движемся дальше левой границы
    l = max(-(camera.width - WIN_WIDTH), l)  # Не движемся дальше правой границы
    t = max(-(camera.height - WIN_HEIGHT), t)  # Не движемся дальше нижней границы
    t = min(0, t)  # Не движемся дальше верхней границы

    return Rect(l, t, w, h)


def loadLevel(current_level):
    """Загружает уровень из текстового файла."""
    file_name = '%s/levels/{}.txt'.format(current_level)
    levelFile = open(file_name % FILE_DIR)
    global playerX, playerY  # объявляем глобальные переменные, это координаты героя

    line = " "
    commands = []
    while line[0] != "!":  # пока не нашли символ завершения файла
        line = levelFile.readline()  # считываем построчно
        if line[0] == "[":  # если нашли символ начала уровня
            while line[0] != "]":  # то, пока не нашли символ конца уровня
                line = levelFile.readline()  # считываем построчно уровень
                if line[0] != "]":  # и если нет символа конца уровня
                    endLine = line.find("|")  # то ищем символ конца строки
                    level.append(line[0: endLine])  # и добавляем в уровень строку от начала до символа "|"

        if line[0] != "":  # если строка не пустая
            commands = line.split()  # разбиваем ее на отдельные команды
            if len(commands) > 1:  # если количество команд > 1, то ищем эти команды
                if commands[0] == "player":  # если первая команда - player
                    playerX = int(commands[1])  # то записываем координаты героя
                    playerY = int(commands[2])
                if commands[0] == "portal":  # если первая команда portal, то создаем портал
                    tp = TeleportBlock(int(commands[1]), int(commands[2]), int(commands[3]), int(commands[4]))
                    characters.add(tp)
                    platforms.append(tp)
                    animatedCharacters.add(tp)

                if commands[0] == "monster":  # если первая команда monster, то создаем монстра
                    mn = Monster(int(commands[1]), int(commands[2]), int(commands[3]), int(commands[4]),
                                 int(commands[5]), int(commands[6]))
                    characters.add(mn)
                    platforms.append(mn)
                    monsters.add(mn)

                if commands[0] == "background":
                    f = BgDecoration(0, 0, "%s/blocks/{}.png".format(commands[1]), 0, 0)
                    backgrounds_img.add(f)


def startGame():
    """ Игровой цикл.
        Загружает текущий уровень, инициализирует окно игры,
        отслеживает события, обновляет положение всех спрайтов.
    """
    pygame.mixer.music.stop()  # Выключаем саундтрек окна меню
    current_level = what_lvl()  # Возвращаем текущий уровень
    loadLevel(current_level)  # Загружаем текущий уровень

    screen = pygame.display.set_mode(DISPLAY)  # Создаем окно
    pygame.display.set_caption(GAME_NAME)  # Пишем в шапку
    bg = Surface((WIN_WIDTH, WIN_HEIGHT))  # Создание видимой поверхности
    bg.fill((0, 0, 0))  # Заливаем поверхность сплошным цветом
    hit = False
    left = right = up = running = False  # По умолчанию персонаж стоит на месте
    x = y = 0  # Координаты объектов по умолчанию

    for row in level:  # вся строка
        for col in row:  # каждый символ
            if col == "-":
                pf = Platform(x, y)  # Экземпляр поверхности
                characters.add(pf)
                platforms.append(pf)

            if col == "*":
                bd = ThornBlock(x, y, "%s/blocks/dieBlock.png")  # Экземпляр колючки
                characters.add(bd)
                platforms.append(bd)
            if col == "P":
                pr = Princess(x, y)  # Экземпляр принцессы
                characters.add(pr)
                platforms.append(pr)
                animatedCharacters.add(pr)

            if col == "+":
                pf = Ground(x, y, "%s/blocks/ground.png")  # Экземпляр поверхности
                characters.add(pf)
                platforms.append(pf)

            if col == "1":
                pf2 = Ground(x, y, "%s/blocks/ground2.png")  # Экземпляр поверхности
                characters.add(pf2)
                platforms.append(pf2)

            if col == "J":
                la = BgDecoration(x, y, "%s/blocks/jp_house.png", 114, 93)  # Экземпляр здания-декорации
                characters.add(la)

            if col == "C":
                cloud = BgDecoration(x, y, "%s/blocks/cloud.png", 200, 20)  # Экземпляр облака-платформы
                characters.add(cloud)
                platforms.append(cloud)

            if col == "c":
                cloud2 = BgDecoration(x, y, "%s/blocks/cloud.png", 200, 20)  # Экземпляр облака-декорации
                characters.add(cloud2)

            if col == 'N':
                lvl = LevelName(x, y, str(current_level))  # Экземпляр названия уровня
                characters.add(lvl)
            if col == '3':
                dg = ThornBlock(x, y, "%s/blocks/die.png")  # Экземпляр блока-колючки
                characters.add(dg)
                platforms.append(dg)
            if col == '4':
                dg2 = ThornBlock(x, y, "%s/blocks/die2.png")  # Экземпляр блока-колючки
                characters.add(dg2)
                platforms.append(dg2)
            if col == ",":
                lava = Lava(x, y)  # Экземпляр поверхности-лавы
                characters.add(lava)
                platforms.append(lava)
                animatedCharacters.add(lava)
            x += PLATFORM_WIDTH  # Блоки платформы ставятся на ширине блоков
        y += PLATFORM_HEIGHT
        x = 0  # На каждой новой строчке начинаем с нуля

    hero = Player(playerX, playerY)  # Создаем героя по (x,y) координатам
    characters.add(hero)  # Добавляем героя в список спрайтов

    # Инициализируем расположение камеры
    total_level_width = len(level[0]) * PLATFORM_WIDTH  # Высчитываем фактическую ширину уровня
    total_level_height = len(level) * PLATFORM_HEIGHT  # высоту
    camera = Camera(camera_configure, total_level_width, total_level_height)

    # Основной цикл программы:
    while not hero.winner:
        # Пропишем обработчик событий
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()
            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True
            if e.type == KEYDOWN and e.key == K_LSHIFT:
                running = True
            if e.type == KEYDOWN and e.key == K_SPACE:
                hit = True

            if e.type == KEYUP and e.key == K_UP:
                up = False
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False
            if e.type == KEYUP and e.key == K_LSHIFT:
                running = False
            if e.type == KEYUP and e.key == K_ESCAPE:
                sys.exit()
            if e.type == KEYUP and e.key == K_SPACE:
                hit = False
        # если игрок соприкоснется с монстром, то спрайт монстра бужет удален:
        for monster in monsters:
            place = monster.rect.x
            if hero.rect.bottom == monster.rect.top and (place - 20 <= hero.rect.x <= place + 20):
                monster.kill()
                monsters.update(platforms)
                platforms.remove(monster)

        # Обновление положения всех игровых спрайтов и перерисовка экрана:
        screen.blit(bg, (0, 0))  # Прорисовка экрана
        animatedCharacters.update()  # Прорисовка анимации
        monsters.update(platforms)  # Обновление расположения монстра
        camera.update(hero)  # Обновление положения камеры
        hero.update(left, right, up, running, platforms, hit)  # Перемещение главного персонажа
        for f in backgrounds_img:
            screen.blit(f.image, camera.apply(f))  # Перерисовка фонового изображения
        for e in characters:
            screen.blit(e.image, camera.apply(e))  # Перерисовка всех персонажей
        pygame.display.update()  # Обновление и вывод всех изменений на экран

    if hero.winner:
        # Очищаем списки всех спрайтов перед переходом на новый уровень:
        characters.empty()
        animatedCharacters.empty()
        monsters.empty()
        level.clear()
        platforms.clear()
        backgrounds_img.empty()
        hero.winner = False
        # Перезапуск игрового цикла:
        startGame()
