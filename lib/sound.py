# some stuff for playing sound
import pygame

class SoundController:
    def __init__(self):
        self.sounds = {}
    
    def loadsound(self, name, filename):
        if not name in self.sounds:
            sound = pygame.mixer.Sound(filename)
            self.sounds[name] = sound
    
    def playsound(self, name):
        channel = self.sounds[name].play()
        sound = PlayingSound(channel)
        return sound

class PlayingSound:
    def __init__(self, channel):
        self.channel = channel
    
    def play(self):
        self.channel.play()
    
    def stop(self, time = 0):
        if time != 0:
            self.channel.fadeout(time)
        else:
            self.channel.stop()
    
    def pause(self):
        self.channel.pause()
    
    def resume(self):
        self.channel.unpause()
    
    def volume(self, volume):
        self.channel.set_volume(volume)
