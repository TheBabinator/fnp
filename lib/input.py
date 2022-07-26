# handler for player input
import pygame

class InputController:
    # just a bunch of fields for later use
    def __init__(self):
        # list of lists
        # 0: left, 1: down, 2: up, 3: right
        # 0: active, 1: pressed, 2: released, 3: frames held
        self.arrows = [
            [False, False, False, 0],
            [False, False, False, 0],
            [False, False, False, 0],
            [False, False, False, 0]
        ]
        self.p1arrows = [
            [False, False, False, 0],
            [False, False, False, 0],
            [False, False, False, 0],
            [False, False, False, 0]
        ]
        self.p2arrows = [
            [False, False, False, 0],
            [False, False, False, 0],
            [False, False, False, 0],
            [False, False, False, 0]
        ]
        self.restart = [False, False, False, 0]
    
    # figure out whats going on for a key
    def handlekey(self, li, keys):
        pressed = pygame.key.get_pressed()
        # this bit checks if any of the keys are down
        key = False
        for alias in keys:
            if pressed[alias]:
                key = True
        # this bit does logic
        if key:
            li[0] = True # the key is down
            if li[3] == 0:
                # this is the first frame the key has been held
                li[1] = True
            else:
                # this is not the first frame the key has been held
                li[1] = False
            li[2] = False # the key is not released
            li[3] += 1 # frames since the key has been held
        else:
            li[0] = False # the key is not down
            li[1] = False # the key is still not held down
            if li[3] != 0:
                # this is the first frame the key has been released
                li[2] = True
            else:
                # this is not the first frame the key has been released
                li[2] = False
            li[3] = 0 # reset frames since the key has been held

    # figure it all out idk
    def update(self):
        pressed = pygame.key.get_pressed()
        self.handlekey(self.arrows[0], [pygame.K_LEFT, pygame.K_a, pygame.K_KP4])
        self.handlekey(self.arrows[1], [pygame.K_DOWN, pygame.K_s, pygame.K_KP2])
        self.handlekey(self.arrows[2], [pygame.K_UP, pygame.K_w, pygame.K_KP8])
        self.handlekey(self.arrows[3], [pygame.K_RIGHT, pygame.K_d, pygame.K_KP6])
        self.handlekey(self.p1arrows[0], [pygame.K_a])
        self.handlekey(self.p1arrows[1], [pygame.K_s])
        self.handlekey(self.p1arrows[2], [pygame.K_w])
        self.handlekey(self.p1arrows[3], [pygame.K_d])
        self.handlekey(self.p2arrows[0], [pygame.K_j])
        self.handlekey(self.p2arrows[1], [pygame.K_k])
        self.handlekey(self.p2arrows[2], [pygame.K_i])
        self.handlekey(self.p2arrows[3], [pygame.K_l])
        self.handlekey(self.restart, [pygame.K_r])
        
