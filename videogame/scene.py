# Brandon Nguyen
# nguyen.bradon771@csu.fullerton.edu
# @brandonnguyenr

"""Scene objects for making games with PyGame."""

import sys
import pygame.mixer
import pygame
import rgbcolors
from player import Player
from random import choice, randint
from laser import Laser
import obstacle


# If you're interested in using abstract base classes, feel free to rewrite
# these classes.
# For more information about Python Abstract Base classes, see
# https://docs.python.org/3.8/library/abc.html

class SceneManager:
    """Scene Manageers that manages all the scenes."""
    def __init__(self):
        self._scene_dict = {}
        self._current_scene = None
        self._next_scene = None
        # This is a safety to ensure that calling
        # next() twice in a row without calling set_next_scene()
        # will raise StopIteration.
        self._reloaded = True

    def set_next_scene(self, key):
        """Next Scene."""
        self._next_scene = self._scene_dict[key]
        self._reloaded = True

    def add(self, scene_list):
        """Add.scene"""
        for (index, scene) in enumerate(scene_list):
            self._scene_dict[str(index)] = scene
        self._current_scene = self._scene_dict['0']

    def __iter__(self):
        """Return self."""
        return self

    def __next__(self):
        """Next Scene."""
        if self._next_scene and self._reloaded:
            self._reloaded = False
            return self._next_scene
        else:
            raise StopIteration

class Scene:
    """Base class for making PyGame Scenes."""

    def __init__(self, screen, soundtrack=None):
        """Scene initializer"""
        self._screen = screen
        #https://unsplash.com/images/nature/space : website used to grab this background - 6-27-2023
        self._background = pygame.image.load("videogame/data/photo-1534796636912-3b95b3ab5986.jpeg").convert()
        self._frame_rate = 60
        self._is_valid = True
        self._soundtrack = soundtrack
        self._render_updates = None

    def draw(self):
        """Draw the scene."""
        self._screen.blit(self._background, (0, 0))

    def process_event(self, event):
        """Process a game event by the scene."""
        # This should be commented out or removed since it generates a lot of noise.
        # print(str(event))
        if event.type == pygame.QUIT:
            print("Good Bye!")
            self._is_valid = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            print("Bye bye!")
            self._is_valid = False

    def is_valid(self):
        """Is the scene valid? A valid scene can be used to play a scene."""
        return self._is_valid

    def render_updates(self):
        """Render all sprite updates."""

    def update_scene(self):
        """Update the scene state."""

    def start_scene(self):
        """Start the scene."""
        if self._soundtrack:
            try:
                pygame.mixer.music.load('videogame/data/Visager_-_15_-_Epilogue.mp3')
                pygame.mixer.music.set_volume(0.5)
            except pygame.error as pygame_error:
                print("\n".join(pygame_error.args))
                raise SystemExit("broken!!") from pygame_error
            pygame.mixer.music.play(-1)

    def end_scene(self):
        """End the scene."""
        if self._soundtrack and pygame.mixer.music.get_busy():
            pygame.mixer.music.fadeout(500)
            pygame.mixer.music.stop()

    def frame_rate(self):
        """Return the frame rate the scene desires."""
        return self._frame_rate


class PressAnyKeyToExitScene(Scene):
    """Empty scene where it will invalidate when a key is pressed."""

    def process_event(self, event):
        """Process game events."""
        super().process_event(event)
        if event.type == pygame.KEYDOWN:
            self._is_valid = False

