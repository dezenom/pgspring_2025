import pygame
from time import time
from random import randint

# not integrated

class Radio():
    def __init__(self,Musics = list,Soundeffects = dict) :
        self.SOUNDEFFECTS = Soundeffects
        self.MUSICS = Musics
        self.music_channel = pygame.mixer.Channel(0)
        self.music_channel.set_volume(0.1)
        self.effects_channel = pygame.mixer.Channel(1)
        self.effects_channel.set_volume(0.2)

        self.current_time = time()
        self.start_time = self.current_time

        self.randmusic = randint(0,len(self.MUSICS)-1)

        self.music_channel.play(self.MUSICS[self.randmusic])

    def play_music(self):
        self.current_time = time()
        if self.MUSICS[self.randmusic].get_length() - (self.current_time-self.start_time) < -3:
            self.start_time = time()
            self.randmusic = randint(0,len(self.MUSICS)-1)
            self.music_channel.play(self.MUSICS[self.randmusic])

    def play_effect(self,effect_name):
        self.effects_channel.play(self.SOUNDEFFECTS[effect_name])
