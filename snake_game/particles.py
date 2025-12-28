# particles.py
import pygame
import random
import math
from config import *


class Particle:
    def __init__(self, x, y, color, particle_type="food"):
        self.x = x
        self.y = y
        # Ensure color is a tuple of 3 integers (R, G, B)
        if isinstance(color, tuple) and len(color) == 3:
            self.color = color
        else:
            # Default to white if invalid color
            self.color = (255, 255, 255)

        self.type = particle_type

        if particle_type == "food":
            self.size = random.uniform(1, 4)
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(1, 3)
            self.vx = math.cos(angle) * speed
            self.vy = math.sin(angle) * speed
            self.life = random.uniform(0.5, 1.0)
            self.gravity = 0.1
        elif particle_type == "trail":
            self.size = random.uniform(1, 2)
            self.vx = random.uniform(-0.5, 0.5)
            self.vy = random.uniform(-0.5, 0.5)
            self.life = random.uniform(0.3, 0.6)
            self.gravity = 0.05
        elif particle_type == "collision":
            self.size = random.uniform(2, 5)
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(2, 5)
            self.vx = math.cos(angle) * speed
            self.vy = math.sin(angle) * speed
            self.life = random.uniform(0.8, 1.2)
            self.gravity = 0.2

        self.decay = random.uniform(0.01, 0.03)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        self.life -= self.decay
        self.size *= 0.98  # Shrink over time
        return self.life > 0

    def draw(self, screen):
        alpha = int(max(0, min(255, self.life * 255)))
        if alpha > 0 and self.size > 0:
            # Create surface with alpha
            size = int(self.size)
            if size < 1:
                return

            surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)

            # Ensure color values are valid integers
            r = int(max(0, min(255, self.color[0])))
            g = int(max(0, min(255, self.color[1])))
            b = int(max(0, min(255, self.color[2])))

            if self.type == "food":
                pygame.draw.circle(surface, (r, g, b, alpha),
                                   (size, size), size)
            elif self.type == "trail":
                pygame.draw.circle(surface, (r, g, b, alpha),
                                   (size, size), size)
            elif self.type == "collision":
                # Star shape for collision
                points = []
                for i in range(5):
                    angle = math.pi * 2 * i / 5 - math.pi / 2
                    outer_x = size + math.cos(angle) * size
                    outer_y = size + math.sin(angle) * size
                    points.append((outer_x, outer_y))

                    inner_angle = angle + math.pi / 5
                    inner_x = size + math.cos(inner_angle) * (size * 0.5)
                    inner_y = size + math.sin(inner_angle) * (size * 0.5)
                    points.append((inner_x, inner_y))

                if len(points) >= 3:  # Need at least 3 points for polygon
                    pygame.draw.polygon(surface, (r, g, b, alpha), points)

            screen.blit(surface, (int(self.x - size), int(self.y - size)))


class ParticleSystem:
    def __init__(self):
        self.particles = []

    def add_food_particles(self, x, y, color, count=15):
        """Add particles for food collection"""
        # Ensure color is valid
        if not isinstance(color, tuple) or len(color) != 3:
            color = (255, 50, 50)  # Default to red

        for _ in range(count):
            self.particles.append(Particle(x, y, color, "food"))

    def add_trail_particles(self, x, y, color, count=3):
        """Add particles for snake trail"""
        # Ensure color is valid
        if not isinstance(color, tuple) or len(color) != 3:
            color = (50, 255, 50)  # Default to green

        for _ in range(count):
            self.particles.append(Particle(x, y, color, "trail"))

    def add_collision_particles(self, x, y, color, count=20):
        """Add particles for collision"""
        # Ensure color is valid
        if not isinstance(color, tuple) or len(color) != 3:
            color = (255, 50, 50)  # Default to red

        for _ in range(count):
            self.particles.append(Particle(x, y, color, "collision"))

    def update(self):
        """Update all particles"""
        self.particles = [p for p in self.particles if p.update()]

    def draw(self, screen):
        """Draw all particles"""
        for particle in self.particles:
            particle.draw(screen)