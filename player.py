import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, border, speed):
        super().__init__()
        self.image = pygame.image.load('videogame/data/player.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = pos)
        self.speed = speed
        self.max_x_border = border

    def border(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= self.max_x_border:
            self.rect.right = self.max_x_border

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.rect.x += self.speed
        elif keys[pygame.K_a]:
            self.rect.x -= self.speed

    def update(self):
        self.get_input()
        self.border()
