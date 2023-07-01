# Brandon Nguyen
# nguyen.bradon771@csu.fullerton.edu
# @brandonnguyenr

"""Player class to create a player."""

"""pylint reading lots of errors on this page but, errors are nonexistent on page."""
import pygame
from laser import Laser

class Player(pygame.sprite.Sprite):
    """Create player sprite."""
    def __init__(self, pos, border, speed):
        super().__init__()
        self.image = pygame.image.load('videogame/data/player.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = pos)
        self.speed = speed
        self.max_x_border = border
        self.ready = True
        self.laser_time = 0
        self.laser_cooldown = 400
        self.lasers = pygame.sprite.Group()
        self.laser_sound = pygame.mixer.Sound('videogame/data/laser.wav')
        self.laser_sound.set_volume(0.5)

    def border(self):
        """Boundaries of the player."""
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= self.max_x_border:
            self.rect.right = self.max_x_border

    def get_input(self):
        """Player movement with keys."""
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.rect.x += self.speed
        elif keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_SPACE]:
            self.shooting()
            self.ready = False
            self.laser_time = pygame.time.get_ticks()
            self.laser_sound.play()

    def cooldown(self):
        """Cooldown on shots so you cant spam."""
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_cooldown:
                self.ready = True

    def shooting(self):
        """Player shooting speed."""
        if self.ready:
            self.lasers.add(Laser(self.rect.center, -8, self.rect.bottom))
            self.ready = False
            self.laser_time = pygame.time.get_ticks()

    def update(self):
        """Updates on the players."""
        self.get_input()
        self.border()
        self.cooldown()
        self.lasers.update()
