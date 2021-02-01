from pygame import init, quit, display, image, transform, time, mouse, event, Surface, QUIT, MOUSEBUTTONDOWN, KEYDOWN, K_SPACE

from .mole import Mole
from .score import Score

GAME_WIDTH     = 960
GAME_HEIGHT      = 540
FPS      = 60

class Game:
    def __init__(self, timer):
        init()
        self.screen = display.set_mode((GAME_WIDTH, GAME_HEIGHT))
        display.set_caption("Whack a MOLE")
        self.img_bg = image.load("assets/background.png")
        self.img_hole = image.load("assets/hole.png")
        self.img_hammer = image.load("assets/mallet.png")
        self.img_bang = image.load("assets/bang.png")
        self.img_oops = image.load("assets/oops.png")
        self.img_click = image.load("assets/click.png")
        self.img_space = image.load("assets/space.png")
        self.img_night = image.load("assets/night.png")
        self.img_sunset = image.load("assets/sunset.png")
        self.img_night = transform.scale(self.img_night, (GAME_WIDTH, GAME_HEIGHT))
        self.img_sunset = transform.scale(self.img_sunset, (GAME_WIDTH, GAME_HEIGHT))
        self.img_space = transform.scale(self.img_space, (GAME_WIDTH, GAME_HEIGHT))
        self.img_click = transform.scale(self.img_click, (GAME_WIDTH, GAME_HEIGHT))
        self.img_hole = transform.scale(self.img_hole, (200, 45))
        self.img_hammer = transform.scale(self.img_hammer, (200, 200))
        self.img_bang = transform.scale(self.img_bang, (150, 150))
        self.img_oops = transform.scale(self.img_oops, (150, 150))
        self.img_hammer_hit = transform.rotate(self.img_hammer.copy(), 35)
        self.img_hammer_norm = transform.rotate(self.img_hammer.copy(), 10)
        self.timer = timer
        self.fixed_timer = timer
        self.reset()
        self.run()

    def reset(self):
        self.holes = []
        self.used_holes = []
        self.moles = []
        for _ in range(3):
            self.moles += [Mole()]

        base_column = GAME_WIDTH / 3
        
        for column in range(3):
            thisX = base_column * column
            thisX += (base_column - 200) / 2
            self.holes.append((int(thisX), int(400)))

        self.score = Score()
        self.show_hit = 0
        self.show_miss = 0
        self.timer_start = 0

    def events(self):
        miss = False
        clicked = False
        hit= False
        pos = mouse.get_pos()

        for e in event.get():
            is_end = False
            if self.timer_start != 0:
                remain = self.timer - (time.get_ticks() - self.timer_start) / 1000
                if remain <= 0:
                    is_end = True

            if is_end == False:

                if e.type == MOUSEBUTTONDOWN and e.button == 1:
                    if self.timer_start == 0:
                        self.timer_start = time.get_ticks()
                    else:
                        miss = True
                        for mole in self.moles:
                            if mole.is_dead(pos) == 1:  # Hit gen Dead
                                hit = True
                                miss = False
                                self.bang_position = pos
                            if mole.is_dead(pos) == 2:  # Stunned
                                miss = False
                        self.oops_position = pos
                        if hit == True:
                            self.score.hit()
                        elif miss == True:
                            self.score.miss()
                        clicked = True
            else:
                if e.type == KEYDOWN:
                    if e.key == K_SPACE:
                        self.reset()
                        break

            if e.type == QUIT:
                self.loop = False
                break

        return (clicked, hit, miss)

    def draw(self, clicked, hit, miss):
        is_end = False
        this_time = None

        if self.timer_start != 0:
            remain = self.timer - (time.get_ticks() - self.timer_start) / 1000
            this_time = remain
            if remain <= 0:
                is_end = True
            
        if this_time is None and self.timer is not None:
            this_time = 0

        if (self.fixed_timer // 2) < this_time:
            self.screen.blit(self.img_bg, (0, 0))
        elif (self.fixed_timer // 2) > this_time > (self.fixed_timer // 4):
            self.screen.blit(self.img_sunset, (0, 0))
        else:
            self.screen.blit(self.img_night, (0, 0))
        
        for position in self.holes:
            self.screen.blit(self.img_hole, position)

        for mole in self.moles:
            holes = []
            for f in self.holes:
                if f not in self.used_holes:
                    holes.append(f)

            mole_display = mole.do_display(holes, self.score.level, not is_end)
            
            if len(mole_display) == 2:
                self.used_holes.remove(mole_display[1])
            if len(mole_display) == 3:
                self.used_holes.append(mole_display[1])

            if mole_display[0]:
                pos = mole.get_hole_pos(not is_end)
                if mole.hit != False:
                    self.screen.blit(mole.img_hit, pos)
                else:
                    self.screen.blit(mole.img_normal, pos)

        hammer_x, hammer_y = mouse.get_pos()
        hammer_x -= 40
        hammer_y -= 50
        if clicked:
            self.screen.blit(self.img_hammer_hit, (hammer_x, hammer_y))
        else:
            self.screen.blit(self.img_hammer_norm, (hammer_x, hammer_y))

        data = self.score.work_text(timer = this_time, size = 1) # score after finish
        self.screen.blit(data, (5, 5))

        if is_end ==  False:

            if hit == True: # got him :)
                self.show_hit = time.get_ticks()
            if self.show_hit > 0 and time.get_ticks() - self.show_hit <= 500:
                self.screen.blit(self.img_bang, (self.bang_position[0] - 50, self.bang_position[1] - 50))
            else:
                self.show_hit = 0

           
            if miss == True: # missed him :(
                self.show_miss = time.get_ticks()
            if self.show_miss > 0 and time.get_ticks() - self.show_miss <= 250:
                self.screen.blit(self.img_oops, (self.oops_position[0] - 50, self.oops_position[1] - 50))
            else:
                self.show_miss = 0

        if self.timer and this_time == 0:
            self.screen.blit(self.img_click, (0, 0))

        if self.timer and is_end: # time's up
            self.screen.blit(self.img_space, (0, 0))
            data = self.score.work_text(timer = this_time, size = 1.5)
            self.screen.blit(data, (5, 5))

    def start(self):
        self.clock = time.Clock()
        self.loop = True

        while self.loop == True:
            self.draw(*self.events())
            self.clock.tick(FPS)
            
            display.flip()

    def run(self):
        self.start()
        quit()

