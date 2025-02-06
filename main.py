import pygame
import sys
import os
import random

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
        self.jump_speed = -15
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
        self.rect.y += self.speed_y
        self.speed_y += self.gravity
        if self.is_dead:
            if self.rect.top > 600:  # Если враг упал за пределы экрана
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


class Enemy(Entity):
    def __init__(self, enemy_image):
        super().__init__(enemy_image)
        self.is_dead = False

    def spawn(self):
        direction = random.randint(0, 1)
        if direction == 0:
            self.speed_x = self.speed
            self.rect.bottomright = (0, 470)
        else:
            self.speed_x = -self.speed
            self.rect.bottomleft = (800, 470)

    def die(self):
        self.is_dead = True
        self.speed_x = 0  # Остановить горизонтальное движение
        self.speed_y = 10  # Ускоренно падать вниз
        self.gravity = 0.5  # Применить гравитацию

    def update(self):
        if self.is_dead:
            self.speed_y += self.gravity  # Ускорять падение вниз
            self.rect.y += self.speed_y
            if self.rect.top > 600:  # Если враг упал за пределы экрана
                self.is_out = True
        else:
            self.rect.x += self.speed_x
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

def save_score(score):
    with open("scores.txt", "a") as f:
        f.write(str(score) + "\n")

def game_over_screen(screen, score):
    save_score(score)
    screen.fill("white")
    font = pygame.font.Font(None, 50)
    text = font.render(f"Игра окончена! Ваш счет: {score}", True, "black")
    screen.blit(text, (800 // 2 - 200, 600 // 2))
    pygame.display.flip()

    pygame.time.delay(3000)

def draw_button(screen):
    color_button = pygame.Color(255, 255, 255)
    color_text = pygame.Color(0, 0, 0)
    pygame.draw.rect(screen, color_button, (650, 250, 100, 75), 0)
    font = pygame.font.Font(None, 36)
    text = font.render("Start", True, color_text)
    text_rect = text.get_rect(center=(700, 287))
    screen.blit(text, text_rect)


def draw_button_back(screen):
    color_button = pygame.Color(255, 255, 255)
    color_text = pygame.Color(0, 0, 0)
    pygame.draw.rect(screen, color_button, (50, 50, 100, 50), 0)  # Кнопка "Back" в верхнем левом углу
    font = pygame.font.Font(None, 36)
    text = font.render("Back", True, color_text)
    text_rect = text.get_rect(center=(100, 75))  # Центрируем текст на кнопке
    screen.blit(text, text_rect)


def draw_second_screen(screen, all_sprites, score, killed_enemies):  # Экран самой игры
    # Отрисовка фона
    pygame.display.set_caption("GAME: MARIO RUN")
    back = load_image("ground.jpg")
    background_game = pygame.transform.scale(back, size)
    screen.blit(background_game, (0, 0))

    # Отрисовка кнопки "Back"
    draw_button_back(screen)

    # Отрисовка счетчика
    font = pygame.font.Font(None, 48)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))  # Белый текст
    score_rect = score_text.get_rect(center=(width // 2, 30))  # По центру вверху
    screen.blit(score_text, score_rect)

    # Отрисовка счетчика убитых врагов
    killed_text = font.render(f"Killed: {killed_enemies}", True, (255, 255, 255))  # Белый текст
    killed_rect = killed_text.get_rect(center=(width // 2, 70))  # По центру вверху, ниже основного счетчика
    screen.blit(killed_text, killed_rect)

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

    # создание спрайта врага
    enemy_image = load_image("enemy.jpg", -1)
    enemy_list = []
    delay_for_start = 2500
    spawn_enemy = 2000
    last_spawn_time = pygame.time.get_ticks()

    current_screen = "main"
    running = True
    score = 0  # Счетчик
    killed_enemies = 0  # Счетчик убитых врагов

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if current_screen == "main":
                    mouse_pos = pygame.mouse.get_pos()
                    if 650 <= mouse_pos[0] <= 750 and 250 <= mouse_pos[1] <= 325:
                        current_screen = "second"
                        mario.rect.x = 5
                        mario.rect.y = 470 - mario.rect.height
                        score = 0
                        killed_enemies = 0  # Сбрасываем счетчик убитых врагов
                elif current_screen == "second":
                    mouse_pos = pygame.mouse.get_pos()
                    if 50 <= mouse_pos[0] <= 150 and 50 <= mouse_pos[1] <= 100:  # Проверка нажатия на кнопку "Back"
                        current_screen = "main"

        if current_screen == "main":
            screen.blit(background, (0, 0))
            draw_button(screen)
        elif current_screen == "second":
            if score < 100:  # Увеличиваем лимит счета для тестирования
                draw_second_screen(screen, all_sprites, score, killed_enemies)
                now = pygame.time.get_ticks()
                elapsed = now - last_spawn_time
                if elapsed > spawn_enemy:
                    last_spawn_time = now
                    new_enemy = Enemy(enemy_image)
                    new_enemy.spawn()
                    enemy_list.append(new_enemy)
                    all_sprites.add(new_enemy)

                for enemy in list(enemy_list):
                    if enemy.is_out:
                        enemy_list.remove(enemy)
                        all_sprites.remove(enemy)
                    else:
                        enemy.update()

                # Проверка столкновений
                for enemy in list(enemy_list):
                    if pygame.sprite.collide_rect(mario, enemy):
                        if mario.rect.bottom <= enemy.rect.top + 10:  # Mario прыгает сверху
                            mario.speed_y = mario.jump_speed  # Mario подпрыгивает от врага
                            enemy.die()  # Враг начинает падать вниз
                            killed_enemies += 1
                        else:
                            mario.kill(mario_image)  # Mario умирает при столкновении сбоку
                            break


            else:
                game_over_screen(screen, score)
                current_screen = "main"

        pygame.display.flip()
        clock.tick(FPS)  # Ограничение FPS

    pygame.quit()
    sys.exit()