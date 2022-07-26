# some stuff for playing the game
import math
import lib.graphics as graphics
import lib.actor as actor

class Control:
    # load some assets and that
    def __init__(self, game, track):
        self.game = game
        self.track = track
        self.paused = False
        self.time = -9 / (self.track.bpm / 60)
        self.beattime = -9
        self.introstate = 0
        self.score = 0
        self.health = 0.5
        self.combo = 0
        self.multiplier = 0
        self.hits = 0
        self.misses = 0
        self.rawscore = 0
        self.maxrawscore = 0
        self.accuracy = 0
        self.rank = 0

        # arrow sheet
        self.sheet = graphics.SpriteSheet("assets/gui/arrows.png")

        # player 1 buttons
        self.p1buttons = graphics.Sprite(self.game)
        self.p1buttons.image = self.sheet.image_at((0, 0, 512, 128))
        self.p1buttons.x = 32
        self.p1buttons.y = 32

        # player 2 buttons
        self.p2buttons = graphics.Sprite(self.game)
        self.p2buttons.image = self.sheet.image_at((0, 0, 512, 128))
        self.p2buttons.x = self.game.width - 544
        self.p2buttons.y = 32

        # player 2 button higlights
        # 4 buttons from 0-3
        self.p2pressed = []
        for i in range(4):
            sprite = graphics.Sprite(self.game)
            sprite.image = self.sheet.image_at((128 * i, 128, 128, 128))
            sprite.x = (self.game.width - 544) + (128 * i)
            sprite.y = 32
            self.p2pressed.append(sprite)

        # player 1 notes
        self.p1notes = []
        for note in self.track.p1notes:
            sprite = graphics.Sprite(self.game)
            sprite.image = self.sheet.image_at((128 * note[1], 256, 128, 128))
            self.p1notes.append((note, sprite))

        # player 2 notes
        self.p2notes = []
        for note in self.track.p2notes:
            sprite = graphics.Sprite(self.game)
            sprite.image = self.sheet.image_at((128 * note[1], 256, 128, 128))
            self.p2notes.append((note, sprite))
        
        # countdown images
        self.countdownsheet = graphics.SpriteSheet("assets/gui/countdown.png")
        self.countdown = graphics.Sprite(self.game)
        self.countdown.x = self.game.width / 2 - 400
        self.countdown.y = self.game.height / 2 - 150
        
        # load scene
        self.scenebgsheet = graphics.SpriteSheet(self.track.scene + "/background.png")
        self.scenebg = graphics.Sprite(self.game)
        self.scenebg.image = self.scenebgsheet.image_at((0, 0, 1280, 720))
        
        # load actors
        self.p1 = actor.Actor(self.game, self.track.p1)
        self.p1.flipped = True
        self.p2 = actor.Actor(self.game, self.track.p2)
        
        # load song
        self.game.sound.loadsound(self.track.name + "-inst", self.track.path + "/inst.ogg")
        self.game.sound.loadsound(self.track.name + "-voices", self.track.path + "/voices.ogg")
        self.inst = self.game.sound.playsound(self.track.name + "-inst")
        self.voices = self.game.sound.playsound(self.track.name + "-voices")
        self.inst.pause()
        self.voices.pause()

    # stop everything
    def kill(self):
        self.paused = True
        self.inst.stop()
        self.voices.stop()
    
    # do the gaming
    def update(self):
        if not self.paused:
            # update actors
            self.p1.update()
            self.p2.update()
            
            # get what beat we on
            self.time += self.game.deltatime
            self.beattime = self.time * (self.track.bpm / 60)
            
            # intro sequence
            if self.introstate != -1:
                if self.introstate == 0:
                    if self.beattime > -4:
                        print("three")
                        self.introstate = 1
                        self.countdown.image = self.countdownsheet.image_at((0, 0, 800, 300))
                elif self.introstate == 1:
                    if self.beattime > -3:
                        print("two")
                        self.introstate = 2
                        self.countdown.image = self.countdownsheet.image_at((0, 300, 800, 300))
                elif self.introstate == 2:
                    if self.beattime > -2:
                        print("one")
                        self.introstate = 3
                        self.countdown.image = self.countdownsheet.image_at((0, 600, 800, 300))
                elif self.introstate == 3:
                    if self.beattime > -1:
                        print("go!")
                        self.introstate = 4
                        self.countdown.image = self.countdownsheet.image_at((0, 900, 800, 300))
                elif self.introstate == 4:
                    if self.beattime > 0:
                        self.introstate = -1
                        self.countdown.image = None
                        self.inst.resume()
                        self.voices.resume()

            # player 1 as the computer will automatically play their notes
            # once they are due we remove them from the incoming list as if they have been played
            if len(self.p1notes) != 0:
                note = self.p1notes[0][0]
                if self.beattime > note[0]:
                    self.p1notes.pop(0)
                    self.voices.volume(1)
                    self.p1.playnote(note[1])
            
            # player 2 as the player should play their notes
            # however if they are overdue it is a miss
            playing = [False, False, False, False]
            playingatall = False
            validnotes = [False, False, False, False]
            validnotesatall = False
            # see if the player is playing any notes
            for i in range(4):
                if self.game.input.arrows[i][1]:
                    playing[i] = True
                    playingatall = True
            # go through all notes
            canplay = [True, True, True, True]
            played = []
            for note in self.p2notes:
                data = note[0]
                allowance = 0.14 * (self.track.bpm / 60)
                # only bother with the notes that are within the "allowance" range
                if self.beattime > data[0] - allowance:
                    validnotes[data[1]] = True
                    validnotesatall = True
                    if playing[data[1]] and canplay[data[1]]:
                        # if the player hit the notes...
                        beatinnacuracy = abs(self.beattime - data[0])
                        innacuracy = beatinnacuracy / (self.track.bpm / 60)
                        played.append(note)
                        self.voices.volume(1)
                        if innacuracy < 0.05:
                            self.rawscore += 350
                            self.score += math.floor(350 * self.multiplier)
                            self.health += 0.0175
                        elif innacuracy < 0.09:
                            self.rawscore += 200
                            self.score += math.floor(200 * self.multiplier)
                            self.health += 0.01
                        elif innacuracy < 0.12:
                            self.rawscore += 100
                            self.score += math.floor(100 * self.multiplier)
                            self.health += 0.005
                        else:
                            self.rawscore += 50
                            self.score += math.floor(50 * self.multiplier)
                            self.health += 0.0025
                        self.combo += 1
                        self.hits += 1
                        self.maxrawscore += 350
                        self.p2.playnote(data[1])
                        canplay[data[1]] = False
                    elif self.beattime > data[0] + allowance:
                        # if the player didn't hit the notes...
                        played.append(note)
                        self.voices.volume(0)
                        self.rawscore -= 50
                        self.score -= 50
                        self.health -= 0.06 * self.track.damagemultiplier
                        self.combo = 0
                        self.misses += 1
                        self.maxrawscore += 350
            # remove the notes from the list AFTERWARDS because otherwise problems
            for note in played:
                self.p2notes.remove(note)
            # if there are no notes to be played...
            for i in range(4):
                if not validnotes[i]:
                    if playing[i]:
                        # but the player is still playing notes...
                        self.rawscore -= 50
                        self.score -= 50
                        self.health -= 0.015 * self.track.damagemultiplier
                        self.combo = 0
                        self.misses += 1
            if not validnotesatall:
                if playingatall:
                    self.voices.volume(0)
                else:
                    self.voices.volume(1)
            # stat stuff
            if self.combo != 0:
                self.multiplier = (math.log(self.combo, 10) + 1) ** 2
            else:
                self.multiplier = 1
            if self.hits > 0:
                self.accuracy = max(self.rawscore / self.maxrawscore, 0)
                if self.accuracy > 0.99:
                    self.rank = 5
                elif self.accuracy > 0.975:
                    self.rank = 4
                elif self.accuracy > 0.95:
                    self.rank = 3
                elif self.accuracy > 0.8:
                    self.rank = 2
                else:
                    self.rank = 1
            # health stuff
            self.health = min(max(self.health, 0), 1)
            if self.health == 0:
                print("death")
                self.kill()
            elif self.beattime > self.track.beatlength:
                print("victory")
                self.kill()
    
    # draw everything to the screen
    def draw(self):
        # scene
        signaturetime = (self.beattime / self.track.signature) % 1
        zoom = max(self.game.drawer.lerp(1.05, 0.9, signaturetime), 1)
        
        self.scenebg.x = (1280 - (1280 * zoom)) / 2
        self.scenebg.y = (720 - (720 * zoom)) / 2
        self.scenebg.size = (int(1280 * zoom), int(720 * zoom))
        self.scenebg.draw()
        
        # actors
        self.p1.x = self.game.drawer.lerp(self.game.width / 2, 300, zoom)
        self.p1.y = self.game.drawer.lerp(self.game.height / 2, self.game.height - 80, zoom)
        self.p1.size = (int(360 * zoom), int(520 * zoom))
        self.p1.draw()
        self.p2.x = self.game.drawer.lerp(self.game.width / 2, self.game.width - 300, zoom)
        self.p2.y = self.game.drawer.lerp(self.game.height / 2, self.game.height - 80, zoom)
        self.p2.size = (int(360 * zoom), int(520 * zoom))
        self.p2.draw()
        
        # buttons
        self.p1buttons.draw()
        self.p2buttons.draw()

        # player 2 button highlights
        # 4 buttons from 0-3
        for i in range(4):
            if self.game.input.arrows[i][0]:
                self.p2pressed[i].draw()

        # player 1 notes
        for note in self.p1notes:
            note[1].x = 32 + 128 * note[0][1]
            note[1].y = 32 + (note[0][0] - self.beattime) * self.track.speed
            if note[1].y < self.game.height:
                note[1].draw()

        # player 2 notes
        for note in self.p2notes:
            note[1].x = self.game.width - 544 + 128 * note[0][1]
            note[1].y = 32 + (note[0][0] - self.beattime) * self.track.speed
            if note[1].y < self.game.height:
                note[1].draw()
        
        # health bar
        self.game.drawer.rect((0, 0, 0), (295, self.game.height - 70, self.game.width - 590, 25))
        self.game.drawer.rect((0, 255, 0), (300, self.game.height - 65, self.game.width - 600, 15))
        self.game.drawer.rect((255, 0, 0), (300, self.game.height - 65, self.game.drawer.lerp(self.game.width - 600, 0, self.health), 15))
        self.game.drawer.numerals((305, self.game.height - 90), self.score, 8)
        self.game.drawer.numerals((305, self.game.height - 110), self.combo, 3)
        self.game.drawer.numerals((361, self.game.height - 110), self.multiplier, 2, 1)
        self.game.drawer.numerals((505, self.game.height - 90), self.health * 100, 3, 2)
        self.game.drawer.numerals((505, self.game.height - 110), self.accuracy * 100, 3, 2)
        self.game.drawer.rank((470, self.game.height - 109), self.rank)
        self.game.drawer.numerals((605, self.game.height - 90), float(str(math.floor(self.beattime / self.track.signature + 1)) + "." + str(math.floor(self.beattime % self.track.signature + 1))), 3, 1)
        
        # countdown
        if self.introstate != -1:
            self.countdown.draw()


