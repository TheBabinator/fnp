# stuff for rendering the players
import lib.graphics as graphics

class Actor:
    def __init__(self, game, name):
        self.game = game
        self.path = "assets/actors/" + name + ".png"
        self.sheet = graphics.SpriteSheet(self.path)
        self.sprite = graphics.Sprite(self.game)
        self.flipped = False
        self.x = 0
        self.y = 0
        self.size = (360, 520)
        self.sprite.image = self.sheet.image_at((0, 0, 360, 520))
        self.animating = False
        self.time = 0
    
    # handle animations for playing a note
    def playnote(self, direction):
        if self.flipped:
            if direction == 0:
                direction = 3
            elif direction == 3:
                direction = 0
        self.time = 0.75
        self.sprite.image = self.sheet.image_at((360 + 360 * direction, 0, 360, 520))
        self.animating = True
    
    # update animations or something idk
    def update(self):
        if self.animating:
            self.time = max(self.time - self.game.deltatime, 0)
            if self.time == 0:
                self.sprite.image = self.sheet.image_at((0, 0, 360, 520))
                self.animating = False
    
    # draw the actor to the screen
    def draw(self):
        self.sprite.x = self.x - self.size[0] / 2
        self.sprite.y = self.y - self.size[1]
        if not self.flipped:
            self.sprite.size = self.size
        else:
            self.sprite.size = (-self.size[0], self.size[1])
        self.sprite.draw()
