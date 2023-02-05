import pygame
from random import randint

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

HEIGHT_MAX_TOP = 40
HEIGHT_MAX_BOTTOM = 55
SPEED = 0.5
SPEED_BALL_X = 0.4
SPEED_BALL_Y = 0.5

WIDTH_WINDOW = 900
HEIGHT_WINDOW = 500

POSITION_X_SCORE_RIGHT = 470
POSITION_Y_SCORE_RIGHT = 30

POSITION_X_SCORE_LEFT = 415
POSITION_Y_SCORE_LEFT = 30

window = None
placar_right = placar_left = 0
text_right_pipe = text_left_pipe = font = None


class Player1:
    def __init__(self, top, left, width, height):
        self.pipe = pygame.draw.rect(window,
                                     WHITE,
                                     [left, top, width, height])
        self.top = top
        self.left = left
        self.width = width
        self.height = height

    def move(self):
        if pygame.key.get_pressed()[pygame.K_UP]:
            if (self.top + self.width) >= HEIGHT_MAX_TOP:
                self.top -= SPEED
        elif pygame.key.get_pressed()[pygame.K_DOWN]:
            if (self.top + self.width) <= (HEIGHT_WINDOW - HEIGHT_MAX_BOTTOM):
                self.top += SPEED

    def collision(self, position_x_ball, position_y_ball, side_ball):
        if self.left < position_x_ball + side_ball and \
                self.left + self.width > position_x_ball and \
                self.top < position_y_ball + side_ball and \
                self.top + self.height > position_y_ball:
            return True

    def draw(self):
        pygame.draw.rect(window, WHITE, [self.left, self.top, self.width, self.height])


class Player2:
    def __init__(self, top, left, width, height):
        self.pipe = pygame.draw.rect(window,
                                     WHITE,
                                     [left, top, width, height])
        self.top = top
        self.left = left
        self.width = width
        self.height = height

    def move(self):
        if pygame.key.get_pressed()[pygame.K_w]:
            if (self.top + self.width) >= HEIGHT_MAX_TOP:
                self.top -= SPEED
        elif pygame.key.get_pressed()[pygame.K_s]:
            if (self.top + self.width) <= (HEIGHT_WINDOW - HEIGHT_MAX_BOTTOM):
                self.top += SPEED

    def collision(self, position_x_ball, position_y_ball, side_ball):
        if self.left < position_x_ball + side_ball and \
                self.left + self.width > position_x_ball and \
                self.top < position_y_ball + side_ball and \
                self.top + self.height > position_y_ball:
            return True

    def draw(self):
        pygame.draw.rect(window, WHITE, [self.left, self.top, self.width, self.height])


class Ball:
    def __init__(self, top, left, width, height):
        self.pipe = pygame.draw.rect(window,
                                     WHITE,
                                     [left, top, width, height])
        self.top = top
        self.left = left
        self.width = width
        self.height = height
        self.right_direction = True

        up_or_down = randint(0, 1)
        if up_or_down == 1:
            self.up = True
        else:
            self.up = False

    def reverse_direction_x(self):
        if self.right_direction:
            self.right_direction = False
        else:
            self.right_direction = True

    def reverse_direction_y(self):
        if self.up:
            self.up = False
        else:
            self.up = True

    def check_new_score(self):
        if self.left > WIDTH_WINDOW:
            return 2
        elif self.left < 0:
            return 1

        return 0

    def move(self):
        if self.right_direction:
            self.left += SPEED_BALL_X
        else:
            self.left -= SPEED_BALL_X

        if self.up:
            self.top += SPEED_BALL_Y
        else:
            self.top -= SPEED_BALL_Y

    def draw(self):
        pygame.draw.rect(window, WHITE, [self.left, self.top, self.width, self.height])


def init():
    pygame.init()
    pygame.display.set_caption("Pong")

    global window, text_right_pipe, text_left_pipe, font

    window = pygame.display.set_mode((WIDTH_WINDOW, HEIGHT_WINDOW))
    window.fill(BLACK)

    font = pygame.font.SysFont("Showcard Gothic", 32)


