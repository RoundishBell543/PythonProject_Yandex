import pygame
import sys
import os


class Entity(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.speed_x = 0
        self.speed_y = 0
        self.speed = 5
        self.is_out = False
        self.is_dead = False
        self.jump_speed = -10
        self.gravity = 0.5
        self.is_grounded = False

    def handle_input(self):
        pass

    def kill(self, image):
        self.image = image
        self.is_dead = True
        self.speed_x = -self.speed_x
        self.speed_y = self.jump_speed

    def update(self):
        self.rect.x += self.speed_x
        self.speed_y += self.gravity
        self.rect.y += self.speed_y
        if self.is_dead:
            if self.rect.top > 470:
                self.is_out = True
        else:
            self.handle_input()

            if self.rect.bottom > 470:
                self.is_grounded = True
                self.speed_y = 0
                self.rect.bottom = 470
                # Проверка на выход за левую и правую границы экрана
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > 800:
                self.rect.right = 800


class Mario(Entity):
    def __init__(self, image):
        super().__init__(image)

    def handle_input(self):
        self.speed_x = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.speed_x += self.speed  # Движение вправо
        elif keys[pygame.K_a]:
            self.speed_x = -self.speed  # Движение влево

        if self.is_grounded and keys[pygame.K_SPACE]:
            self.jump()
    def jump(self):
        self.is_grounded = False
        self.speed_y = self.jump_speed
    def respawn(self):
        self.is_out = False
        self.is_dead = False
        self.rect.midbottom = (400, 530)




def load_image(name, colorkey=None):
    fullname = os.path.join('C:\\Users\\lexfe\\PycharmProjects\\pythonProject_Yandex\\images', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def draw_button(screen):
    color_button = pygame.Color(255, 255, 255)
    color_text = pygame.Color(0, 0, 0)
    pygame.draw.rect(screen, color_button, (650, 250, 100, 75), 0)
    font = pygame.font.Font(None, 36)
    text = font.render("Start", True, color_text)
    text_rect = text.get_rect(center=(700, 287))
    screen.blit(text, text_rect)


def draw_second_screen(screen, all_sprites):  # Экран самой игры
    # Отрисовка фона
    pygame.display.set_caption("GAME: MARIO RUN")
    back = load_image("ground.jpg")
    background_game = pygame.transform.scale(back, size)
    screen.blit(background_game, (0, 0))

    # Отрисовка спрайтов
    all_sprites.update()
    all_sprites.draw(screen)


if __name__ == '__main__':
    pygame.init()
    # Атрибуты для начального окна
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Start of game: Mario RUN")
    icon = load_image("start.jpeg")
    pygame.display.set_icon(icon)
    background = pygame.transform.scale(icon, size)
    FPS = 60
    clock = pygame.time.Clock()

    # Группа спрайтов для персонажа
    all_sprites = pygame.sprite.Group()

    # Создание спрайта персонажа
    mario_image = load_image("caracter_stand.png", -1)
    mario = Mario(mario_image)  # Используем класс Mario
    mario.rect.x = 5
    mario.rect.y = 470 - mario.rect.height  # Помещаем Марио на землю
    all_sprites.add(mario)

    current_screen = "main"
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if current_screen == "main":
                    mouse_pos = pygame.mouse.get_pos()
                    if 650 <= mouse_pos[0] <= 750 and 250 <= mouse_pos[1] <= 325:
                        current_screen = "second"

        if current_screen == "main":
            screen.blit(background, (0, 0))
            draw_button(screen)
        elif current_screen == "second":
            draw_second_screen(screen, all_sprites)

        pygame.display.flip()
        clock.tick(FPS)  # Ограничение FPS

    pygame.quit()
    sys.exit()