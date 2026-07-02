import pygame

class DummySound:
    def play(self): pass

def load_sounds():
    return DummySound(), DummySound()

def make_shoot_sound():
    return DummySound()

def make_explosion_sound():
    return DummySound()

def make_powerup_sound():
    return DummySound()

def make_boss_hit_sound():
    return DummySound()

def make_hit_sound():
    return DummySound()

