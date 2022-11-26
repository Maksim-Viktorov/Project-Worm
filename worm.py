import random
import pygame
from globals import globals


def draw_level(surface, level):
    for y in range(globals.level_height):
        for x in range(globals.level_width):
            rect = pygame.Rect(x * globals.sprite_width, y * globals.sprite_height,
                               globals.sprite_width, globals.sprite_height)
            color = globals.back_color
            if (x + y) % 2 == 1:
                color = globals.light_back_color
            pygame.draw.rect(surface, color, rect)

            rect = pygame.Rect(x * globals.sprite_width + 1, y * globals.sprite_height + 1,
                               globals.sprite_width - 2, globals.sprite_height - 2)
            cell = level[y * globals.level_width + x]
            if cell == '#':
                pygame.draw.rect(surface, globals.wall_color, rect)
            elif cell == 'A':
                points = [(rect.left + rect.width / 2, rect.top),
                          (rect.left, rect.bottom),
                          (rect.right, rect.bottom)]
                pygame.draw.polygon(surface, globals.accel_color, points)
            elif cell == 'B':
                points = [(rect.left + rect.width / 2, rect.bottom - 1),
                          (rect.right, rect.top),
                          (rect.left, rect.top)]
                pygame.draw.polygon(surface, globals.decel_color, points)


def draw_fruit(surface, fruit):
    rect = pygame.Rect(fruit[0] * globals.sprite_width, fruit[1] * globals.sprite_height,
                       globals.sprite_width, globals.sprite_height)
    pygame.draw.ellipse(surface, globals.fruit_color, rect)


def draw_score(surface, font, score):
    rect = pygame.Rect(0, globals.level_height * globals.sprite_height,
                       globals.level_width * globals.sprite_width,
                       globals.level_height * globals.sprite_height + globals.score_height)
    surface.fill(globals.score_back_color, rect)
    text_surface = font.render('  Score: ' + str(score), True, globals.score_color, globals.score_back_color)
    text_size = text_surface.get_size()
    surface.blit(text_surface, (0,
                                globals.level_height * globals.sprite_height +
                                (globals.sprite_height - text_size[1]) / 2))


def init_level(level, worm, fruits):
    for y in range(globals.level_height):
        for x in range(globals.level_width):
            cell = level[y * globals.level_width + x]
            if cell >= '0' and cell <= '9':
                i = int(cell)
                for j in range(len(worm), i + 1):
                    worm.append(None)
                worm[i] = (x, y)
            elif cell == '@':
                fruits.append((x, y))
    random.shuffle(fruits)


def draw_worm(surface, worm_color, worm, direction=None, delta=0):
    for i in range(len(worm)):
        rect = pygame.Rect(worm[i][0] * globals.sprite_width,
                           worm[i][1] * globals.sprite_height,
                           globals.sprite_width, globals.sprite_height)
        color = globals.back_color
        if (worm[i][0] + worm[i][1]) % 2 == 1:
            color = globals.light_back_color
        pygame.draw.rect(surface, color, rect)

    prev = None
    for i in range(len(worm)):
        if worm_color is not None:
            if i > 0 and direction is not None:
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
            rect = pygame.Rect((worm[i][0] + dx) * globals.sprite_width + 3 + i / 2,
                               (worm[i][1] + dy) * globals.sprite_height + 3 + i / 2,
                               globals.sprite_width - 6 - i, globals.sprite_height - 6 - i)
            pygame.draw.ellipse(surface, worm_color, rect)
            if prev is not None:
                points = [(prev.left, (prev.top + prev.bottom) / 2),
                          (prev.right, (prev.top + prev.bottom) / 2),
                          (rect.right, (rect.top + rect.bottom) / 2),
                          (rect.left, (rect.top + rect.bottom) / 2)]
                pygame.draw.polygon(surface, worm_color, points)

                points = [((prev.left + prev.right) / 2, prev.top),
                          ((prev.left + prev.right) / 2, prev.bottom - 1),
                          ((rect.left + rect.right) / 2, rect.bottom - 1),
                          ((rect.left + rect.right) / 2, rect.top)]
                pygame.draw.polygon(surface, worm_color, points)
            prev = rect


