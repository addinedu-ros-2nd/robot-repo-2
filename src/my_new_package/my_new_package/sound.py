import pygame
import os

class SoundPlayer:
    def __init__(self, sound_file):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        sound_path = os.path.join(current_dir, 'src/my_new_package/my_new_package/sound',sound_file)
        pygame.init()
        self.sound_file = sound_path
        self.sound = pygame.mixer.Sound(self.sound_file)

    def play(self):
        self.sound.play()
    def wait_for_completion(self):
        pygame.time.delay(int(self.sound.get_length() * 900))
    def cleanup(self):
        pygame.quit()

def play_sound(sound_file):
    player = SoundPlayer(sound_file)
    player.play()
    player.wait_for_completion()
    player.cleanup()