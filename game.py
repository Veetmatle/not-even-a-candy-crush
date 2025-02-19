import pygame
from player import Player
from falling_objects import FallingObject
from settings import WIDTH, HEIGHT, LIVES, POINTS_TO_SPEEDUP, SPEED_INCREASE, SPAWN_INTERVAL, OBJECT_SPEED
from assets_loader import load_image
from sound_manager import SoundManager

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Not even a candy crush")

        self.clock = pygame.time.Clock()
        self.running = True

        # bg
        self.background = pygame.image.load("assets/tlo.jpg").convert_alpha()
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

        # half-visible bg
        self.overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)  
        self.overlay.fill((0, 0, 0, 80))  

        # sounds
        self.sound_manager = SoundManager()
        self.sound_manager.start_background_music()


        # assets loading
        self.player = Player(WIDTH // 2, HEIGHT - 20) 
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        
        # falling objects
        self.falling_objects = pygame.sprite.Group()

        # images loading
        self.candy_images = [load_image(f"assets/candy_{i}.png") for i in range(1, 3)]
        self.bad_image = load_image("assets/screw.png")
        self.heart_image = load_image("assets/heart.png", (40, 40))

        # stats
        self.lives = LIVES
        self.score = 0
        self.object_speed = OBJECT_SPEED
        self.spawn_time = SPAWN_INTERVAL
        self.last_spawn = pygame.time.get_ticks()
        
        # game state
        self.game_over_state = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def spawn_object(self):
        now = pygame.time.get_ticks()
        self.spawn_time = max(300, SPAWN_INTERVAL - (self.score * 10))
        if now - self.last_spawn > self.spawn_time:
            obj = FallingObject(self.candy_images, self.bad_image)
            self.falling_objects.add(obj)
            self.all_sprites.add(obj)
            self.last_spawn = now

    def update(self):
        if not self.game_over_state:
            keys = pygame.key.get_pressed()
            self.player.update(keys)
            
            # falling objects update
            for obj in self.falling_objects:
                obj.update()
                if obj.rect.top > HEIGHT:
                    if not obj.is_bad: 
                        self.lives -= 1
                        self.sound_manager.play_heart_loss()
                        if self.lives <= 0:
                            self.game_over_state = True
                    obj.kill()  

            # collision detection
            hits = pygame.sprite.spritecollide(self.player, self.falling_objects, True)
            for obj in hits:
                if obj.is_bad:
                    self.lives -= 1
                    self.sound_manager.play_heart_loss()
                    if self.lives <= 0:
                        self.game_over_state = True
                else:
                    self.score += 1
                    self.sound_manager.play_candy_collect()  
                    if self.score % POINTS_TO_SPEEDUP == 0:
                        self.object_speed += SPEED_INCREASE
                        for obj in self.falling_objects:
                            obj.speed += (self.object_speed - obj.speed) * 0.05 

        
    def draw(self):
        self.screen.fill((0, 0, 0))  
        self.screen.blit(self.background, (0, 0))  
        self.screen.blit(self.overlay, (0, 0))  

        self.all_sprites.draw(self.screen)

        # heart drawing
        for i in range(self.lives):
            self.screen.blit(self.heart_image, (WIDTH - 150 + i * 50, 10))
        
        # points drawing
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Punkty: {self.score}", True, (0, 0, 0))
        self.screen.blit(score_text, (10, 10))

        if self.game_over_state:
            self.draw_game_over()

        pygame.display.flip()

    def draw_game_over(self):
        font = pygame.font.Font(None, 72)
        text = font.render("KONIEC GRY", True, (255, 0, 0))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(text, text_rect)

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.handle_events()
            self.spawn_object()
            self.update()
            self.draw()

            if self.game_over_state:
                pygame.time.delay(3000)
                self.running = False