def updateScore():
    global text_right_pipe, text_left_pipe

    text_right_pipe = font.render(fr'{placar_right}', True, WHITE)
    text_left_pipe = font.render(fr'{placar_left}', True, WHITE)

    window.blit(text_right_pipe, (POSITION_X_SCORE_RIGHT, POSITION_Y_SCORE_RIGHT))
    window.blit(text_left_pipe, (POSITION_X_SCORE_LEFT, POSITION_Y_SCORE_LEFT))


def won():
    if placar_right > placar_left:
        winner = font.render("The player on the right won", True, WHITE)
    else:
        winner = font.render("The player on the left won", True, WHITE)

    window.blit(winner, (200, 200))
    pygame.display.update()

    pygame.time.delay(5000)
    exit()


def add_score(num_score: int):
    global placar_right, placar_left

    if num_score == 1:
        placar_right += 1
    elif num_score == 2:
        placar_left += 1

    if placar_right >= 5 or placar_left >= 5:
        won()

    game()


def draw_collision_simple_game_objects(dotted: bool, position_x_ball, position_y_ball, side_ball):
    middle_screen_horizontal = WIDTH_WINDOW * 0.5
    init_line_in_x = init_line_in_y = 0
    init_line_higher_y = 5
    init_line_bottom_y = HEIGHT_WINDOW - 5

    # Desenha linha superior
    pygame.draw.line(window,
                     WHITE,
                     (init_line_in_x, init_line_higher_y),
                     (WIDTH_WINDOW, init_line_higher_y), 20)

    # Desenha linha inferior
    pygame.draw.line(window,
                     WHITE,
                     (init_line_in_x, init_line_bottom_y),
                     (WIDTH_WINDOW, init_line_bottom_y), 20)

    # Desenha o trasejado(dotted) no meio da tela
    for index in range(init_line_in_y, HEIGHT_WINDOW, 15):
        if dotted:
            pygame.draw.line(window,
                             WHITE,
                             (middle_screen_horizontal, index),
                             (middle_screen_horizontal, index + 13),
                             12)
            dotted = False
        else:
            dotted = True

    # Detecta colisao superior
    if init_line_in_x < position_x_ball + side_ball and \
            init_line_in_x + WIDTH_WINDOW > position_x_ball and \
            init_line_higher_y < position_y_ball + side_ball and \
            init_line_higher_y + init_line_higher_y > position_y_ball:
        return True

    # Detecta colisao inferior
    if init_line_in_x < position_x_ball + side_ball and \
            init_line_in_x + WIDTH_WINDOW > position_x_ball and \
            init_line_bottom_y < position_y_ball + side_ball and \
            init_line_bottom_y + init_line_bottom_y > position_y_ball:
        return True


def game():
    init()

    pipe_right_left = WIDTH_WINDOW * 0.96
    pipe_right_top = HEIGHT_WINDOW * 0.5
    pipe_right_width = 15
    pipe_right_height = 50

    pipe_left_left = WIDTH_WINDOW * 0.0242
    pipe_left_top = HEIGHT_WINDOW * 0.5
    pipe_left_width = 15
    pipe_left_height = 50

    side_ball = 15
    center_y_ball = WIDTH_WINDOW * 0.5
    center_x_ball = HEIGHT_WINDOW * 0.5

    pipe_right = Player1(pipe_right_top, pipe_right_left, pipe_right_width, pipe_right_height)
    pipe_left = Player2(pipe_left_top, pipe_left_left, pipe_left_width, pipe_left_height)
    ball = Ball(center_x_ball, center_y_ball, side_ball, side_ball)

    run = True
    dotted = False

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        window.fill(BLACK)

        if draw_collision_simple_game_objects(dotted, ball.left, ball.top, ball.width):
            ball.reverse_direction_y()

        pipe_right.move()

        if pipe_right.collision(ball.left, ball.top, ball.width):
            ball.reverse_direction_x()
        elif pipe_left.collision(ball.left, ball.top, ball.width):
            ball.reverse_direction_x()

        pipe_right.draw()

        pipe_left.move()
        pipe_left.draw()

        ball.move()
        ball.draw()

        num_score = ball.check_new_score()

        if num_score != 0:
            add_score(num_score)

        updateScore()

        pygame.display.update()
        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit()


if __name__ == '__main__':
    game()
