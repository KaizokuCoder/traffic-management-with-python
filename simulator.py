import pygame as pg

# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
AQUA = (0, 255, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

def create_arrow_surface(color):
    arrow_surface = pg.Surface((20, 125), pg.SRCALPHA)
    arrow_points = [(10, 0), (20, 20), (12, 20), (12, 125), (8, 125), (8, 20), (0, 20)]
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

def run(values, CAPACITY):
    # Initialize Pygame
    pg.init()
    screen = pg.display.set_mode((1000, 700))

    # Initialize values
    Ae, Be, Ce, De = values[0]
    As, Bs, Cs, Ds = values[1]
    X1, X2, X3, X4 = values[2]

    current_flux = X1 + X2 + X3 + X4
    total_entries = Ae + Be + Ce + De
    total_exits = As + Bs + Cs + Ds

    # Initialize font
    pg.font.init()
    font_big = pg.font.Font(None, 50)  # None for default font
    font_normal = pg.font.Font(None, 30)
    font_small = pg.font.Font(None, 20)

    # Create arrow surfaces
    arrow_north_in = create_arrow_surface(GREEN)
    arrow_north_out = create_arrow_surface(YELLOW)
    arrow_east_in = create_arrow_surface(GREEN)
    arrow_east_out = create_arrow_surface(YELLOW)
    arrow_south_in = create_arrow_surface(GREEN)
    arrow_south_out = create_arrow_surface(YELLOW)
    arrow_west_in = create_arrow_surface(GREEN)
    arrow_west_out = create_arrow_surface(YELLOW)

    arrow_ab = create_arrow_surface(WHITE)
    arrow_bc = create_arrow_surface(WHITE)
    arrow_cd = create_arrow_surface(WHITE)
    arrow_da = create_arrow_surface(WHITE)

        
    # Main loop
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        screen.fill(BLACK)

        # Draw Arrows

        # North
        draw_arrow(screen, arrow_north_out, (635, 125), 0)
        draw_arrow(screen, arrow_north_in, (595, 125), 180)
        # East
        draw_arrow(screen, arrow_east_in, (885, 320), 90)
        draw_arrow(screen, arrow_east_out, (885, 360), -90)
        # South
        draw_arrow(screen, arrow_south_in, (635, 580), 0)
        draw_arrow(screen, arrow_south_out, (595, 580), 180)
        # West
        draw_arrow(screen, arrow_west_in, (345, 370), -90)
        draw_arrow(screen, arrow_west_out, (345, 330), 90)
        # Connections
        draw_arrow(screen, arrow_ab, (715, 280), -125)
        draw_arrow(screen, arrow_bc, (715, 430), 125)
        draw_arrow(screen, arrow_cd, (515, 430), 55)
        draw_arrow(screen, arrow_da, (525, 280), -55)

        # Render text

        # Nodes
        render_text(screen, font_big, 'A', (605, 200), WHITE)
        render_text(screen, font_big, 'B', (785, 330), WHITE)
        render_text(screen, font_big, 'C', (605, 480), WHITE)
        render_text(screen, font_big, 'D', (425, 340), WHITE)

        # Edges - In and Out
        # North
        render_text(screen, font_normal, 'Ae=%.2f' % Ae, (505, 110), GREEN) 
        render_text(screen, font_normal, 'As=%.2f' % As, (650, 110), YELLOW)
        # East
        render_text(screen, font_normal, 'Be=%.2f' % Be, (855, 290), GREEN)
        render_text(screen, font_normal, 'Bs=%.2f' % Bs, (855, 375), YELLOW)
        # South
        render_text(screen, font_normal, 'Ce=%.2f' % Ce, (650, 565), GREEN)
        render_text(screen, font_normal, 'Cs=%.2f' % Cs, (505, 565), YELLOW)
        # West
        render_text(screen, font_normal, 'De=%.2f' % De, (310, 385), GREEN)
        render_text(screen, font_normal, 'Ds=%.2f' % Ds, (310, 300), YELLOW)

        # Edges - Connections
        render_text(screen, font_normal, 'X1=%.2f' % X1, (715, 250), WHITE)
        render_text(screen, font_normal, 'X2=%.2f' % X2, (725, 440), WHITE)
        render_text(screen, font_normal, 'X3=%.2f' % X3, (520, 410), WHITE)
        render_text(screen, font_normal, 'X4=%.2f' % X4, (520, 300), WHITE)

        # Show Data
        render_text(screen, font_normal, 'Roundway Status', (10, 10), AQUA)
        render_text(screen, font_small, 'CAPACITY: %.2f' % CAPACITY, (10, 40), WHITE)
        render_text(screen, font_small, 'FLUX INSIDE: %.2f' % current_flux, (10, 60), WHITE)
        if (X1 + X2 + X3 + X4) > CAPACITY:
            render_text(screen, font_small, 'ROUNDWAY OVERLOADED', (10, 80), RED)
        else:
            render_text(screen, font_small, 'ROUNDWAY ON NORMAL CONDITIONS', (10, 80), GREEN)
        
        render_text(screen, font_normal, 'Entries', (10, 110), AQUA)
        render_text(screen, font_small, 'Ae: %.2f %%' % ((Ae/total_entries)*100), (10, 140), GREEN)
        render_text(screen, font_small, 'Be: %.2f %%' % ((Be/total_entries)*100), (10, 160), GREEN)
        render_text(screen, font_small, 'Ce: %.2f %%' % ((Ce/total_entries)*100), (10, 180), GREEN)
        render_text(screen, font_small, 'De: %.2f %%' % ((De/total_entries)*100), (10, 200), GREEN)

        render_text(screen, font_normal, 'Exits', (10, 230), AQUA)
        render_text(screen, font_small, 'As: %.2f %%' % ((As/total_exits)*100), (10, 260), YELLOW)
        render_text(screen, font_small, 'Bs: %.2f %%' % ((Bs/total_exits)*100), (10, 280), YELLOW)
        render_text(screen, font_small, 'Cs: %.2f %%' % ((Cs/total_exits)*100), (10, 300), YELLOW)
        render_text(screen, font_small, 'Ds: %.2f %%' % ((Ds/total_exits)*100), (10, 320), YELLOW)

        render_text(screen, font_normal, 'Connections', (10, 350), AQUA)
        render_text(screen, font_small, 'X1: %.2f %%' % ((X1/current_flux)*100), (10, 380), WHITE)
        render_text(screen, font_small, 'X2: %.2f %%' % ((X2/current_flux)*100), (10, 400), WHITE)
        render_text(screen, font_small, 'X3: %.2f %%' % ((X3/current_flux)*100), (10, 420), WHITE)
        render_text(screen, font_small, 'X4: %.2f %%' % ((X4/current_flux)*100), (10, 440), WHITE)   

        # Update screen
        pg.display.flip()

    pg.quit()

if __name__ == "__main__":
    run([[10, 30, 15, 25],[7, 18, 38, 17],[16, 7, 16, 11]], 50)