import pygame
import os

class SoundPlayer:
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        subdir_name = "sound"

        subdir_path = os.path.join(current_dir, subdir_name)
        os.chdir(subdir_path)
        
        pygame.init()
        self.sound_file = subdir_path
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