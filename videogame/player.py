# Brandon Nguyen
# nguyen.bradon771@csu.fullerton.edu
# @brandonnguyenr

import math
import rgbcolors
import pygame

class Player:
    def __init__(self, position):
        self._position = position
        self._radius = 40
        self._color = rgbcolors.orange
        self._velocity = pygame.math.Vector2(0, 0)

    def update(self):
        v = self._position.x + self._velocity.x
        if v > 0 and v < 800:
            self._position = self._position + self._velocity
        
    @property
    def position(self):
        return self._position
    
    def stop(self):
        self._velocity = pygame.math.Vector2(0, 0)
        
    def move_left(self):
        self._velocity = pygame.math.Vector2(-10, 0)
    
    def move_right(self):
        self._velocity = pygame.math.Vector2(10, 0)
    
    def _move(self, v):
        self._position = self._position + v

    def draw(self, screen):
        """Draw the circle to screen."""
        pygame.draw.circle(screen, self._color, self._position, self._radius)
        

class Bullet:
    def __init__(self, position, target_position, speed):
        self._position = pygame.math.Vector2(position)
        self._target_position = pygame.math.Vector2(target_position)
        self._speed = speed
        self._color = rgbcolors.mult_color(self._speed, rgbcolors.red)
        self._radius = 10
    
    @property
    def rect(self):
        """Return bounding rect."""
        left = self._position.x - self._radius
        top = self._position.y - self._radius
        width = 2 * self._radius
        return pygame.Rect(left, top, width, width)
    
    def should_die(self):
        squared_distance = (self._position - self._target_position).length_squared()
        return math.isclose(squared_distance, 0.0, rel_tol=1e-01)
            
    def update(self, delta_time):
        self._position.move_towards_ip(self._target_position, self._speed * delta_time)
    
    def draw(self, screen):
        """Draw the circle to screen."""
        pygame.draw.circle(screen, self._color, self._position, self._radius)