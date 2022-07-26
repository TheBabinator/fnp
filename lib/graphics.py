# some stuff for drawing
# cheers https://ehmatthes.github.io/pcc_2e/beyond_pcc/pygame_sprite_sheets/
import pygame

class SpriteSheet:
    # load the sheet
    def __init__(self, filename):
        self.sheet = pygame.image.load(filename).convert_alpha()

    # load a specific image from a specific rectangle
    def image_at(self, rectangle):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size, pygame.SRCALPHA) # cheers r/dunkler_wanderer
        image.blit(self.sheet, (0, 0), rect)
        return image

class Sprite:
    def __init__(self, game):
        self.image = None
        self.screen = game.screen
        self.x = 0
        self.y = 0
        self.size = None

    def draw(self):
        if self.image != None:
            if self.size == None:
                self.rect = self.image.get_rect()
                self.rect.topleft = self.x, self.y
                self.screen.blit(self.image, self.rect)
            else:
                size = (abs(self.size[0]), abs(self.size[1]))
                self.rect = self.image.get_rect()
                self.rect.topleft = self.x, self.y
                surface = pygame.transform.flip(self.image, self.size[0] < 0, self.size[1] < 0)
                surface = pygame.transform.scale(surface, size)
                self.screen.blit(surface, self.rect)

class Drawer:
    def __init__(self, game):
        self.game = game
        self.numeralsfont = SpriteSheet("assets/gui/font/numerals.png")
        self.ranksfont = SpriteSheet("assets/gui/font/rank.png")
    
    # ive put the function for linear interpolation here because its used for drawing so eh
    def lerp(self, a, b, alpha):
        return a + (b - a) * alpha
    
    # same for the sigmoid function
    # simplified because math
    def sig(self, x):
        if x < -100:
            return 0
        elif x > 100:
            return 1
        else:
            return 1 / (1 + (2.714 ** -x))
    
    # draw a cool rectangle
    def rect(self, color, rectangle):
        rect = pygame.Rect(rectangle)
        surface = pygame.Surface(rect.size)
        surface.fill(color)
        self.game.screen.blit(surface, rect)
    
    # draw some cool numbers
    # id love to annotate this but i honestly dont want to
    def numerals(self, at, number, padleft = None, padright = None):
        display = ""
        parts = (str(number) + ".0").split(".")
        if padleft != None:
            display += ("{:>0" + str(padleft) + "s}").format(parts[0] or "0")
        else:
            display += parts[0] or "0"
        if padright != None:
            display += "."
            display += (parts[1] + "0" * padright)[:padright]
        x = -1
        padded = True
        for char in display:
            x += 1
            sprite = Sprite(self.game)
            if padded and char == "0":
                sprite.image = self.numeralsfont.image_at((168, 0, 14, 18))
            else:
                if char == "-":
                    padded = True
                    sprite.image = self.numeralsfont.image_at((154, 0, 14, 18))
                elif char == ".":
                    padded = False
                    sprite.image = self.numeralsfont.image_at((140, 0, 14, 18))
                else:
                    padded = False
                    sprite.image = self.numeralsfont.image_at((14 * int(char), 0, 14, 18))
            sprite.x = at[0] + x * 14
            sprite.y = at[1]
            sprite.draw()
    
    def rank(self, at, rank):
        sprite = Sprite(self.game)
        sprite.image = self.ranksfont.image_at((28 * rank, 0, 28, 36))
        sprite.x = at[0]
        sprite.y = at[1]
        sprite.draw()