class BattleScene(Scene):
    """Everything that happens in the Battle Scene."""
    def __init__(self, screen, background_color):
        super().__init__(screen, background_color)
        (w, h) = self._screen.get_size()
        player_sprite = Player((w / 2, h), w, 5)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        self.lives = 4
        self.live_surf = pygame.image.load('videogame/data/player.png').convert_alpha()
        self.live_x_start_pos = w - self.live_surf.get_size()[0] * 2 - 90
        self.score = 0
        self.font = pygame.font.Font('videogame/data/Pixeled.ttf', 20)

        self.shape = obstacle.shape
        self.shield_size = 6
        self.shields = pygame.sprite.Group()
        self.obstacle_num = 4
        self.obstacle_x_pos = [num * (w / self.obstacle_num) for num in range(self.obstacle_num)]
        self.create_multi_obs(*self.obstacle_x_pos, x_start = w / 15, y_start = 480)

        self.aliens = pygame.sprite.Group()
        self.alien_setup(rows = 6, cols = 8)
        self.alien_direction = 1
        self.alien_lasers = pygame.sprite.Group()

        self.top = pygame.sprite.Group()
        self.top_alien_time = randint(40, 80)

        pygame.mixer.music.load('videogame/data/Visager_-_15_-_Epilogue.mp3')
        self.explosion_sound = pygame.mixer.Sound('videogame/data/explosion.wav')
        self.laser_sound = pygame.mixer.Sound('videogame/data/laser.wav')
        self.explosion_sound.set_volume(0.5)
        self.laser_sound.set_volume(0.5)

        self._next_key = '1'

    def alien_setup(self, rows, cols, x_distance = 60, y_distance = 48, x_offset = 70, y_offset = 100):
        """Place aliens in rows and colums on scene."""
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset
                if row_index == 0:
                    alien_sprite = obstacle.Alien('yellow', x, y)
                elif 1 <= row_index <= 2:
                    alien_sprite = obstacle.Alien('green', x, y)
                else:
                    alien_sprite = obstacle.Alien('red', x, y)
                self.aliens.add(alien_sprite)

    def create_obstacle(self, x_start, y_start, offset_x):
        """Create all obstacles."""
        for row_index, row in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col == 'x':
                    x = x_start + col_index * self.shield_size + offset_x
                    y = y_start + row_index * self.shield_size
                    shield = obstacle.Shield(self.shield_size, rgbcolors.red, x, y)
                    self.shields.add(shield)

    def create_multi_obs(self, *offset, x_start, y_start):
        """Create multiple sets of the obstacles."""
        for offset_x in offset:
            self.create_obstacle(x_start, y_start, offset_x)

    def alien_pos(self):
        """Alien movement on screen."""
        all_aliens = self.aliens.sprites()
        (w, h) = self._screen.get_size()
        for alien in all_aliens:
            if alien.rect.right >= w:
                self.alien_direction = -1
                self.alien_mov(2)
            elif alien.rect.left <= 0:
                self.alien_direction = 1
                self.alien_mov(2)

    def alien_mov(self, distance):
        """Used in alien_pos to find movment position."""
        if self.aliens:
            for alien in self.aliens.sprites():
                alien.rect.y += distance

    def alien_shoot(self):
        """Alien laser shooting."""
        if self.aliens.sprites():
            (w, h) = self._screen.get_size()
            random_alien = choice(self.aliens.sprites())
            alien_laser = Laser(random_alien.rect.center, 6, h)
            self.alien_lasers.add(alien_laser)
            self.laser_sound.play()

    def alien_timer(self, event):
        """Alien timer to space out lasers."""
        ALIEN_LASER = pygame.USEREVENT + 1
        pygame.time.set_timer(ALIEN_LASER, 800)
        if event.type == ALIEN_LASER:
            self.alien_shoot()

    def top_dog_alien(self):
        """Alien at the top with the most points."""
        (w, h) = self._screen.get_size()
        self.top_alien_time -= 1
        if self.top_alien_time <= 0:
            if len(self.top) == 0:
                self.top.add(obstacle.Top_Alien(choice(['right', 'left']), w))
            self.top_alien_time = randint(40, 80)

    def process_event(self, event):
        """Make the top alien rare."""
        super().process_event(event)
        self.alien_timer(event)

    def collisions(self):
        """All the collisions in the game."""
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                if pygame.sprite.spritecollide(laser, self.shields, True):
                    laser.kill()

                aliens_hit = pygame.sprite.spritecollide(laser, self.aliens, True)
                if aliens_hit:
                    for alien in aliens_hit:
                        self.score += alien.value
                        laser.kill()
                        self.explosion_sound.play()
                
                if pygame.sprite.spritecollide(laser, self.top, True):
                    laser.kill()
                    self.score +=500

        if self.alien_lasers:
            for laser in self.alien_lasers:
                if pygame.sprite.spritecollide(laser, self.shields, True):
                    laser.kill()

                if pygame.sprite.spritecollide(laser, self.player, False):
                    laser.kill()
                    self.lives -= 1
                    if self.lives <= 0:
                        pygame.quit()
                        sys.exit()

        if self.aliens:
            for alien in self.aliens:
                pygame.sprite.spritecollide(alien, self.shields, True)

                if pygame.sprite.spritecollide(alien, self.player, True):
                    pygame.quit()
                    sys.exit()

    def display_lives(self):
        """Display the extra lives"""
        for live in range(self.lives - 1):
            x = self.live_x_start_pos + (live * (self.live_surf.get_size()[0] + 10))
            self._screen.blit(self.live_surf,(x, 8))

    def display_score(self):
        """Display the score."""
        score_surface = self.font.render(f'score: {self.score}', False, 'white')
        score_rect = score_surface.get_rect(topleft = (10,-10))
        self._screen.blit(score_surface, score_rect)

    def start_scene(self):
        """Start scene."""
        super().start_scene()
        pygame.mixer.music.play(-1)

    def end_scene(self):
        """End Scene."""
        super().end_scene()
        pygame.mixer.music.stop()

    def update_scene(self):
        """Update Scene."""
        self.player.update()

    def draw(self):
        """Draw everything included."""
        super().draw()
        self.top.update()
        self.aliens.update(self.alien_direction)
        self.alien_lasers.update()

        self.collisions()
        self.display_lives()
        self.display_score()
        self.alien_pos()
        self.top_dog_alien()

        self.shields.draw(self._screen)
        self.aliens.draw(self._screen)
        self.player.draw(self._screen)
        self.player.sprite.lasers.draw(self._screen)
        self.alien_lasers.draw(self._screen)
        self.top.draw(self._screen)

