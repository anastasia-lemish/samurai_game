import pygame
import pygame_menu
from main_file import startGame


def startMenu():
    """Инициализирует окно программы, создает виджет меню"""
    pygame.init()
    menu = pygame_menu.Menu(530, 790, 'Меню',
                            theme=mytheme)
    pygame.display.set_caption("Игра про Самурая")

    menu.add_button('Новая игра', start_new_game)
    menu.add_button('Продолжить', startGame)
    menu.add_button('Выйти', pygame_menu.events.EXIT)
    pygame.mixer.music.load('soundtrack.mp3')  # загружаем саундтрек
    pygame.mixer.music.play(-1)  # зацикливает проигрывание музыки
    menu.mainloop(surface)


def start_new_game():
    with open('settings.txt', 'w') as file:
        file.writelines('1')
    startGame()


surface = pygame.display.set_mode((940, 540))
mytheme = pygame_menu.themes.Theme(background_color=(0, 0, 0, 0),
                                   title_font='font.ttf',
                                   title_font_color=(0, 0, 0),
                                   title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_UNDERLINE_TITLE,
                                   widget_font_color=(255, 0, 0),
                                   widget_font_size=40,
                                   widget_font='font.ttf',
                                   widget_offset=(220, 150))

mytheme.title_background_color = (0, 0, 0)
myimage = pygame_menu.baseimage.BaseImage(
    image_path='bg.jpg',
    drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL)
mytheme.background_color = myimage

if __name__ == "__main__":
    startMenu()
