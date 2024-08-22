import pygame as pg
import sys

# COLORS
WHITE = (255, 255, 255)
GRAY = (144, 144, 144)
BLACK = (0, 0, 0)
RED = (255, 32, 78)
BLUE = (0, 0, 255)
GREEN = (22, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 143, 0)
LIGHT_BLUE = (0, 121, 255)
AQUA = (0, 255, 255)
LIGHT_PURPLE = (173, 73, 225)


def create_arrow_surface(color, size='normal'):
    if size == 'normal':
        arrow_surface = pg.Surface((20, 110), pg.SRCALPHA)
        arrow_points = [(10, 0), (20, 20), (12.5, 20), (12.5, 110), (7.5, 110), (7.5, 20), (0, 20)]
    elif size == 'small':
        arrow_surface = pg.Surface((20, 100), pg.SRCALPHA)
        arrow_points = [(10, 0), (20, 20), (12.5, 20), (12.5, 100), (7.5, 100), (7.5, 20), (0, 20)]

    pg.draw.polygon(arrow_surface, color, arrow_points)
    return arrow_surface


def draw_arrow(screen, arrow_surface, pos, angle):
    rotated_arrow = pg.transform.rotate(arrow_surface, angle)
    arrow_rect = rotated_arrow.get_rect(center=pos)
    screen.blit(rotated_arrow, arrow_rect)


# def draw_circle(screen, pos, radius, color):
#     pg.draw.circle(screen, color, pos, radius)


def render_text(screen, font, text, pos, color):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, pos)


def fill_arrow(surface, color):
    mask = pg.mask.from_surface(surface)
    for x in range(surface.get_width()):
        for y in range(surface.get_height()):
            if mask.get_at((x, y)):
                surface.set_at((x, y), color)


def draw_button(screen, color, x, y, width, height, text='', text_color=WHITE):
    pg.draw.rect(screen, color, (x, y, width, height))
    if text != '':
        font = pg.font.Font(None, 30)
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=(x + width / 2, y + height / 2))
        screen.blit(text_surface, text_rect)


def button_clicked(x, y, width, height, mouse_pos):
    return x < mouse_pos[0] < x + width and y < mouse_pos[1] < y + height


