# Brandon Nguyen
# nguyen.bradon771@csu.fullerton.edu
# @brandonnguyenr

"""Obstacle class to create blocking obstacles."""

import pygame

class Shield(pygame.sprite.Sprite):
    """Create the shields."""
    def __init__(self, size, color, x, y):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft = (x, y))

shape = [
'  xxxxxxx',
' xxxxxxxxx',
'xxxxxxxxxxx',
'xxxxxxxxxxx',
'xxxxxxxxxxx',
'xxx     xxx',
'xx       xx']

class Alien(pygame.sprite.Sprite):
    """Create the aliens."""
    def __init__(self, color, x, y):
        super().__init__()
        file_path = 'videogame/data/' + color + '.png'
        self.image = pygame.image.load(file_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))

        if color == 'red':
            self.value = 100
        elif color == 'green':
            self.value = 200
        else:
            self.value = 300

    def update(self, direction):
        """Update alien movements."""
        self.rect.x += direction

class Top_Alien(pygame.sprite.Sprite):
    """Speedy alien at the top worth the most points."""
    def __init__(self, side, w):
        super().__init__()
        self.image = pygame.image.load('videogame/data/extra.png').convert_alpha()
        if side == 'right':
            x = w + 50
            self.speed = -3
        else:
            x = -50
            self.speed = 3
        self.rect = self.image.get_rect(topleft=(x, 80))

    def update(self):
        """Updates on the top alien."""
        self.rect.x += self.speed
        