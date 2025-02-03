import pygame
import sys

# Функция для отрисовки кнопки
def draw_button(screen):
    color_button = pygame.Color(255, 255, 255)  # Белый цвет
    color_text = pygame.Color(0, 0, 0)  # Черный цвет

    # Рисуем прямоугольник (кнопку)
    pygame.draw.rect(screen, color_button, (650, 250, 100, 75), 0)

    # Добавляем текст на кнопку
    font = pygame.font.Font(None, 36)
    text = font.render("Start", True, color_text)
    text_rect = text.get_rect(center=(700, 287))
    screen.blit(text, text_rect)

# Функция для отрисовки второго окна
def draw_second_screen(screen):
    screen.fill("#60B9CE")


if __name__ == '__main__':
    pygame.init()
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Start of game: Mario RUN")
    icon = pygame.image.load("images\\start.jpeg")
    pygame.display.set_icon(icon)
    background = pygame.transform.scale(pygame.image.load("images\\start.jpeg"), size)

    # Основной игровой цикл
    current_screen = "main"  # Текущий экран: "main" или "second"
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Если нажата кнопка мыши
                if current_screen == "main":
                    # Проверяем, была ли нажата кнопка
                    mouse_pos = pygame.mouse.get_pos()
                    if 650 <= mouse_pos[0] <= 750 and 250 <= mouse_pos[1] <= 325:
                        current_screen = "second"  # Переключаемся на второй экран

        # Отрисовка текущего экрана
        if current_screen == "main":
            screen.blit(background, (0, 0))
            draw_button(screen)
        elif current_screen == "second":
            draw_second_screen(screen)

        # Обновление экрана
        pygame.display.flip()

    pygame.quit()
    sys.exit()