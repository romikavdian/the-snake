from random import randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
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

# Скорость движения змейки:
SPEED = 7

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
        position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
        body_color=None
    ):
        self.position = position
        self.body_color = body_color

    def draw(self, position=None):
        """Отрисовывает игровой объект."""
        if position is None:
            position = self.position
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def clear(self, position):
        """Очищает ячейку игрового объекта."""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect)


class Apple(GameObject):
    """Класс яблока."""

    def __init__(self, body_color=APPLE_COLOR):
        super().__init__(body_color=body_color)
        self.randomize_position()

    def randomize_position(self):
        """Задаёт яблоку случайную позицию на игровом поле."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )


class Snake(GameObject):
    """Класс змейки."""

    def __init__(self, body_color=SNAKE_COLOR):
        super().__init__(body_color=body_color)
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.length = 1
        self.last = None

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Перемещает змейку на одну клетку."""
        head_x, head_y = self.get_head_position()
        direction_x, direction_y = self.direction
        new_x = (head_x + direction_x * GRID_SIZE) % SCREEN_WIDTH
        new_y = (head_y + direction_y * GRID_SIZE) % SCREEN_HEIGHT
        new_head = (new_x, new_y)
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def reset(self):
        """Сбрасывает змейку к начальному состоянию."""
        for position in self.positions:
            self.clear(position)

        if self.last:
            self.clear(self.last)

        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def draw(self):
        """Отрисовывает змейку на игровом поле."""
        super().draw(self.positions[0])
        if self.last:
            self.clear(self.last)


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш управления змейкой."""
    global SPEED

    key_to_direction = {
        pygame.K_UP: UP,
        pygame.K_DOWN: DOWN,
        pygame.K_LEFT: LEFT,
        pygame.K_RIGHT: RIGHT,
    }

    opposite_direction = {
        UP: DOWN,
        DOWN: UP,
        LEFT: RIGHT,
        RIGHT: LEFT,
    }

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

        if event.type != pygame.KEYDOWN:
            continue

        if event.key == pygame.K_ESCAPE:
            pygame.quit()
            raise SystemExit

        if event.key in (pygame.K_EQUALS, pygame.K_KP_PLUS):
            SPEED = min(SPEED + 1, 30)

        elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
            SPEED = max(SPEED - 1, 1)

        else:
            new_direction = key_to_direction.get(event.key)

            if (
                new_direction is not None
                and new_direction != opposite_direction[game_object.direction]
            ):
                game_object.next_direction = new_direction


def main():
    """Запускает основной игровой цикл."""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake()  # центр и цвет уже заданы в классе
    apple = Apple()  # цвет задан, позиция выбирается случайно

    while True:
        # Тут опишите основную логику игры.
        handle_keys(snake)          # смотрим, какую клавишу нажал игрок
        snake.update_direction()   # применяем новое направление
        snake.move()               # двигаем змейку на одну клетку
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()

        snake.draw()  # рисуем змейку
        apple.draw()  # рисуем яблоко
        pygame.display.set_caption(
            f'Змейка | ESC — выход | Скорость: {SPEED} | + / - изменить'
        )
        pygame.display.update()  # показать на экране то, что мы нарисовали
        clock.tick(SPEED)   # ограничить скорость игрового цикла


if __name__ == '__main__':
    main()