class Title(PressAnyKeyToExitScene):
    """A scene with blinking text."""

    def __init__(
        self, screen, scene_manager, message, color, size, background_color
    ):
        super().__init__(screen, background_color)
        self._scene_manager = scene_manager
        self._message_color = color
        self._message_complement_color = (
            255 - color[0],
            255 - color[1],
            255 - color[2],
        )
        self._size = size
        self._message = message
        self._t = 0.0
        self._delta_t = 0.01

    def _interpolate(self):
        """Rainbow Colors."""
        # This can be done with pygame.Color.lerp
        self._t += self._delta_t
        if self._t > 1.0 or self._t < 0.0:
            self._delta_t *= -1
        c = rgbcolors.sum_color(
            rgbcolors.mult_color(
                (1.0 - self._t), self._message_complement_color
            ),
            rgbcolors.mult_color(self._t, self._message_color),
        )
        return c

    def draw(self):
        """Draw everything on the title screen."""
        super().draw()
        #https://www.1001fonts.com/ : is where the font was aquired - 6-27-2023
        presskey_font = pygame.font.Font(
            "videogame/data/ARCADECLASSIC.TTF", self._size
        )
        presskey = presskey_font.render(
            self._message, True, self._interpolate()
        )
        (w, h) = self._screen.get_size()
        presskey_pos = presskey.get_rect(center=(w / 2, h / 2 - 50))
        press_any_key_font = pygame.font.Font(
            "videogame/data/ARCADECLASSIC.TTF", 15
        )
        press_any_key = press_any_key_font.render(
            'Press  any  key  to  continue', True, rgbcolors.white
        )
        (w, h) = self._screen.get_size()
        press_any_key_pos = press_any_key.get_rect(center=(w / 2, h - 50))
        self._screen.blit(presskey, presskey_pos)
        self._screen.blit(press_any_key, press_any_key_pos)

    def start_scene(self):
        """Start scene."""
        super().start_scene()

    def end_scene(self):
        """End Scene."""
        super().end_scene()

    def end_scene(self):
        """End the scene."""
        super().end_scene()
        self._is_valid = True

    def process_event(self, event):
        """Name the screen and where it leads to."""
        super().process_event(event)
        if event.type == pygame.KEYDOWN:
            self._scene_manager.set_next_scene('1')
