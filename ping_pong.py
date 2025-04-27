import pygame
import time

pygame.init()

# класс-родитель для спрайтов 
class GameSprite(pygame.sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, height):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(player_image), (width, height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update_r(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed

    def update_l(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.y < win_height - 80:
            self.rect.y += self.speed

# Настройки окна
back = (200, 255, 255)
win_width = 600
win_height = 500
window = pygame.display.set_mode((win_width, win_height))
window.fill(back)

clock = pygame.time.Clock()
FPS = 60

# Создание объектов
racket1 = Player('racket.png', 7, 200, 4, 50, 150)
racket2 = Player('racket.png', 560, 200, 4, 50, 150)
ball = GameSprite('tenis_ball.png', 200, 200, 4, 50, 50)

pygame.font.init()
game_font = pygame.font.Font(None, 35)

# Тексты для проигрыша (будут обновляться динамически)
lose1_text = 'PLAYER 1 LOSE!'
lose2_text = 'PLAYER 2 LOSE!'

# Начальные параметры
speed_x = 3
speed_y = 3
last_speed_increase_time = time.time()

# Счётчики очков
score1 = 0
score2 = 0

# Флаги состояния игры
game = True
finish = False

def reset_game():
    global finish, speed_x, speed_y, ball, racket1, racket2, score1, score2, last_speed_increase_time
    finish = False
    speed_x = 3
    speed_y = 3
    score1 = 0
    score2 = 0
    ball.rect.x = win_width // 2 - ball.rect.width // 2
    ball.rect.y = win_height // 2 - ball.rect.height // 2
    racket1.rect.y = 200
    racket2.rect.y = 200
    last_speed_increase_time = time.time()

while game:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            game = False
        if e.type == pygame.KEYDOWN:
            if finish and e.key == pygame.K_SPACE:
                reset_game()

    if not finish:
        window.fill(back)
        racket1.update_l()
        racket2.update_r()
        ball.rect.x += speed_x
        ball.rect.y += speed_y

        # Отскок мяча от ракеток
        if pygame.sprite.collide_rect(racket1, ball) or pygame.sprite.collide_rect(racket2, ball):
            speed_x *= -1

        # Отскок мяча от верхней и нижней границ
        if ball.rect.y > win_height - ball.rect.height or ball.rect.y < 0:
            speed_y *= -1

        # Мяч вышел за левую границу - очко игроку 2
        if ball.rect.x < 0:
            score2 += 1
            ball.rect.x = win_width // 2 - ball.rect.width // 2
            ball.rect.y = win_height // 2 - ball.rect.height // 2
            speed_x = 3  # сброс скорости
            speed_y = 3

        # Мяч вышел за правую границу - очко игроку 1
        if ball.rect.x > win_width:
            score1 += 1
            ball.rect.x = win_width // 2 - ball.rect.width // 2
            ball.rect.y = win_height // 2 - ball.rect.height // 2
            speed_x = -3  # сброс скорости, меняем направление
            speed_y = 3

        # Проверка на победу (10 очков)
        if score1 >= 10:
            finish = True
            lose_message = game_font.render(lose2_text, True, (180, 0, 0))
        elif score2 >= 10:
            finish = True
            lose_message = game_font.render(lose1_text, True, (180, 0, 0))

        # Увеличение скорости каждые 5 секунд
        current_time = time.time()
        if current_time - last_speed_increase_time >= 5:
            speed_x += 1 if speed_x > 0 else -1
            speed_y += 1 if speed_y > 0 else -1
            last_speed_increase_time = current_time

        # Отрисовка объектов
        racket1.reset()
        racket2.reset()
        ball.reset()

        # Отрисовка счёта
        score1_text = game_font.render(f"Player 1: {score1}", True, (0, 0, 0))
        score2_text = game_font.render(f"Player 2: {score2}", True, (0, 0, 0))
        window.blit(score1_text, (10, 10))
        window.blit(score2_text, (win_width - score2_text.get_width() - 10, 10))

    else:
        # Отрисовка экрана проигрыша
        window.fill(back)
        window.blit(lose_message, (win_width//2 - lose_message.get_width()//2, win_height//2 - lose_message.get_height()//2))

        # Подсказка для перезапуска
        restart_text = game_font.render("Press SPACE to restart", True, (50, 50, 50))
        window.blit(restart_text, (win_width//2 - restart_text.get_width()//2, win_height//2 + 50))

    pygame.display.update()
    clock.tick(FPS)

