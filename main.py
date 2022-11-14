
import time
import random
import pygame

level_width = 32
level_height = 24
level1 = "################################" \
         "#                              #" \
         "#                       @      #" \
         "#     @####    B     ####      #" \
         "#      #@             @ #      #" \
         "#      #                #      #" \
         "#      #                #      #" \
         "#              @               #" \
         "#   210                        #" \
         "#           #######            #" \
         "#           #  @  #            #" \
         "#           #     #            #" \
         "#           #     #            #" \
         "#                              #" \
         "#              @               #" \
         "#      #                #      #" \
         "#      #                #      #" \
         "#      #@              @#      #" \
         "#      ##################@     #" \
         "#      @       A               #" \
         "#           #######            #" \
         "#              @               #" \
         "#                              #" \
         "################################"

sprite_width = 32
sprite_height = 32
score_height = 32

back_color = (0, 0x3f, 0xf)
light_back_color = (0, 0x48, 0x18)
wall_color = (0x3f, 0, 0)
worm_color = (0xcf, 0xcf, 0)
fruit_color = (0xff, 0, 0)
accel_color = (0, 0, 0xcf)
decel_color = (0, 0, 0x3f)
score_color = (0, 0, 0)
score_back_color = (0xcf, 0xcf, 0xcf)

def draw_level(surface, level):
    for y in range(level_height):
        for x in range(level_width):
            rect = pygame.Rect(x * sprite_width, y * sprite_height,
                               sprite_width, sprite_height)
            color = back_color
            if (x + y) % 2 == 1:
                color = light_back_color
            pygame.draw.rect(surface, color, rect)

            rect = pygame.Rect(x * sprite_width + 1, y * sprite_height + 1,
                               sprite_width - 2, sprite_height - 2)
            cell = level[y * level_width + x]
            if cell == '#':
                pygame.draw.rect(surface, wall_color, rect)
            elif cell == 'A':
                points = [(rect.left + rect.width / 2, rect.top),
                          (rect.left, rect.bottom),
                          (rect.right, rect.bottom)]
                pygame.draw.polygon(surface, accel_color, points)
            elif cell == 'B':
                points = [(rect.left + rect.width / 2, rect.bottom - 1),
                          (rect.right, rect.top),
                          (rect.left, rect.top)]
                pygame.draw.polygon(surface, decel_color, points)

def draw_fruit(surface, fruit):
    rect = pygame.Rect(fruit[0] * sprite_width, fruit[1] * sprite_height,
                       sprite_width, sprite_height)
    pygame.draw.ellipse(surface, fruit_color, rect)

def draw_score(surface, font, score):
    rect = pygame.Rect(0, level_height * sprite_height,
                       level_width * sprite_width,
                       level_height * sprite_height + score_height)
    surface.fill(score_back_color, rect)
    text_surface = font.render('  Score: ' + str(score), True, score_color, score_back_color)
    text_size = text_surface.get_size()
    surface.blit(text_surface, (0,
                                level_height * sprite_height +
                                (sprite_height - text_size[1]) / 2))

def init_level(level, worm, fruits):
    for y in range(level_height):
        for x in range(level_width):
            cell = level[y * level_width + x]
            if cell >= '0' and cell <= '9':
                i = int(cell)
                for j in range(len(worm), i + 1):
                    worm.append(None)
                worm[i] = (x, y)
            elif cell == '@':
                fruits.append((x, y))
    random.shuffle(fruits)

def draw_worm(surface, worm_color, worm, direction = None, delta = 0):
    for i in range(len(worm)):
        rect = pygame.Rect(worm[i][0] * sprite_width,
                           worm[i][1] * sprite_height,
                           sprite_width, sprite_height)
        color = back_color
        if (worm[i][0] + worm[i][1]) % 2 == 1:
            color = light_back_color
        pygame.draw.rect(surface, color, rect)

    prev = None
    for i in range(len(worm)):
        if worm_color != None:
            if i > 0 and direction != None:
                if worm[i - 1][0] == worm[i][0]:
                    if worm[i - 1][1] < worm[i][1]:
                        direction = 'U'
                    else:
                        direction = 'D'
                else:
                    if worm[i - 1][0] < worm[i][0]:
                        direction = 'L'
                    else:
                        direction = 'R'
            dx, dy = 0, 0
            if direction == 'U':
                dy = -delta
            elif direction == 'D':
                dy = delta
            elif direction == 'L':
                dx = -delta
            elif direction == 'R':
                dx = delta
            rect = pygame.Rect((worm[i][0] + dx) * sprite_width + 3 + i / 2,
                               (worm[i][1] + dy) * sprite_height + 3 + i / 2,
                               sprite_width - 6 - i, sprite_height - 6 - i)
            pygame.draw.ellipse(surface, worm_color, rect)
            if prev != None:
                points = [(prev.left, (prev.top + prev.bottom) / 2),
                          (prev.right - 1, (prev.top + prev.bottom) / 2),
                          (rect.right - 1, (rect.top + rect.bottom) / 2),
                          (rect.left, (rect.top + rect.bottom) / 2)]
                pygame.draw.polygon(surface, worm_color, points)

                points = [((prev.left + prev.right) / 2, prev.top),
                          ((prev.left + prev.right) / 2, prev.bottom - 1),
                          ((rect.left + rect.right) / 2, rect.bottom - 1),
                          ((rect.left + rect.right) / 2, rect.top)]
                pygame.draw.polygon(surface, worm_color, points)
            prev = rect

