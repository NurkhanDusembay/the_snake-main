# -------------------
import pygame
from random import choice, randint

# Константы для размеров поля и сетки
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки
SPEED = 20

# Инициализация Pygame и Pygame.mixer
pygame.init()
if not pygame.mixer.get_init():
    pygame.mixer.quit()

# Глобальные переменные для экрана и часов
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
clock = pygame.time.Clock()

# -------------------
# Базовый класс


class GameObject:
    """Инициализация базовых атрибутов объекта."""

    def __init__(self, position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
                 body_color=None):
        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        """Отрисовка объекта на экране."""
        pass

    def draw_cell(self, surface, position, color):
        """Отрисовка ячейки на экране."""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

# -------------------


class Apple(GameObject):
    """Инициализация яблока с заданным цветом и случайной позицией."""

    def __init__(self, color=APPLE_COLOR):
        super().__init__(body_color=color)
        self.randomize_position([])

    def randomize_position(self, occupied_positions):
        """Устанавливает случайное положение яблока на игровом поле."""
        while True:
            self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                             randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if self.position not in occupied_positions:
                break

    def draw(self, surface):
        """Отрисовка яблока на экране."""
        self.draw_cell(surface, self.position, self.body_color)

# -------------------
# Класс Snake


class Snake(GameObject):
    """Инициализация начального состояния змейки."""

    def __init__(self):
        super().__init__(body_color=SNAKE_COLOR)
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = RIGHT
        self.next_direction = None
        self.length = 2
        self.last = None

    def update_direction(self):
        """Обновление направления движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновление движения змейки."""
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction
        new_position = (((head_x + (dir_x * GRID_SIZE)) % SCREEN_WIDTH),
                        (head_y + (dir_y * GRID_SIZE)) % SCREEN_HEIGHT)

        # Столкновение
        if new_position in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new_position)
            if len(self.positions) > self.length:
                self.last = self.positions.pop()

    def draw(self, surface):
        """Отрисовка змейки на экране."""
        for position in self.positions[:-1]:
            self.draw_cell(surface, position, self.body_color)

        head_position = self.positions[0]
        self.draw_cell(surface, head_position, self.body_color)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние после столкновения."""
        self.length = 2
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])

# -------------------


# Функция обработки нажатий клавиш
def handle_keys(snake):
    """Обрабатывает нажатия клавиш для управления змейкой."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT

# -------------------


# Основной игровой цикл
def main():
    """Основная функция игры."""
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        screen.fill(BOARD_BACKGROUND_COLOR)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()


if __name__ == '__main__':
    main()
