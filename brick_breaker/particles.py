# particles.py
import pygame
import random
import math
from config import *


class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        # Ensure color is valid RGB tuple
        if isinstance(color, tuple) and len(color) >= 3:
            self.color = (int(color[0]), int(color[1]), int(color[2]))
        else:
            self.color = (255, 255, 255)

        self.size = random.randint(2, 6)
        self.speed_x = random.uniform(-3, 3)
        self.speed_y = random.uniform(-3, 3)
        self.life = 1.0  # 1.0 to 0.0
        self.decay = random.uniform(0.02, 0.05)

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.life -= self.decay
        self.speed_y += 0.1  # Gravity
        return self.life > 0

    def draw(self, screen):
        alpha = int(max(0, min(255, self.life * 255)))
        if alpha > 0 and self.size > 0:
            # Create surface with alpha for particle
            particle_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)

            # Ensure color values are valid
            r = int(max(0, min(255, self.color[0])))
            g = int(max(0, min(255, self.color[1])))
            b = int(max(0, min(255, self.color[2])))

            pygame.draw.circle(particle_surface, (r, g, b, alpha),
                               (self.size, self.size), self.size)
            screen.blit(particle_surface, (int(self.x - self.size), int(self.y - self.size)))


class ParticleSystem:
    def __init__(self):
        self.particles = []

    def add_brick_break(self, x, y, color, count=20):
        """Add particles for brick break effect"""
        for _ in range(count):
            self.particles.append(Particle(x, y, color))

    def add_powerup_collect(self, x, y, color, count=15):
        """Add particles for power-up collection"""
        for _ in range(count):
            particle = Particle(x, y, color)
            particle.speed_y = random.uniform(-5, -2)  # Upward burst
            self.particles.append(particle)

    def update(self):
        """Update all particles"""
        self.particles = [p for p in self.particles if p.update()]

    def draw(self, screen):
        """Draw all particles"""
        for particle in self.particles:
            particle.draw(screen)