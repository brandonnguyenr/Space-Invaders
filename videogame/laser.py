# Brandon Nguyen
# nguyen.bradon771@csu.fullerton.edu
# @brandonnguyenr

"""Laser class to create a laser."""

import pygame

class Laser(pygame.sprite.Sprite):
    """Laser class to create the lasers."""
    def __init__(self, pos, speed, height):
        super().__init__()
        self.image = pygame.Surface((4, 20))
        self.image.fill('white')
        self.rect = self.image.get_rect(center = pos)
        self.speed = speed
        self.border_y = height

    def destroy(self):
        """Destroy laser on contact."""
        if self.rect.y <= -50 or self.rect.y >= self.border_y + 50:
            self.kill()

    def update(self):
        """Update laser speed."""
        self.rect.y += self.speed
