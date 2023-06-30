import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load('videogame/data/player.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = pos)