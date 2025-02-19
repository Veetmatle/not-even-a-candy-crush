import pygame

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        
        # Sound loading
        self.background_music = pygame.mixer.Sound("assets/sounds/dzwiek_gry.wav")
        self.heart_loss_sound = pygame.mixer.Sound("assets/sounds/minus_serce.wav")
        self.candy_collect_sound = pygame.mixer.Sound("assets/sounds/podniesienie_cukierka.wav")
        
        # Sound settings
        self.background_music.set_volume(0.3)  
        self.heart_loss_sound.set_volume(0.4)
        self.candy_collect_sound.set_volume(0.4)
    
    def start_background_music(self):
        self.background_music.play(loops=-1)
        
    def play_heart_loss(self):
        self.heart_loss_sound.play()
        
    def play_candy_collect(self):
        self.candy_collect_sound.play()
        
    def stop_all(self):
        pygame.mixer.stop()