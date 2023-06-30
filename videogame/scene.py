# Brandon Nguyen
# nguyen.bradon771@csu.fullerton.edu
# @brandonnguyenr

"""Scene objects for making games with PyGame."""

import os
import pygame
import rgbcolors
from player import Player


# If you're interested in using abstract base classes, feel free to rewrite
# these classes.
# For more information about Python Abstract Base classes, see
# https://docs.python.org/3.8/library/abc.html

class SceneManager:
    def __init__(self):
        self._scene_dict = {}
        self._current_scene = None
        self._next_scene = None
        # This is a safety to ensure that calling
        # next() twice in a row without calling set_next_scene()
        # will raise StopIteration.
        self._reloaded = True

    def set_next_scene(self, key):
        self._next_scene = self._scene_dict[key]
        self._reloaded = True

    def add(self, scene_list):
        for (index, scene) in enumerate(scene_list):
            self._scene_dict[str(index)] = scene
        self._current_scene = self._scene_dict['0']

    def __iter__(self):
        return self

    def __next__(self):
        if self._next_scene and self._reloaded:
            self._reloaded = False
            return self._next_scene
        else:
            raise StopIteration

class Scene:
    """Base class for making PyGame Scenes."""

    def __init__(self, screen, background_color, soundtrack=None):
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
                pygame.mixer.music.load(self._soundtrack)
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
    def __init__(self, screen, background_color):
        super().__init__(screen, background_color)
        (w, h) = self._screen.get_size()
        player_sprite = Player((w / 2, h), w, 5)
        self.player = pygame.sprite.GroupSingle(player_sprite)
        self._next_key = '1'

    def start_scene(self):
        super().start_scene()

    def end_scene(self):
        super().end_scene()

    def update_scene(self):
        self.player.update()

    def draw(self):
        super().draw()
        self.player.draw(self._screen)
        self.player.sprite.lasers.draw(self._screen)

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

    def end_scene(self):
        super().end_scene()
        self._is_valid = True

    def process_event(self, event):
        super().process_event(event)
        if event.type == pygame.KEYDOWN:
            self._scene_manager.set_next_scene('1') 

