# Import necessary libraries
import pygame
import os
import random  # Add random library for randomization

# Define the game window size
SCREEN_WIDTH = 800    
SCREEN_HEIGHT = 600   
PADDLE_SPEED = 7      
BALL_SPEED = 5        

pygame.init()

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
clock = pygame.time.Clock()
pygame.display.set_caption("Pong Game")

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([15, 15])
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.score_left = 0    
        self.score_right = 0   
        self.reset_ball()  # Call reset_ball to set initial position and speed

    def reset_ball(self):
        # Set random vertical position between top and bottom of screen
        # (leaving some space from edges)
        random_y = random.randint(50, SCREEN_HEIGHT - 50)
        
        # Place ball in the middle horizontally, but at random vertical position
        self.rect.center = (SCREEN_WIDTH // 2, random_y)
        
        # Randomly choose starting direction (left or right)
        self.move_horizontal = BALL_SPEED * random.choice([-1, 1])
        
        # Randomly choose vertical speed and direction
        # Using random.uniform for more precise random numbers
        self.move_vertical = random.uniform(-BALL_SPEED, BALL_SPEED)

    def animation(self):
        self.rect.x += self.move_horizontal  
        self.rect.y += self.move_vertical    

        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.move_vertical = -self.move_vertical  

        if self.rect.left <= 0:              
            self.score_right += 1            
            self.reset_ball()                
        elif self.rect.right >= SCREEN_WIDTH:  
            self.score_left += 1             
            self.reset_ball()                

    def collide(self, sprite_group):
        if pygame.sprite.spritecollide(self, sprite_group, False):
            self.move_horizontal = -self.move_horizontal
            # Add slight randomization to vertical movement on paddle hit
            self.move_vertical += random.uniform(-0.5, 0.5)
            # Keep vertical speed within reasonable limits
            self.move_vertical = max(min(self.move_vertical, BALL_SPEED), -BALL_SPEED)
            # Speed up horizontal movement
            self.move_horizontal *= 1.1 if abs(self.move_horizontal) < 15 else 1

    def update(self):
        self.animation()
        self.collide(player_sprites)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, controls):
        super().__init__()
        self.image = pygame.Surface([20, 100])
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.controls = controls

    def update(self):
        keys = pygame.key.get_pressed()
        
        if keys[self.controls['up']] and self.rect.top > 0:
            self.rect.y -= PADDLE_SPEED
        if keys[self.controls['down']] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += PADDLE_SPEED

controls_player1 = {'up': pygame.K_w, 'down': pygame.K_s}
controls_player2 = {'up': pygame.K_UP, 'down': pygame.K_DOWN}

player_1 = Player(30, SCREEN_HEIGHT // 2 - 50, controls_player1)
player_2 = Player(SCREEN_WIDTH - 50, SCREEN_HEIGHT // 2 - 50, controls_player2)

player_sprites = pygame.sprite.Group()
player_sprites.add(player_1, player_2)

ball_sprite = Ball()
ball = pygame.sprite.GroupSingle(ball_sprite)

font = pygame.font.Font(None, 74)

def draw_score():
    score_left = font.render(str(ball_sprite.score_left), True, (255, 255, 255))
    score_right = font.render(str(ball_sprite.score_right), True, (255, 255, 255))
    screen.blit(score_left, (SCREEN_WIDTH // 4, 20))
    screen.blit(score_right, (3 * SCREEN_WIDTH // 4, 20))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    pygame.draw.aaline(screen, (255, 255, 255),
                      (SCREEN_WIDTH // 2, 0),
                      (SCREEN_WIDTH // 2, SCREEN_HEIGHT))

    ball.update()
    player_sprites.update()
    
    ball.draw(screen)
    player_sprites.draw(screen)
    
    draw_score()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()