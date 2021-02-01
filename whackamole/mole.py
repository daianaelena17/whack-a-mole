from random import randint, choice
from pygame import image, transform, time

MOLE_WIDTH = 200
Mole_HEIGTH  = 159
HOLE_WIDTH  = 200
HOLE_HEIGHT  = 45
SPEED = 5
DEPTH = 20
STUNNED = 800
COOL = 500

class Mole:
    def __init__(self):
        self.img_normal = image.load("assets/mole.png")
        self.img_hit = image.load("assets/mole_hit.png")
        self.this_hole = (0, 0)
        self.showing_state = 0
        self.showing_counter = 0
        self.show_time = 0 
        self.show_frame = 0
        self.frames = 8
        self.cooldown = 0
        self.hit = False

    @property
    def get_frame(self):
        return DEPTH / self.frames * (self.frames - self.show_frame)

    def do_display(self, holes, level, do_tick = True):
        if self.cooldown != 0:
            if time.get_ticks() - self.cooldown >= COOL:
                self.cooldown = 0
                return [False, self.this_hole]
            else:
                return [False]
        ret_holes = False
        if do_tick:
            if self.showing_state == 0 and holes:
                self.show_frame = 0
                self.hit = False

                chance = int(3 + (0.3 * level))
                random = randint(0, chance)
                if random == 0:
                    self.showing_state = 1
                    self.showing_counter = 0

                    levelTime = 1 - ((SPEED / 100) * level)
                    timeMin = int(0.3 * 1000 * levelTime)
                    timeMax = int(2 * 1000 * levelTime)
                    self.show_time = randint(timeMin, timeMax)

                    ret_holes = True
                    self.this_hole = choice(holes)
                    
            if self.showing_state == 1 and self.showing_counter != 0 and\
                time.get_ticks() - self.showing_counter >= self.show_time:
                self.showing_state = -1
                self.showing_counter = 0
        if ret_holes == True:
            return [True, self.this_hole, True]
        if self.showing_state == 0:
            return [False]
        return [True]


    def get_hole_pos(self, do_tick = True):

        moleX, holeY = self.this_hole
        offset = (HOLE_WIDTH - MOLE_WIDTH) / 2
        moleY = (holeY + HOLE_HEIGHT) - (Mole_HEIGTH * 1.2)
        
        frame = 0
        if self.hit == True:
            if time.get_ticks() - self.hit < STUNNED:
                do_tick = False
            else:
                self.showing_state = -1
                

        if self.showing_state == 1: # montrer
            if self.show_frame <= self.frames:
                frame = self.get_frame
                if do_tick:
                    self.show_frame += 1
            elif self.showing_counter == 0:
                    self.showing_counter = time.get_ticks()

        elif self.showing_state == -1: # decendre
            
            if do_tick:
                self.show_frame -= 1
                if self.show_frame < 0:
                    self.cooldown = time.get_ticks()

            if self.show_frame < 0:
                self.showing_state = 0
            elif self.show_frame >= 0:
                frame = self.get_frame
            else:
                frame = DEPTH

        return (moleX, moleY + Mole_HEIGTH * (frame / 100))

    def is_dead(self, pos):
        moleX1, moleY1 = self.get_hole_pos(False)
        moleX2, moleY2 = (moleX1 + MOLE_WIDTH, moleY1 + Mole_HEIGTH)

        if pos[0] >= moleX1 and pos[0] <= moleX2 and pos[1] >= moleY1 \
            and pos[1] <= moleY2 and (self.showing_state == 1 or self.showing_state == -1):
            if self.hit == False:
                self.hit = time.get_ticks()
                return 1
            else:
                return 2
        return False
