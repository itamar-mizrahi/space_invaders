import pygame
import numpy as np

SAMPLE_RATE = 44100
pygame.mixer.init(frequency=SAMPLE_RATE, size=-16, channels=2, buffer=512)

def _make_sound(samples):
    samples = np.clip(samples, -32767, 32767).astype(np.int16)
    # pygame-ce stereo mixer needs shape (n, 2)
    stereo = np.column_stack([samples, samples])
    sound = pygame.sndarray.make_sound(stereo)
    return sound

def _sine(freq, duration, volume=0.3, sample_rate=SAMPLE_RATE):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = (np.sin(2 * np.pi * freq * t) * volume * 32767)
    return wave

def _noise(duration, volume=0.3, sample_rate=SAMPLE_RATE):
    n = int(sample_rate * duration)
    wave = (np.random.uniform(-1, 1, n) * volume * 32767)
    return wave

def _envelope(wave, attack=0.01, decay=0.1, sample_rate=SAMPLE_RATE):
    n = len(wave)
    env = np.ones(n)
    a = int(attack * sample_rate)
    d = int(decay * sample_rate)
    if a > 0:
        env[:a] = np.linspace(0, 1, a)
    end = min(n, a + d)
    if end > a:
        env[a:end] = np.linspace(1, 0, end - a)
    env[end:] = 0
    return wave * env

# Shoot: short "pew" - descending sine
def make_shoot_sound():
    t = np.linspace(0, 0.12, int(SAMPLE_RATE * 0.12), endpoint=False)
    freq = np.linspace(900, 200, len(t))
    wave = np.sin(2 * np.pi * freq * t) * 0.25 * 32767
    wave = _envelope(wave, attack=0.005, decay=0.115)
    return _make_sound(wave)

# Explosion: burst of noise
def make_explosion_sound():
    wave = _noise(0.25, volume=0.4)
    wave = _envelope(wave, attack=0.005, decay=0.24)
    return _make_sound(wave)

# Power-up: ascending chime
def make_powerup_sound():
    w1 = _sine(440, 0.08, 0.3)
    w2 = _sine(660, 0.08, 0.3)
    w3 = _sine(880, 0.1, 0.3)
    wave = np.concatenate([w1, w2, w3])
    wave = _envelope(wave, attack=0.005, decay=0.25)
    return _make_sound(wave)

# Boss hit: deep thud
def make_boss_hit_sound():
    t = np.linspace(0, 0.15, int(SAMPLE_RATE * 0.15), endpoint=False)
    freq = np.linspace(180, 60, len(t))
    wave = np.sin(2 * np.pi * freq * t) * 0.4 * 32767
    wave = _envelope(wave, attack=0.005, decay=0.14)
    return _make_sound(wave)

# Player hit / life lost: harsh buzz
def make_hit_sound():
    t = np.linspace(0, 0.2, int(SAMPLE_RATE * 0.2), endpoint=False)
    wave = np.sign(np.sin(2 * np.pi * 120 * t)) * 0.35 * 32767
    wave = _envelope(wave, attack=0.005, decay=0.19)
    return _make_sound(wave)
