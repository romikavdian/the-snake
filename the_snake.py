from random import randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

OPPOSITE_DIRECTIONS = {
    UP: DOWN,
    DOWN: UP,
    LEFT: RIGHT,
    RIGHT: LEFT,
}

KEY_TO_DIRECTION = {
    pygame.K_UP: UP,
    pygame.K_DOWN: DOWN,
    pygame.K_LEFT: LEFT,
    pygame.K_RIGHT: RIGHT,
}

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 7
MIN_SPEED = 1
MAX_SPEED = 30
SPEED_STEP = 1
current_speed = SPEED

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.

class GameObject:
    """Базовый класс игровых объектов."""

    def __init__(
        self,
        position=CENTER,
        body_color=None
    ):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Отрисовывает игровой объект."""
        raise NotImplementedError(
            f'Метод draw() не реализован в классе {self.__class__.__name__}'
        )

    def draw_cell(self, position, color=None):
        """Рисует одну ячейку."""
        if color is None:
            color = self.body_color

        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, color, rect)
        if color != BOARD_BACKGROUND_COLOR:
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс яблока."""

    def __init__(self, body_color=APPLE_COLOR, occupied_cells=()):
        super().__init__(body_color=body_color)
        self.randomize_position(occupied_cells)

    def randomize_position(self, occupied_cells):
        """Задаёт яблоку случайную позицию на игровом поле."""
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )

            if self.position not in occupied_cells:
                break

    def draw(self):
        """Отрисовывает яблоко на игровом поле."""
        self.draw_cell(self.position)


class Snake(GameObject):
    """Класс змейки."""

    def __init__(self, body_color=SNAKE_COLOR):
        super().__init__(body_color=body_color)
        self.reset()

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def update_direction(self, new_direction):
        """Обновляет направление движения змейки."""
        if new_direction != OPPOSITE_DIRECTIONS[self.direction]:
            self.direction = new_direction

    def move(self):
        """Перемещает змейку на одну клетку."""
        head_x, head_y = self.get_head_position()
        direction_x, direction_y = self.direction
        new_x = (head_x + direction_x * GRID_SIZE) % SCREEN_WIDTH
        new_y = (head_y + direction_y * GRID_SIZE) % SCREEN_HEIGHT
        new_head = (new_x, new_y)
        self.positions.insert(0, new_head)
        self.last = None

        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def reset(self):
        """Сбрасывает змейку к начальному состоянию."""
        self.length = 1
        self.positions = [CENTER]
        self.direction = RIGHT
        self.last = None

    def draw(self):
        """Отрисовывает змейку на игровом поле."""
        self.draw_cell(self.get_head_position())
        if self.last:
            self.draw_cell(self.last, BOARD_BACKGROUND_COLOR)


def handle_keys(snake):
    """Обрабатывает нажатия клавиш управления змейкой."""
    global current_speed

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN
            and event.key == pygame.K_ESCAPE
        ):
            pygame.quit()
            raise SystemExit

        if event.type != pygame.KEYDOWN:
            continue

        if event.key in (pygame.K_EQUALS, pygame.K_KP_PLUS):
            current_speed = min(current_speed + SPEED_STEP, MAX_SPEED)

        elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
            current_speed = max(current_speed - SPEED_STEP, MIN_SPEED)

        else:
            new_direction = KEY_TO_DIRECTION.get(event.key)

            if new_direction is not None:
                snake.update_direction(new_direction)


def main():
    """Запускает основной игровой цикл."""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake()  # центр и цвет уже заданы в классе
    apple = Apple(occupied_cells=snake.positions)

    while True:
        handle_keys(snake)  # смотрим, какую клавишу нажал игрок
        snake.move()  # двигаем змейку на одну клетку
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        elif snake.get_head_position() in snake.positions[4:]:
            snake.reset()
            apple.randomize_position(snake.positions)

        snake.draw()
        apple.draw()
        pygame.display.set_caption(
            f'Змейка | ESC — выход | Скорость: {SPEED} | + / - изменить'
        )
        pygame.display.update()  # показать на экране то, что мы нарисовали
        clock.tick(current_speed)   # ограничить скорость игрового цикла


if __name__ == '__main__':
    main()