def run(values, CAPACITY, X8):
    traffic = 1
    user_text = ''
    X8_input = ''
    negatives = []

    cycle = 0
    X8_input_box = False

    traffic_lights1 = None
    traffic_lights2 = None

    # Initialize Pygame
    pg.init()
    screen = pg.display.set_mode((1250, 700))
    pg.display.set_caption("Simulation of a Roundway with Traffic Lights")
    clock = pg.time.Clock()
    FPS = 60  # Set the desired FPS

    input_rect = pg.Rect(20, 50, 140, 32) 

    # Initialize values
    Ea, Ec, Ee, Eg = values[0]
    Sb, Sd, Sf, Sh = values[1]

    # Initialize font
    pg.font.init()
    font_big = pg.font.Font(None, 50)  # None for default font
    font_normal = pg.font.Font(None, 30)
    font_small = pg.font.Font(None, 24)

    # Create arrow surfaces
    arrow_north_in, arrow_north_out, arrow_east_in, arrow_east_out, arrow_south_in, arrow_south_out, arrow_west_in, arrow_west_out = [create_arrow_surface(LIGHT_BLUE, 'small') if i % 2 == 0 else create_arrow_surface(ORANGE, 'small') for i in range(8)]

    arrow_surfaces = [create_arrow_surface(WHITE) for _ in range(8)]
    arrow_surfaces = [pg.transform.scale(arrow_surface, (arrow_surface.get_width(), int(arrow_surface.get_height() * 1.2))) for arrow_surface in arrow_surfaces]
    arrow_ab, arrow_bc, arrow_cd, arrow_de, arrow_ef, arrow_fg, arrow_gh, arrow_ha = arrow_surfaces

    # Main loop
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if button_clicked(275, 25, 200, 50, mouse_pos):
                    cycle = 0 if cycle == 1 else 1
                if button_clicked(275, 90, 200, 50, mouse_pos):
                    X8_input_box = True

            if (traffic < 3):
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_BACKSPACE:
                        user_text = user_text[:-1]

                    elif event.key == pg.K_RETURN:
                        if traffic == 1:
                            traffic_lights1 = user_text.split()
                            if traffic_lights1 == ['']:
                                traffic_lights1 = []

                            user_text = ''
                        else:
                            traffic_lights2 = user_text.split()
                            if traffic_lights2 == ['']:
                                traffic_lights2 = []

                            user_text = ''

                        traffic += 1

                    else:
                        user_text += event.unicode
            elif X8_input_box == True:
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_BACKSPACE:
                        X8_input = X8_input[:-1]

                    elif event.key == pg.K_RETURN:
                        X8 = int(X8_input)
                        X8_input = ''
                        X8_input_box = False

                    else:
                        X8_input += event.unicode

        screen.fill(BLACK)

        if traffic < 3:
            if traffic == 2:
                remaining_lights = [light for light in ['Ea', 'Ec', 'Ee', 'Eg'] if light not in traffic_lights1]
                remaining_lights_text = ' '.join(remaining_lights)
                render_text(screen, font_normal, f'Traffic Lights Cycle 2 - {remaining_lights_text}', (20, 10), GREEN)
                render_text(screen, font_small, 'Enter the roads separated by space - Empty if none', (20, 40), LIGHT_PURPLE)
            else:
                render_text(screen, font_normal, 'Traffic Lights Cycle 1 - Ea Ec Ee Eg', (20, 10), GREEN)
                render_text(screen, font_small, 'Enter the roads separated by space - Empty if none', (20, 40), LIGHT_PURPLE)
            
            render_text(screen, font_small, '> ' + user_text, (20, 60), WHITE)


        # Draw Graph

        # Nodes
        render_text(screen, font_big, 'A', (600, 130), YELLOW)
        render_text(screen, font_big, 'B', (800, 130), YELLOW)
        render_text(screen, font_big, 'C', (950, 230), YELLOW)
        render_text(screen, font_big, 'D', (950, 430), YELLOW)
        render_text(screen, font_big, 'E', (800, 530), YELLOW)
        render_text(screen, font_big, 'F', (600, 530), YELLOW)
        render_text(screen, font_big, 'G', (455, 430), YELLOW)
        render_text(screen, font_big, 'H', (455, 230), YELLOW)

        # Edges Values
        render_text(screen, font_small, 'X1', (680, 110), WHITE)
        render_text(screen, font_small, 'X2', (895, 170), WHITE)
        render_text(screen, font_small, 'X3', (980, 320), WHITE)
        render_text(screen, font_small, 'X4', (900, 500), WHITE)
        render_text(screen, font_small, 'X5', (690, 560), WHITE)
        render_text(screen, font_small, 'X6', (485, 510), WHITE)
        render_text(screen, font_small, 'X7', (395, 345), WHITE)
        render_text(screen, font_small, 'X8', (480, 170), WHITE)

        # Edges In and Out Values
        render_text(screen, font_small, 'Ea', (620, 60), BLUE)
        render_text(screen, font_small, 'Sb', (825, 60), ORANGE)
        render_text(screen, font_small, 'Ec', (1025, 215), BLUE)
        render_text(screen, font_small, 'Sd', (1005, 415), ORANGE)
        render_text(screen, font_small, 'Ee', (820, 615), BLUE)
        render_text(screen, font_small, 'Sf', (620, 615), ORANGE)
        render_text(screen, font_small, 'Eg', (360, 415), BLUE)
        render_text(screen, font_small, 'Sh', (370, 215), ORANGE)


        # Edges - In and Out
        # North
        draw_arrow(screen, arrow_north_in, (612, 70), 180)
        draw_arrow(screen, arrow_north_out, (812, 70), 0)
        # East
        draw_arrow(screen, arrow_east_in, (1035, 245), 90)
        draw_arrow(screen, arrow_east_out, (1035, 445), -90)
        # South
        draw_arrow(screen, arrow_south_in, (812, 620), 0)
        draw_arrow(screen, arrow_south_out, (612, 620), 180)
        # West
        draw_arrow(screen, arrow_west_in, (395, 445), 270)
        draw_arrow(screen, arrow_west_out, (395, 245), 90)

        # Edges - In and Out
        # North
        draw_arrow(screen, arrow_north_in, (612, 70), 180)
        draw_arrow(screen, arrow_north_out, (812, 70), 0)
        # East
        draw_arrow(screen, arrow_east_in, (1035, 245), 90)
        draw_arrow(screen, arrow_east_out, (1035, 445), -90)
        # South
        draw_arrow(screen, arrow_south_in, (812, 620), 0)
        draw_arrow(screen, arrow_south_out, (612, 620), 180)
        # West
        draw_arrow(screen, arrow_west_in, (395, 445), 270)
        draw_arrow(screen, arrow_west_out, (395, 245), 90)

        # Edges - Connections
        # Draw Edges - Connections
        edges = {'X1': (arrow_ab, (715, 145), 270),
            'X2': (arrow_bc, (890, 190), 235),
            'X3': (arrow_cd, (962, 340), 180),
            'X4': (arrow_de, (885, 495), 125),
            'X5': (arrow_ef, (710, 548), 90),
            'X6': (arrow_fg, (540, 495), 55),
            'X7': (arrow_gh, (467, 345), 0),
            'X8': (arrow_ha, (538, 195), 305)}

        for edge, (arrow_surface, position, angle) in edges.items():
            if edge not in negatives:
                draw_arrow(screen, arrow_surface, position, angle)
            else:
                draw_arrow(screen, arrow_surface, position, angle + 180)

        if (traffic_lights1 is not None and traffic_lights2 is not None):

            Ea_aux, Ec_aux, Ee_aux, Eg_aux = Ea, Ec, Ee, Eg

            if set(traffic_lights1) & set(traffic_lights2):
                print("\033[31m" + "\nCycle 2 cannot have the same roads as Cycle 1! Run again!" + "\033[39m")
                traffic_lights2 = list(set(traffic_lights2) - set(traffic_lights1))
            
            if cycle == 0:
                traffic_lights_red = traffic_lights1
                traffic_lights_green = traffic_lights2
            else:
                traffic_lights_red = traffic_lights2
                traffic_lights_green = traffic_lights1
            if 'Ea' in traffic_lights_red:
                Ea_aux = 0
                fill_arrow(arrow_north_in, RED)
            else:
                fill_arrow(arrow_north_in, GREEN)
            if 'Ec' in traffic_lights_red:
                Ec_aux = 0
                fill_arrow(arrow_east_in, RED)
            else:
                fill_arrow(arrow_east_in, GREEN)
            if 'Ee' in traffic_lights_red:
                Ee_aux = 0
                fill_arrow(arrow_south_in, RED)
            else:
                fill_arrow(arrow_south_in, GREEN)
            if 'Eg' in traffic_lights_red:
                Eg_aux = 0
                fill_arrow(arrow_west_in, RED)
            else:
                fill_arrow(arrow_west_in, GREEN)
            
            negatives = []

            total_entries = Ea_aux + Ec_aux + Ee_aux + Eg_aux
            
            # Update Values
            X1 = Ea_aux + X8
            X2 = -(Sb*total_entries/100) + Ea_aux + X8
            X3 = Ec_aux - (Sb*total_entries/100) + Ea_aux + X8
            X4 = -(Sd*total_entries/100) + Ec_aux - (Sb*total_entries/100) + Ea_aux + X8
            X5 = Ee_aux - (Sd*total_entries/100) + Ec_aux - (Sb*total_entries/100) + Ea_aux + X8
            X6 = -(Sf*total_entries/100) + Ee_aux - (Sd*total_entries/100) + Ec_aux - (Sb*total_entries/100) + Ea_aux + X8
            X7 = Eg_aux - (Sf*total_entries/100) + Ee_aux - (Sd*total_entries/100) + Ec_aux - (Sb*total_entries/100) + Ea_aux + X8

            if X1 < 0:
                negatives.append('X1')
            if X2 < 0:
                negatives.append('X2')
            if X3 < 0:
                negatives.append('X3')
            if X4 < 0:
                negatives.append('X4')
            if X5 < 0:
                negatives.append('X5')
            if X6 < 0:
                negatives.append('X6')
            if X7 < 0:
                negatives.append('X7')
            if X8 < 0:
                negatives.append('X8')

            current_flux = abs(X1) + abs(X2) + abs(X3) + abs(X4) + abs(X5) + abs(X6) + abs(X7) + abs(X8)
            if 'Ea' in traffic_lights_red:
                current_flux -= abs(X1)
            if 'Ec' in traffic_lights_red:
                current_flux -= abs(X3)
            if 'Ee' in traffic_lights_red:
                current_flux -= abs(X5)
            if 'Eg' in traffic_lights_red:
                current_flux -= abs(X7)
            overloaded = any(x > CAPACITY for x in [X1, X2, X3, X4, X5, X6, X7, X8])  # True if at least one variable is greater than CAPACITY

            # Edges Values
            render_text(screen, font_small, 'X1: %d' % X1, (680, 110), WHITE)
            render_text(screen, font_small, 'X2: %d' % X2, (895, 170), WHITE)
            render_text(screen, font_small, 'X3: %d' % X3, (980, 320), WHITE)
            render_text(screen, font_small, 'X4: %d' % X4, (900, 500), WHITE)
            render_text(screen, font_small, 'X5: %d' % X5, (690, 560), WHITE)
            render_text(screen, font_small, 'X6: %d' % X6, (485, 510), WHITE)
            render_text(screen, font_small, 'X7: %d' % X7, (395, 345), WHITE)
            render_text(screen, font_small, 'X8: %d' % X8, (480, 170), WHITE)

            # Edges In and Out Values
            render_text(screen, font_small, 'Ea: %d' % Ea_aux, (620, 60), RED if 'Ea' in traffic_lights_red else GREEN)
            render_text(screen, font_small, 'Sb: %d%%' % Sb, (825, 60), ORANGE)
            render_text(screen, font_small, 'Ec: %d' % Ec_aux, (1025, 215), RED if 'Ec' in traffic_lights_red else GREEN)
            render_text(screen, font_small, 'Sd: %d%%' % Sd, (1005, 415), ORANGE)
            render_text(screen, font_small, 'Ee: %d' % Ee_aux, (820, 615), RED if 'Ee' in traffic_lights_red else GREEN)
            render_text(screen, font_small, 'Sf: %d%%' % Sf, (620, 615), ORANGE)
            render_text(screen, font_small, 'Eg: %d' % Eg_aux, (360, 415), RED if 'Eg' in traffic_lights_red else GREEN)
            render_text(screen, font_small, 'Sh: %d%%' % Sh, (370, 215), ORANGE)


            # Show Data
            render_text(screen, font_normal, 'Roundway Status', (10, 10), GREEN)
            render_text(screen, font_small, 'capacity: %d' % CAPACITY, (10, 40), WHITE)
            render_text(screen, font_small, 'total entries: %d' % total_entries, (10, 60), WHITE)
            render_text(screen, font_small, 'flux inside: %d' % current_flux, (10, 80), WHITE)
            if (overloaded):
                render_text(screen, font_small, 'Roundway Overloaded', (10, 100), RED)
            else:
                render_text(screen, font_small, 'Roundway Stable', (10, 100), LIGHT_BLUE)
            
            render_text(screen, font_normal, 'Entries', (10, 130), GREEN)
            render_text(screen, font_small, 'Ea: %.2f %%' % ((Ea_aux/total_entries)*100), (10, 160), WHITE)
            render_text(screen, font_small, 'Ec: %.2f %%' % ((Ec_aux/total_entries)*100), (10, 180), WHITE)
            render_text(screen, font_small, 'Ee: %.2f %%' % ((Ee_aux/total_entries)*100), (10, 200), WHITE)
            render_text(screen, font_small, 'Eg: %.2f %%' % ((Eg_aux/total_entries)*100), (10, 220), WHITE)

            render_text(screen, font_normal, 'Exits', (10, 250), GREEN)
            render_text(screen, font_small, 'Sb: %.2f %%' % (Sb), (10, 280), WHITE)
            render_text(screen, font_small, 'Sd: %.2f %%' % (Sd), (10, 300), WHITE)
            render_text(screen, font_small, 'Sf: %.2f %%' % (Sf), (10, 320), WHITE)
            render_text(screen, font_small, 'Sh: %.2f %%' % (Sh), (10, 340), WHITE)

            render_text(screen, font_normal, 'Connections', (10, 370), GREEN)
            render_text(screen, font_small, 'X1: %.2f %%' % ((abs(X1)/current_flux)*100), (10, 400), WHITE)
            render_text(screen, font_small, 'X2: %.2f %%' % ((abs(X2)/current_flux)*100), (10, 420), WHITE)
            render_text(screen, font_small, 'X3: %.2f %%' % ((abs(X3)/current_flux)*100), (10, 440), WHITE)
            render_text(screen, font_small, 'X4: %.2f %%' % ((abs(X4)/current_flux)*100), (10, 460), WHITE)
            render_text(screen, font_small, 'X5: %.2f %%' % ((abs(X5)/current_flux)*100), (10, 480), WHITE)
            render_text(screen, font_small, 'X6: %.2f %%' % ((abs(X6)/current_flux)*100), (10, 500), WHITE)
            render_text(screen, font_small, 'X7: %.2f %%' % ((abs(X7)/current_flux)*100), (10, 520), WHITE)
            render_text(screen, font_small, 'X8: %.2f %%' % ((abs(X8)/current_flux)*100), (10, 540), WHITE)

            render_text(screen, font_normal, 'Traffic Lights', (10, 570), GREEN)
            for i in range(len(traffic_lights_red)):
                render_text(screen, font_small, '%s is on red light' % traffic_lights_red[i], (10, 600 + (i*20)), RED)
            for i in range(len(traffic_lights_green)):
                render_text(screen, font_small, '%s is on green light' % traffic_lights_green[i], (10, 600 + (len(traffic_lights_red)+i)*20), GREEN)

            # Draw Button
            draw_button(screen, LIGHT_PURPLE, 275, 15, 200, 50, 'Change', WHITE)
            draw_button(screen, LIGHT_PURPLE, 275, 90, 200, 50, "X8: " + X8_input, WHITE)

        # Update screen
        pg.display.flip()
        clock.tick(FPS)  # Control the frame rate

    pg.quit()
