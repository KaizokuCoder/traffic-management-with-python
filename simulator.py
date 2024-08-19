import pygame as pg

# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 32, 78)
BLUE = (0, 0, 255)
GREEN = (22, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 143, 0)
LIGHT_BLUE = (0, 121, 255)
LIGHT_PURPLE = (124, 0, 254)


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
    screen.blit(rotated_arrow, arrow_rect.topleft)


def draw_circle(screen, pos, radius, color):
    pg.draw.circle(screen, color, pos, radius)


def render_text(screen, font, text, pos, color):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, pos)

def fill_arrow(surface, color):
    mask = pg.mask.from_surface(surface)
    for x in range(surface.get_width()):
        for y in range(surface.get_height()):
            if mask.get_at((x, y)):
                surface.set_at((x, y), color)


def run(values, CAPACITY, X8, traffic_lights1, traffic_lights2):
    # Initialize Pygame
    pg.init()
    screen = pg.display.set_mode((1250, 700))
    pg.display.set_caption("Simulation with FPS Control")
    clock = pg.time.Clock()
    running = True
    FPS = 60  # Set the desired FPS
    frame_counter = 0

    # Initialize values
    Ae, Ce, Ee, Ge = values[0]
    Bs, Ds, Fs, Hs = values[1]

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
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        screen.fill(BLACK)
        
        Ae_aux, Ce_aux, Ee_aux, Ge_aux = Ae, Ce, Ee, Ge

        if set(traffic_lights1) & set(traffic_lights2):
            print("Cycle 2 cannot have the same roads as Cycle 1. Please try again.")
            traffic_lights2 = []
        else:
            if (frame_counter//600) % 2 == 0:
                traffic_lights_red = traffic_lights1
                traffic_lights_green = traffic_lights2
            else:
                traffic_lights_red = traffic_lights2
                traffic_lights_green = traffic_lights1
            if 'Ae' in traffic_lights_red:
                Ae_aux = 0
                fill_arrow(arrow_north_in, RED)
            else:
                fill_arrow(arrow_north_in, GREEN)
            if 'Ce' in traffic_lights_red:
                Ce_aux = 0
                fill_arrow(arrow_east_in, RED)
            else:
                fill_arrow(arrow_east_in, GREEN)
            if 'Ee' in traffic_lights_red:
                Ee_aux = 0
                fill_arrow(arrow_south_in, RED)
            else:
                fill_arrow(arrow_south_in, GREEN)
            if 'Ge' in traffic_lights_red:
                Ge_aux = 0
                fill_arrow(arrow_west_in, RED)
            else:
                fill_arrow(arrow_west_in, GREEN)
        
        
        # Update Values
        X1 = Ae_aux + X8
        X2 = -Bs + Ae_aux + X8
        X3 = Ce_aux - Bs + Ae_aux + X8
        X4 = -Ds + Ce_aux - Bs + Ae_aux + X8
        X5 = Ee_aux - Ds + Ce_aux - Bs + Ae_aux + X8
        X6 = -Fs + Ee_aux - Ds + Ce_aux - Bs + Ae_aux + X8
        X7 = Ge_aux - Fs + Ee_aux - Ds + Ce_aux - Bs + Ae_aux + X8

        current_flux = X1 + X2 + X3 + X4 + X5 + X6 + X7 + X8
        total_entries = Ae + Ce + Ee + Ge
        total_exits = Bs + Ds + Fs + Hs
        overloaded = current_flux > CAPACITY # True if the roundway is overloaded

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
        draw_arrow(screen, arrow_ab, (715, 145), -90)
        draw_arrow(screen, arrow_bc, (890, 190), -125)
        draw_arrow(screen, arrow_cd, (962, 340), 180)
        draw_arrow(screen, arrow_de, (885, 495), 125)
        draw_arrow(screen, arrow_ef, (710, 548), 90)
        draw_arrow(screen, arrow_fg, (540, 495), 55)
        draw_arrow(screen, arrow_gh, (467, 345), 0)
        draw_arrow(screen, arrow_ha, (538, 195), -55)

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
        render_text(screen, font_small, 'Ae: %d' % Ae_aux, (620, 60), RED if 'Ae' in traffic_lights_red else GREEN)
        render_text(screen, font_small, 'Bs: %d' % Bs, (825, 60), ORANGE)
        render_text(screen, font_small, 'Ce: %d' % Ce_aux, (1025, 215), RED if 'Ce' in traffic_lights_red else GREEN)
        render_text(screen, font_small, 'Ds: %d' % Ds, (1005, 415), ORANGE)
        render_text(screen, font_small, 'Ee: %d' % Ee_aux, (820, 615), RED if 'Ee' in traffic_lights_red else GREEN)
        render_text(screen, font_small, 'Fs: %d' % Fs, (620, 615), ORANGE)
        render_text(screen, font_small, 'Ge: %d' % Ge_aux, (360, 415), RED if 'Ge' in traffic_lights_red else GREEN)
        render_text(screen, font_small, 'Hs: %d' % Hs, (370, 215), ORANGE)



        # Show Data
        render_text(screen, font_normal, 'Roundway Status', (10, 10), GREEN)
        render_text(screen, font_small, 'capacity: %d' % CAPACITY, (10, 40), WHITE)
        render_text(screen, font_small, 'flux inside: %d' % current_flux, (10, 60), WHITE)
        if (overloaded):
            render_text(screen, font_small, 'Roundway Overloaded', (10, 80), RED)
        else:
            render_text(screen, font_small, 'Roundway Stable', (10, 80), LIGHT_BLUE)
        
        render_text(screen, font_normal, 'Entries', (10, 110), GREEN)
        render_text(screen, font_small, 'Ae: %.2f %%' % ((Ae/total_entries)*100), (10, 140), WHITE)
        render_text(screen, font_small, 'Ce: %.2f %%' % ((Ce/total_entries)*100), (10, 160), WHITE)
        render_text(screen, font_small, 'Ee: %.2f %%' % ((Ee/total_entries)*100), (10, 180), WHITE)
        render_text(screen, font_small, 'Ge: %.2f %%' % ((Ge/total_entries)*100), (10, 200), WHITE)

        render_text(screen, font_normal, 'Exits', (10, 230), GREEN)
        render_text(screen, font_small, 'Bs: %.2f %%' % ((Bs/total_exits)*100), (10, 260), WHITE)
        render_text(screen, font_small, 'Ds: %.2f %%' % ((Ds/total_exits)*100), (10, 280), WHITE)
        render_text(screen, font_small, 'Fs: %.2f %%' % ((Fs/total_exits)*100), (10, 300), WHITE)
        render_text(screen, font_small, 'Hs: %.2f %%' % ((Hs/total_exits)*100), (10, 320), WHITE)

        render_text(screen, font_normal, 'Connections', (10, 350), GREEN)
        render_text(screen, font_small, 'X1: %.2f %%' % ((X1/current_flux)*100), (10, 380), WHITE)
        render_text(screen, font_small, 'X2: %.2f %%' % ((X2/current_flux)*100), (10, 400), WHITE)
        render_text(screen, font_small, 'X3: %.2f %%' % ((X3/current_flux)*100), (10, 420), WHITE)
        render_text(screen, font_small, 'X4: %.2f %%' % ((X4/current_flux)*100), (10, 440), WHITE)
        render_text(screen, font_small, 'X5: %.2f %%' % ((X5/current_flux)*100), (10, 460), WHITE)
        render_text(screen, font_small, 'X6: %.2f %%' % ((X6/current_flux)*100), (10, 480), WHITE)
        render_text(screen, font_small, 'X7: %.2f %%' % ((X7/current_flux)*100), (10, 500), WHITE)
        render_text(screen, font_small, 'X8: %.2f %%' % ((X8/current_flux)*100), (10, 520), WHITE)

        render_text(screen, font_normal, 'Traffic Lights', (10, 550), GREEN)
        for  i in range(len(traffic_lights_red)):
            render_text(screen, font_small, '%s is on red light' % traffic_lights_red[i], (10, 580 + (i*20)), RED)
        for  i in range(len(traffic_lights_green)):
            render_text(screen, font_small, '%s is on green light' % traffic_lights_green[i], (10, 580 + (len(traffic_lights_red)+i)*20), GREEN)

        # Update screen
        pg.display.flip()
        clock.tick(FPS)  # Control the frame rate
        frame_counter += 1

    pg.quit()

if __name__ == "__main__":
    run([[27, 63, 48, 82],[35, 52, 68, 65],[48, 13, 76, 24, 72, 4, 86, 21],[]], 150)