import pygame

pygame.init()

game_window = pygame.display.set_mode((1000,1000), pygame.FULLSCREEN)
black_color = (0,0,0)
dark_slate = (30, 30, 45)
white_color = (255,255,255)
lavender = (201, 184, 232)

game_music = 'chill_piano.wav'

rect_x_pos = 0
rect_y_pos = 200

rect_width = 20
rect_height = 200
rect_centre = rect_height/2

# Rendering ball to center of screen
initial_x = 630
initial_y = 500
ball_x_pos = initial_x
ball_y_pos = initial_y
ball_velocity = [3,5]

rect_movement_velocity = 10
game_running = True

def display_score(header_text, player_score_int,x,y):
    font20 = pygame.font.Font('freesansbold.ttf', 20)
    text = font20.render(header_text + str(player_score_int),True, white_color)
    text_rect = text.get_rect()
    text_rect.center = (x,y)

    game_window.blit(text, text_rect)

def reset_ball(x,y):
    x = initial_x
    y = initial_y

    return x,y

player_score = 0
ai_score = 0
player_score_header = "Player Score: "
ai_score_header = "AI Score: "

# Load mixer and play music
pygame.mixer.init()
music_player = pygame.mixer.music
music_player.load(game_music)
music_player.play(-1, 0, 5)

while game_running:
    pygame.time.delay(10)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            game_running = False

    # Player controls
    if keys[pygame.K_w] and rect_y_pos>0:
        rect_y_pos -= rect_movement_velocity
    if keys[pygame.K_s] and rect_y_pos<1000-rect_height:
        rect_y_pos += rect_movement_velocity

    # Ball physics
    ball_x_pos += ball_velocity[0]
    ball_y_pos += ball_velocity[1]
    if ball_x_pos >= 1260:
        player_score += 1
        ball_x_pos, ball_y_pos = reset_ball(ball_x_pos, ball_y_pos)
    elif ball_x_pos < 0:
        ai_score += 1
        ball_x_pos, ball_y_pos = reset_ball(ball_x_pos, ball_y_pos)
    # Top/bottom walls
    if ball_y_pos <= 0 or ball_y_pos >= 1000:
        ball_velocity[1] = -ball_velocity[1]

    # Draw sprites
    game_window.fill(dark_slate)
    player = pygame.draw.rect(game_window,lavender, (rect_x_pos, rect_y_pos, rect_width, rect_height))
    player_top_paddle = pygame.draw.rect(game_window,lavender, (rect_x_pos, rect_y_pos, rect_width, rect_height//2))
    ai = pygame.draw.rect(game_window, lavender, (1260, 0, rect_width, rect_height))
    ball = pygame.draw.rect(game_window, white_color, (ball_x_pos, ball_y_pos, 20, 20))

    # Detect collisions
    if player.colliderect(ball):
        # Checks if ball hits top of the paddle
        if ball_y_pos < player.y:
            player.y = ball_y_pos
            ball_velocity[1] = -ball_velocity[1]
        else:
            player.x = ball_x_pos
            player.y = ball_y_pos
            ball_velocity[0] = -ball_velocity[0]

    if ai.colliderect(ball):
        ai.x = ball_x_pos
        ai.y = ball_y_pos
        ball_velocity[0] = -ball_velocity[0]

    # Display Player and AI scores
    display_score(player_score_header, player_score,80,10)
    display_score(ai_score_header, ai_score, 1200, 10)

    pygame.display.update()

pygame.quit()