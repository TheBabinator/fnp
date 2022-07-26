# some stuff for playing the game (but pvp)
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
        self.p1score = 0
        self.p1maxscore = 0
        self.p1accuracy = 0
        self.p2score = 0
        self.p2maxscore = 0
        self.p2accuracy = 0

        # arrow sheet
        self.sheet = graphics.SpriteSheet("assets/gui/arrows.png")

        # player 1 buttons
        self.p1buttons = graphics.Sprite(self.game)
        self.p1buttons.image = self.sheet.image_at((0, 0, 512, 128))
        self.p1buttons.x = 32
        self.p1buttons.y = 32
        self.p1pressed = []
        for i in range(4):
            sprite = graphics.Sprite(self.game)
            sprite.image = self.sheet.image_at((128 * i, 128, 128, 128))
            sprite.x = 32 + (128 * i)
            sprite.y = 32
            self.p1pressed.append(sprite)

        # player 2 buttons
        self.p2buttons = graphics.Sprite(self.game)
        self.p2buttons.image = self.sheet.image_at((0, 0, 512, 128))
        self.p2buttons.x = self.game.width - 544
        self.p2buttons.y = 32
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
            
            # --- HANDLE NOTE INPUT ---
            playingatall = False
            validnotesatall = False
            
            # player 1
            playing = [False, False, False, False]
            validnotes = [False, False, False, False]
            # see if the player is playing any notes
            for i in range(4):
                if self.game.input.p1arrows[i][1]:
                    playing[i] = True
                    playingatall = True
            # go through all notes
            canplay = [True, True, True, True]
            played = []
            for note in self.p1notes:
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
                        #self.voices.volume(1)
                        if innacuracy < 0.05:
                            self.p1score += 350
                        elif innacuracy < 0.09:
                            self.p1score += 200
                        elif innacuracy < 0.12:
                            self.p1score += 100
                        else:
                            self.p1score += 50
                        self.p1maxscore += 350
                        self.p1.playnote(data[1])
                        canplay[data[1]] = False
                    elif self.beattime > data[0] + allowance:
                        # if the player didn't hit the notes...
                        played.append(note)
                        #self.voices.volume(0)
                        self.p1score -= 50
                        self.p1maxscore += 350
            # remove the notes from the list AFTERWARDS because otherwise problems
            for note in played:
                self.p1notes.remove(note)
            # if there are no notes to be played...
            for i in range(4):
                if not validnotes[i]:
                    if playing[i]:
                        # but the player is still playing notes...
                        self.p1score -= 50
            
            # player 2
            playing = [False, False, False, False]
            validnotes = [False, False, False, False]
            # see if the player is playing any notes
            for i in range(4):
                if self.game.input.p2arrows[i][1]:
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
                        #self.voices.volume(1)
                        if innacuracy < 0.05:
                            self.p2score += 350
                        elif innacuracy < 0.09:
                            self.p2score += 200
                        elif innacuracy < 0.12:
                            self.p2score += 100
                        else:
                            self.p2score += 50
                        self.p2maxscore += 350
                        self.p2.playnote(data[1])
                        canplay[data[1]] = False
                    elif self.beattime > data[0] + allowance:
                        # if the player didn't hit the notes...
                        played.append(note)
                        #self.voices.volume(0)
                        self.p2score -= 50
                        self.p2maxscore += 350
            # remove the notes from the list AFTERWARDS because otherwise problems
            for note in played:
                self.p2notes.remove(note)
            # if there are no notes to be played...
            for i in range(4):
                if not validnotes[i]:
                    if playing[i]:
                        # but the player is still playing notes...
                        self.p2score -= 50
            
            #if not validnotesatall:
            #    if playingatall:
            #        self.voices.volume(0)
            #    else:
            #        self.voices.volume(1)
            
            # --- END HANDLE NOTE INPUT ---
            
            # accuracy
            if self.p1maxscore > 0:
                self.p1accuracy = max(self.p1score / self.p1maxscore, 0)
            if self.p2maxscore > 0:
                self.p2accuracy = max(self.p2score / self.p2maxscore, 0)
            
            # song ending
            if self.beattime > self.track.beatlength:
                print("ende")
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
        for i in range(4):
            if self.game.input.p1arrows[i][0]:
                self.p1pressed[i].draw()
        for i in range(4):
            if self.game.input.p2arrows[i][0]:
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
        self.game.drawer.rect((255, 0, 0), (300, self.game.height - 65, self.game.drawer.lerp(0, self.game.width - 600, self.game.drawer.sig((self.p1score - self.p2score) / 2000)), 15))
        self.game.drawer.numerals((305, self.game.height - 110), self.p1score, 8)
        self.game.drawer.numerals((425, self.game.height - 110), self.p1accuracy * 100, 3, 2)
        self.game.drawer.numerals((305, self.game.height - 90), self.p2score, 8)
        self.game.drawer.numerals((425, self.game.height - 90), self.p2accuracy * 100, 3, 2)
        self.game.drawer.numerals((605, self.game.height - 90), float(str(math.floor(self.beattime / self.track.signature + 1)) + "." + str(math.floor(self.beattime % self.track.signature + 1))), 3, 1)
        
        # countdown
        if self.introstate != -1:
            self.countdown.draw()


