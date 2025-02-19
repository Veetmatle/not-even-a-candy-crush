import pygame
import random
from settings import LANE_X, OBJECT_SPEED

class FallingObject(pygame.sprite.Sprite):
    def __init__(self, images, bad_image):
        super().__init__()
        self.is_bad = random.random() < 0.2  
        
        if self.is_bad:
            self.image = bad_image
        else:
            self.image = random.choice(images)

        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(midtop=(random.choice(LANE_X), -50))
        self.speed = OBJECT_SPEED

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > 600:
            self.kill()
