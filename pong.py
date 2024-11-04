import pygame
import os


#constants 

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600

pygame.init()

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
clock = pygame.time.Clock()


class Ball(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join("images", "ball.png")).convert_alpha()
        self.rect = self.image.get_rect(center=(400, 300))
        self.move_horizontal = 3
        self.move_vertical = 3  # Initial movement speed and direction

    def animation(self):
        # Move the ball horizontally
        self.rect.x += self.move_horizontal
        # Move the ball vertically
        self.rect.y += self.move_vertical

        # Check if the ball hits the left or right edge of the screen
        if self.rect.right >= (SCREEN_WIDTH) or self.rect.left <= 0:
            self.move_horizontal = -self.move_horizontal  # Reverse the direction
        elif self.rect.bottom >=(SCREEN_HEIGHT) or self.rect.top <=0:
            self.move_vertical = -self.move_vertical

    def update(self):
        self.animation()

class Player_1(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.image.load(os.path.join("images", "side-bar.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x  # Initial x-position
        self.rect.y = y  # Initial y-position

    def movement(self):
        key = pygame.key.get_pressed()
        dist = 4
        if key[pygame.K_w]:
            self.rect.y -= dist  # Update rect.y 
        elif key[pygame.K_s]:
            self.rect.y += dist  # Update rect.y 

        # Boundary checks to prevent the player from moving off the screen
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:  
            self.rect.bottom = SCREEN_HEIGHT

    def update(self):
        self.movement()


class Player_2(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.image.load(os.path.join("images", "side-bar.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x  # Initial x-position
        self.rect.y = y  # Initial y-position

    def movement(self):
        key = pygame.key.get_pressed()
        dist = 4
        if key[pygame.K_UP]:
            self.rect.y -= dist  # Update rect.y 
        elif key[pygame.K_DOWN]:
            self.rect.y += dist  # Update rect.y 

        # Boundary checks to prevent the player from moving off the screen
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:  
            self.rect.bottom = SCREEN_HEIGHT

    def update(self):
        self.movement()



player_1 = pygame.sprite.GroupSingle()
player_1.add(Player_1(10, (SCREEN_HEIGHT/2)))

player_2 = pygame.sprite.GroupSingle()
player_2.add(Player_2((SCREEN_WIDTH - 50), (SCREEN_HEIGHT/2)))

ball = pygame.sprite.GroupSingle()
ball.add(Ball())




running = True

while running:
    screen.fill("white")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    # draw the ball
    ball.draw(screen)
    ball.update()

    # Draw player 1
    player_1.draw(screen)
    player_1.update()

    # Draw player 2
    player_2.draw(screen)
    player_2.update()



    # collision 
    ball_sprite = ball.sprite
    player1_sprite = player_1.sprite
    player2_sprite = player_2.sprite

    if pygame.sprite.spritecollide(ball_sprite,player_1, False):
        ball_sprite.move_horizontal = abs(ball_sprite.move_horizontal)
    elif pygame.sprite.spritecollide(ball_sprite,player_2,False):
        ball_sprite.move_horizontal = abs(ball_sprite.move_horizontal)
        
        
    

    pygame.display.update()

    clock.tick(60)

pygame.quit()