def draw_gameover(surface, font, text):
    x = level_width * sprite_width / 2
    y = level_height * sprite_height / 2
    rect = pygame.Rect(x - sprite_width * 2.5, y - sprite_height * 2.5,
                       sprite_width * 5, sprite_height * 5)
    pygame.draw.ellipse(surface, score_back_color, rect)
    text_surface = font.render(text, True, score_color, score_back_color)
    text_size = text_surface.get_size()
    surface.blit(text_surface, (x - text_size[0] / 2, y - text_size[1] / 2))

def main():
    pygame.init()
    surface = pygame.display.set_mode(
        (level_width * sprite_width,
         level_height * sprite_height + score_height))
    font = pygame.font.SysFont(None, score_height)

    level = level1
    worm = []
    fruits = []
    init_level(level, worm, fruits)
    prev_worm = worm
    prev_direction = None
    direction = None
    speed = 4
    accel = 0.3

    score = 0

    millis = pygame.time.get_ticks()

    draw_level(surface, level)
    draw_fruit(surface, fruits[0])
    draw_score(surface, font, score)
    draw_worm(surface, worm_color, worm, 'U', 0)
    pygame.display.flip()

    clock = pygame.time.Clock()

    (GAME, YOUWON, GAMEOVER, QUIT) = (0, 1, 2, 3)
    state = GAME
    while state != QUIT:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = QUIT
                elif event.key == pygame.K_UP:
                    if direction != 'D':
                        direction = 'U'
                elif event.key == pygame.K_DOWN:
                    if direction != 'U':
                        direction = 'D'
                elif event.key == pygame.K_LEFT:
                    if direction != 'R':
                        direction = 'L'
                elif event.key == pygame.K_RIGHT:
                    if direction != 'L':
                        direction = 'R'
            if event.type == pygame.QUIT:
                state = QUIT

        if state == GAME:
            now = pygame.time.get_ticks()
            new_speed = speed + (now - millis) / 1000 * accel
            if new_speed > 30:
                new_speed = 30
            delta = (now - millis) / 1000 * new_speed
            if delta >= 1:
                millis += 1000 / new_speed
                speed = speed + 1 / new_speed * accel
                if speed > 30:
                    speed = 30

                prev_direction = direction
                prev_worm = worm
                x, y = worm[0]
                if direction == 'U':
                    y = y - 1
                elif direction == 'D':
                    y = y + 1
                elif direction == 'L':
                    x = x - 1
                elif direction == 'R':
                    x = x + 1
                else:
                    continue
                draw_worm(surface, None, worm)
                pos = y * level_width + x
                if x < 0 or x >= level_width \
                    or y < 0 or y >= level_height \
                    or level[pos] == '#' \
                    or (x, y) in worm:
                    state = GAMEOVER
                elif (x, y) == fruits[0]:
                    fruits = fruits[1:]
                    score = score + 1
                    # grow
                    worm = [(x, y)] + worm
                else:
                    # move
                    worm = [(x, y)] + worm[:len(worm) - 1]
                if level[pos] == 'A':
                    level = level[:pos] + ' ' + level[pos + 1:]
                    speed = speed * 1.5
                    if speed > 30:
                        speed = 30
                elif level[pos] == 'B':
                    level = level[:pos] + ' ' + level[pos + 1:]
                    speed = speed * 0.5
                    if speed < 4:
                        speed = 4
                draw_worm(surface, worm_color, prev_worm, prev_direction, 0)
                if len(fruits) > 0:
                    if not fruits[0] in worm:
                        draw_fruit(surface, fruits[0])
                else:
                    state = YOUWON
                draw_score(surface, font, score)
            else:
                draw_worm(surface, worm_color, prev_worm, prev_direction, delta)

        if state == GAMEOVER:
            draw_gameover(surface, font, 'Game over')
        elif state == YOUWON:
            draw_gameover(surface, font, 'You won')

        pygame.display.flip()

        clock.tick(60)


if __name__ == '__main__':
    main()
