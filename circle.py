import pygame as pg
import random

class Circle:
    def __init__(self, x, y, speed_x, speed_y, screen_width, screen_height):
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.screen_width = screen_width
        self.screen_height = screen_height

    def update_position(self, radius, fullscreen):
        self.x += self.speed_x
        self.y += self.speed_y
        if self.x + radius >= self.screen_width or self.x - radius <= 0:
            self.speed_x *= -1  # Add randomness to speed_x
        if self.y + radius >= self.screen_height or self.y - radius <= 0:
            self.speed_y *= -1  # Add randomness to speed_y

        # Adjust behavior for fullscreen mode
        if fullscreen:
            self.screen_width, self.screen_height = pg.display.get_surface().get_size()

    def draw(self, surface, color1, color2, radius, is_circle):
        if is_circle:
            pg.draw.circle(surface, color1, (self.x, self.y), radius)
            pg.draw.circle(surface, color1, (self.screen_width - self.x, self.y), radius)

            pg.draw.circle(surface, color2, (self.x, self.y), radius - 10)
            pg.draw.circle(surface, color2, (self.screen_width - self.x, self.y), radius - 10)
        else:
            pg.draw.circle(surface, color1, (self.screen_width / 2, self.screen_height / 2), radius * 16)
            pg.draw.circle(surface, color2, (self.screen_width / 2, self.screen_height / 2), radius * 15)

# Example usage in your main loop:
if __name__ == "__main__":
    screen_width = 960
    screen_height = 540

    # Initialize Pygame
    pg.init()
    screen = pg.display.set_mode((screen_width, screen_height))
    clock = pg.time.Clock()

    circle_radius = 25
    circle_color1 = (255, 0, 0)
    circle_color2 = (0, 255, 0)
    circle_x = screen_width // 2
    circle_y = screen_height // 2
    circle_speed_x = 5
    circle_speed_y = 5
    fullscreen = False
    is_circle = False

    circle = Circle(circle_x, circle_y, circle_speed_x, circle_speed_y, screen_width, screen_height)

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        screen.fill((0, 0, 0))  # Fill the screen with black

        circle.update_position(circle_radius, fullscreen)
        circle.draw(screen, circle_color1, circle_color2, circle_radius, is_circle)

        pg.display.flip()
        clock.tick(60)

    pg.quit()