import pygame
import os


#constants 

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

pygame.init()

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
clock = pygame.time.Clock()


class Ball(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join("images", "ball.png")).convert_alpha()
        self.rect = self.image.get_rect(center=(400, 300))
        self.move_horizontal = 4
        self.move_vertical = 3  # Initial movement speed and direction

    def animation(self):
        # Move the ball horizontally
        self.rect.x += self.move_horizontal
        # Move the ball vertically
        self.rect.y += self.move_vertical

        # Check if the ball hits the left or right edge of the screen
        if self.rect.bottom >=(SCREEN_HEIGHT) or self.rect.top <=0:
            self.move_vertical = -self.move_vertical

    def collide(self, spriteGroup):
        if pygame.sprite.spritecollide(self,spriteGroup,False):
            self.move_horizontal = -self.move_horizontal

        

    def update(self):
        self.animation()
        self.collide(player_sprites)

class Player_1(pygame.sprite.Sprite):
    def __init__(self, x, y, controls):
        super().__init__()

        self.image = pygame.image.load(os.path.join("images", "side-bar.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x  # Initial x-position
        self.rect.y = y  # Initial y-position
        self.controls = controls 

   

        # Boundary checks to prevent the player from moving off the screen
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:  
            self.rect.bottom = SCREEN_HEIGHT

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[self.controls['up']]:
            self.rect.y -= 5
        if keys[self.controls['down']]:
            self.rect.y += 5
        if keys[self.controls['left']]:
            self.rect.x -= 5
        if keys[self.controls['right']]:
            self.rect.x += 5


# create player's controls
controls_player1 = {'up': pygame.K_w, 'down': pygame.K_s, 'left': pygame.K_a, 'right': pygame.K_d}
controls_player2 = {'up': pygame.K_UP, 'down': pygame.K_DOWN, 'left': pygame.K_LEFT, 'right': pygame.K_RIGHT}

#create player's sprite
player_1 = Player_1(10, (SCREEN_HEIGHT/2),controls_player1)
player_2 = Player_1((SCREEN_WIDTH - 50), (SCREEN_HEIGHT/2),controls_player2)

#create sprite Groupe
player_sprites = pygame.sprite.Group()
# Add players to the sprite groupe.
player_sprites.add(player_1,player_2)

# Create a ball group single add the ball to it
ball = pygame.sprite.GroupSingle()
ball.add(Ball()) 



# Create the game loop
running = True

while running:
    screen.fill("red")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    # draw the ball
    ball.draw(screen)
    ball.update()

    # Draw players
    player_sprites.draw(screen)
    player_sprites.update()


    pygame.display.update()

    clock.tick(60)

pygame.quit()