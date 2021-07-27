import pygame
import time
import numpy
from scipy import interpolate
import math

class LiveLine:
    def __init__(self, data_colors=None, width=1800, height=800, max_abs=10):
        self.width = width
        self.height = height
        self.max_abs = max_abs

        self.data_colors = data_colors or [(0, 244, 244)] * 10

        self.scale = 1.0

        self.data_index = 0
        self.head_index = 0
        self.margin = 100
        self.zero_height = self.height / 2
        self.data_window_n = self.width - self.margin

        self.rate = self.height / 2.0 / self.max_abs * self.scale 

        self.last_data = None
        self.active = True

        self.surface = pygame.Surface((self.width, self.height)).convert_alpha()
        self.rect = pygame.Rect((0, 0, self.width, self.height))

    def update_rate(self):
        self.rate = self.height / 2.0 / self.max_abs * self.scale 

    def process_event(self, event):
        if event.type == pygame.TEXTINPUT:
            if event.text == 'a':
                if self.active == True:
                    self.active = False
                else:
                    self.active = True

            if event.text == 'w':
                self.scale *= 2.0
                self.update_rate()

            if event.text == 's':
                self.scale /= 2.0
                self.update_rate()


    def draw_text(self, x, y, text):
        font = pygame.font.SysFont(None, 24)
        img = font.render('hello', True, (0, 255, 0))
        self.surface.blit(img, (20, 20))

    def draw(self, dest_surface):
        #self.surface.fill((0, 0, 0))
        pygame.draw.rect(self.surface, (0, 0, 0),
                (0, 0, self.margin, self.height), width=0)

        pygame.draw.line(self.surface, (0, 255, 0),
            (self.margin - 1, 0), (self.margin - 1, self.height-1))

        pygame.draw.line(self.surface, (0, 255, 0),
            (0, self.zero_height), (self.width - 1, self.zero_height))


        font = pygame.font.SysFont(None, 34)
        for i in range(1, 5):
            height_offset = self.height / 2.0 / 4.0 * i

            height_offset = int(round(height_offset))

            pygame.draw.line(self.surface, (100, 125, 100),
                (0, self.zero_height + height_offset),
                (self.width - 1, self.zero_height + height_offset))

            pygame.draw.line(self.surface, (100, 125, 100),
                (0, self.zero_height - height_offset),
                (self.width - 1, self.zero_height - height_offset))

            marker_v = self.max_abs / 4.0 * i / self.scale

            img = font.render('%.2f' % marker_v, True, (0, 255, 0))
            self.surface.blit(img, (5, self.zero_height - height_offset))

            img = font.render('-%.2f' % marker_v, True, (0, 255, 0))
            self.surface.blit(img, (5, self.zero_height + height_offset - 20))

        dest_surface.blit(self.surface, self.rect) 

    def feed(self, data):
        self.data_index += 1
        self.head_index = self.data_index % self.data_window_n

        if self.active == False:
            return

        if self.last_data is None:
            self.last_data = data
            return

        if self.head_index == 0:
            return
        
        pygame.draw.rect(self.surface, (0, 0, 0),
                (self.margin + self.head_index, 0, 20, self.height), width=0)

        for i in range(len(data)):
            v = data[i]
            last_v = self.last_data[i]

            color = self.data_colors[i]

            h_off = int(round(v * self.rate))
            last_h_off = int(round(last_v * self.rate))

            pygame.draw.line(self.surface, color,
                (self.margin + self.head_index - 1, self.zero_height - h_off),
                (self.margin + self.head_index, self.zero_height - last_h_off))
        
        self.last_data = data


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1800, 800))
    clock = pygame.time.Clock()

    live_line_obj = LiveLine(data_colors=[(124, 123, 244)])

    i = 0

    running = True
    while running:

        clock.tick(25)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.TEXTINPUT:
                if event.text == 'q':
                    running = False

            live_line_obj.process_event(event)

        v = math.sin(math.pi * 2.0 / 100.0 * i) * 5.0
        i += 1
        live_line_obj.feed([v])
        live_line_obj.draw(screen)

        pygame.display.flip()
