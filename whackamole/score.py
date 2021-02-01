import pygame as py
from pygame import font, Surface, SRCALPHA


class Score:

    def __init__(self):
        self.hits = 0
        self.misses = 0

    @property
    def score(self):
        return self.hits - self.misses

    @property
    def level(self):
        if self.score < 0:
            return 1
        else:
            return 1 + self.score // 10

    def disp_score(self, timer):
        if (self.hits + self.misses) == 0:
            misses = 0
            hits = 0
        else:
            hits = self.hits / (self.hits + self.misses) * 100
            misses = self.misses / (self.hits + self.misses) * 100

        if timer >= 0:
            text = "Score: {:,.0f} / Hit: {:,} ({:,.1f}%) / Missed: {:,} ({:,.1f}%) / Level: {:,.0f} / Time left: {:,.0f}s".format(
            self.score, self.hits, hits, self.misses, misses, self.level, timer)
        else:
            text = "Score: {:,.0f} / Hit: {:,} ({:,.1f}%) / Missed: {:,} ({:,.1f}%) / Level: {:,.0f} / Time left: 0".format(
            self.score, self.hits, hits, self.misses, misses, self.level)

        return text

    def hit(self):
        self.hits += 1

    def miss(self):
        self.misses += 1
    
    def work_text(self, timer = None, size = 1):
        color = (255, 255, 255)
        string = self.disp_score(timer)
        background = (0, 0, 0, 0.4 * 255)
        font_size = 15 * size
        font = py.font.SysFont("monospace", int(font_size), bold = True)
        line_width = 25
        lines = string.split('/ ')
        labels = []
        
        for line in lines:
            render = font.render(line, 1, color)
            labels.append(render)

        width = max([f.get_width() for f in labels])
        height = 0
        ys = [0]
        for f in labels:
            height += f.get_height() + 3
            ys += [height]

        surface = Surface((width, height), SRCALPHA, 32)
        surface = surface.convert_alpha()
        if background != None:
            surface.fill(background)

        y = 0
        for label in labels:
            surface.blit(label, (0, ys[y]))
            y += 1

        return surface
