import pygame
import sys
import random
import json


pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1000, 600
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


pygame.display.set_caption('Meteor shooter')

font = pygame.font.Font(None, 40)

bg_surface = pygame.image.load('fundo.png').convert()


# laser
laser_surf = pygame.image.load('laser.png').convert_alpha()
laser_list = []


# player
x_pos = WINDOW_WIDTH//2
ship = pygame.image.load('ships/Ship_1.png').convert_alpha()
ship_rect = ship.get_rect(center=(x_pos, 460))


# meteoro
meteoro = pygame.image.load('meteoro.png').convert_alpha()
meteoro = pygame.transform.scale(meteoro, (32*3, 32*3))
meteor_rect = meteoro.get_rect()
meteor_list = []

meteor_time = pygame.event.custom_type()
pygame.time.set_timer(meteor_time, 600)


def text_menu(texto='Asteroids wave', y=WINDOW_HEIGHT//2):
    menu_surf = font.render(texto, True, (255, 255, 255))
    menu_rect = menu_surf.get_rect(center=(WINDOW_WIDTH//2, y))
    display_surface.blit(menu_surf, menu_rect)


def laser_update(laser_list, speed=10):
    for rect in laser_list:
        rect.y -= speed
        if rect.bottom < 0:
            laser_list.remove(rect)


def meteor_update(meteor_list, speed=4):
    for rect in meteor_list:
        rect.y += speed
        if rect.top > WINDOW_HEIGHT:
            meteor_list.remove(rect)


def display_score(score):

    text_surf = font.render(f'Score: {score}', True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=(140, 60))
    display_surface.blit(text_surf, text_rect)


def display_life(vida):

    text_surf = font.render(f'Life: {vida}', True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=(140, 100))
    display_surface.blit(text_surf, text_rect)

# def rotate(surface, angle):
#     rotate_surface = pygame.transform.rotozoom(surface, angle, 1)
#     rotated_rect = rotate_surface.get_rect(center = (300,300))

#     return rotate_surface, rotated_rect


pontos = 0

data = {
    'highscore': 0
}

try:
    with open('score.text') as score_file:
        data = json.load(score_file)

except:
    print('sem arquivo')


highscore = data["highscore"]

# variaveis

bg_surface_main = pygame.image.load('spacebg.png').convert_alpha()

bg_surface_main = pygame.transform.scale(
    bg_surface_main, (WINDOW_WIDTH, WINDOW_HEIGHT))


# sons
laser_sound = pygame.mixer.Sound('laser.ogg')

explosion_sound = pygame.mixer.Sound('explosion.wav')


def main_menu():
    global pontos, highscore, data

    if pontos > highscore:
        data['highscore'] = pontos
        highscore = pontos

    while True:
        display_surface.fill((2, 2, 2))
        display_surface.blit(bg_surface_main, (0, 0))
        text_menu()
        text_menu("Play", (WINDOW_HEIGHT//2) + 100)
        text_menu(f'High Score: {highscore}', 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                with open('score.text', "w") as score_file:
                    json.dump(data, score_file)

                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game()

        pygame.display.update()


def game():
    global pontos, ship_rect, ship
    pontos = 0
    vida = 5
    run = True
    comecar = False

    while run:
        display_surface.fill((0, 200, 0))
        display_surface.blit(bg_surface, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                comecar = True

                laser_rect = laser_surf.get_rect(
                    midbottom=(ship_rect.midtop))
                laser_list.append(laser_rect)
                laser_sound.play()

            if event.type == pygame.KEYDOWN:
                comecar = True
                # if event.key == pygame.K_a:
                #     angle += 10
                #     # ship = pygame.transform.rotate(ship, angulo)
                #     ship , ship_rect = rotate(ship, angle)

                # if event.key == pygame.K_d:
                #     ship_rect.x += 20

            if event.type == meteor_time and comecar:
                x_pos = random.randint(100, WINDOW_WIDTH-120)
                meteor_rect = meteoro.get_rect(center=(x_pos, -100))
                meteor_list.append(meteor_rect)

        # ship_rect.center = (pygame.mouse.get_pos()[0],500)

        # ship_rotated, ship_rotated_rect = rotate(ship, angle)

        # display_surface.blit(ship_rotated, ship_rotated_rect)

        if comecar == False:
            text_menu("Press any key to begin", (WINDOW_HEIGHT//2))

        if pygame.key.get_pressed()[pygame.K_a]:
            ship_rect.x -= 8

        if pygame.key.get_pressed()[pygame.K_d]:
            ship_rect.x += 8

        display_surface.blit(ship, ship_rect)

        # chamar funcoes

        laser_update(laser_list)

        meteor_update(meteor_list)

        display_score(pontos)
        display_life(vida)

        # fors

        for rect in laser_list:
            display_surface.blit(laser_surf, rect)

        for rect in meteor_list:
            display_surface.blit(meteoro, rect)

        for laser_rect in laser_list:
            for meteor_tuple in meteor_list:
                if laser_rect.colliderect(meteor_tuple):
                    meteor_list.remove(meteor_tuple)
                    laser_list.remove(laser_rect)
                    explosion_sound.play()
                    pontos += 1

        for meteor_tuple in meteor_list:
            meteor_rect = meteor_tuple
            if ship_rect.colliderect(meteor_rect):
                explosion_sound.play()
                meteor_list.remove(meteor_tuple)
                vida -= 1

            if vida <= 0:
                meteor_list.clear()
                comecar = False
                game_over()

        pygame.display.update()


def game_over():
    run = True

    while run:
        display_surface.fill((0, 200, 0))
        display_surface.blit(bg_surface, (0, 0))

        text_menu("Gamer over", WINDOW_HEIGHT//2)
        text_menu(f"Score: {pontos}", (WINDOW_HEIGHT//2)+50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main_menu()

        pygame.display.update()


main_menu()