def draw_text_lines(surface, font, lines):
    width = 14 * globals.sprite_width
    height = (0.5 + len(lines) + 0.5) * globals.score_height
    x = (globals.level_width * globals.sprite_width - width) / 2
    y = (globals.level_height * globals.sprite_height - height) / 2
    rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(surface, globals.score_back_color, rect,
                     border_radius=globals.sprite_width // 2)
    y += 0.5 * globals.score_height
    for i in range(len(lines)):
        text_surface = font.render(str(lines[i]), True, globals.score_color, globals.score_back_color)
        text_size = text_surface.get_size()
        surface.blit(text_surface, (x + (width - text_size[0]) / 2,
                                    y + (globals.score_height - text_size[1]) / 2))
        y += globals.score_height


def main():
    pygame.init()
    pygame.display.set_caption("Worm")
    surface = pygame.display.set_mode(
        (globals.level_width * globals.sprite_width,
         globals.level_height * globals.sprite_height + globals.score_height))
    font = pygame.font.SysFont(None, globals.score_height)
    clock = pygame.time.Clock()

    score = 0

    (LEVELSELECT, INITLEVEL, GAME, LEVELUP, GAMEOVER, QUIT) = (0, 1, 2, 3, 4, 5)
    state = LEVELSELECT
    draw_text_lines(surface, font,
                    ['Use arrow keys to control the worm', '',
                     'Press 1 to 5 to select level'])
    while state != QUIT:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = QUIT
                if state == GAME:
                    if event.key == pygame.K_UP:
                        if prev_direction != 'D':
                            direction = 'U'
                    elif event.key == pygame.K_DOWN:
                        if prev_direction != 'U':
                            direction = 'D'
                    elif event.key == pygame.K_LEFT:
                        if prev_direction != 'R':
                            direction = 'L'
                    elif event.key == pygame.K_RIGHT:
                        if prev_direction != 'L':
                            direction = 'R'
                elif state == LEVELSELECT:
                    if event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5):
                        score = 0
                        levelno = event.key - pygame.K_1
                        state = INITLEVEL
                elif state == LEVELUP:
                    levelno = levelno + 1
                    if levelno >= len(globals.levels):
                        levelno = 0
                    state = INITLEVEL
            if event.type == pygame.QUIT:
                state = QUIT

        if state == INITLEVEL:
            level = globals.levels[levelno]
            worm = []
            fruits = []
            init_level(level, worm, fruits)
            prev_worm = worm
            prev_direction = None
            direction = None
            speed = 4
            accel = 0.10

            millis = pygame.time.get_ticks()

            draw_level(surface, level)
            draw_fruit(surface, fruits[0])
            draw_score(surface, font, score)
            draw_worm(surface, globals.worm_color, worm, 'U', 0)

            state = GAME

        if state == GAME:
            now = pygame.time.get_ticks()
            new_speed = speed + (now - millis) / 1000 * accel
            if new_speed > 20:
                new_speed = 20
            delta = (now - millis) / 1000 * new_speed
            if delta >= 1:
                millis += 1000 / new_speed
                speed = speed + 1 / new_speed * accel
                if speed > 20:
                    speed = 20

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
                pos = y * globals.level_width + x
                if x < 0 or x >= globals.level_width or y < 0 or y >= globals.level_height \
                        or level[pos] == '#' \
                        or (x, y) in worm:
                    globals.top_scores.append(score)
                    globals.top_scores = sorted(globals.top_scores, reverse=True)[:3]
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
                        if speed > 20:
                            speed = 20
                    elif level[pos] == 'B':
                        level = level[:pos] + ' ' + level[pos + 1:]
                        speed = speed * 0.5
                        if speed < 4:
                            speed = 4
                draw_worm(surface, globals.worm_color, prev_worm, prev_direction, 0)
                if len(fruits) > 0:
                    if not fruits[0] in worm:
                        draw_fruit(surface, fruits[0])
                else:
                    draw_worm(surface, globals.worm_color, worm, prev_direction, 0)
                    state = LEVELUP
                draw_score(surface, font, score)
            else:
                draw_worm(surface, globals.worm_color, prev_worm, prev_direction, delta)

        if state == GAMEOVER:
            draw_text_lines(surface, font,
                            ['Game over', '', 'Top scores'] +
                            globals.top_scores + ['', 'Press 1 to 5 to select level'])
            state = LEVELSELECT
        elif state == LEVELUP:
            draw_text_lines(surface, font,
                            ['Level up!', '', 'Press any key to continue'])

        pygame.display.flip()
        clock.tick(60)
