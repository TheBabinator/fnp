# the game
# cheers to pygame documentation
# original at https://uploads.ungrounded.net/alternate/1528000/1528775_alternate_113347_r88.zip/?NewgroundsAPI_PublisherID=1&NewgroundsAPI_SandboxID=609b03e749a28&NewgroundsAPI_SessionID=&NewgroundsAPI_UserName=%26lt%3Bdeleted%26gt%3B&NewgroundsAPI_UserID=0&ng_username=%26lt%3Bdeleted%26gt%3B
# also on http://v6p9d9t4.ssl.hwcdn.net/html/2876359-359162/index.html
# also on https://w8.snokido.com/games/html5/friday-night-funkin/0281/
import sys
import traceback
import pygame
import lib.graphics as graphics
import lib.sound as sound
import lib.control as control
import lib.pvpcontrol as pvpcontrol
import lib.input as user
import lib.track as track

class Game:
    # initialise the game and create resources
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        pygame.init()
        pygame.mixer.init(44100)
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("friday night python")

        self.deltatime = 0
        self.tickslastframe = 0
        
        self.drawer = graphics.Drawer(self)
        self.sound = sound.SoundController()
        self.input = user.InputController()
        self.control = None
        
        self.instructions = graphics.Sprite(self)
        self.instructions.image = graphics.SpriteSheet("assets/gui/instructions.png").image_at((0, 0, 1280, 720))
        

    # runs every frame
    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        self.input.update()
        if self.control:
            self.control.update()
        if self.input.restart[1]:
            if self.control:
                self.control.kill()
            test = track.Track("megalofunkia")
            self.control = control.Control(self, test)

    # draws the game after update
    def draw(self):
        self.screen.fill((50, 50, 50))

        self.instructions.draw()
        if self.control:
            self.control.draw()
        
        pygame.display.flip()

    # starts the main loop
    def run(self):
        clock = pygame.time.Clock()
        while True:
            t = pygame.time.get_ticks()
            self.deltatime = (t - self.tickslastframe) / 1000 # keeps track of delta time
            
            self.update()
            self.draw()
            
            self.tickslastframe = t
            clock.tick(144)

game = Game(1280, 720)
game.run()
