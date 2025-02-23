# Import necessary libraries
# Pygame is a library for making games in Python
import pygame
import os

# Define the game window size
# These values can be changed to make the window bigger or smaller
SCREEN_WIDTH = 800    # Width of the game window in pixels
SCREEN_HEIGHT = 600   # Height of the game window in pixels
PADDLE_SPEED = 7      # How fast the paddles move (higher number = faster movement)
BALL_SPEED = 5        # Starting speed of the ball (higher number = faster ball)

# Initialize Pygame - This must be done before using any pygame functions
pygame.init()

# Create the game window with the specified size
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
# Create a clock object to control game speed
clock = pygame.time.Clock()
# Set the title of the game window
pygame.display.set_caption("Pong Game")

# Define the Ball class - This creates the ball object that bounces between paddles
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()
        # Create a white square for the ball (size: 15x15 pixels)
        self.image = pygame.Surface([15, 15])
        self.image.fill((255, 255, 255))  # Color is white (RGB: 255, 255, 255)
        # Set the ball's starting position to the center of the screen
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        # Set the ball's initial movement speed and direction
        self.move_horizontal = BALL_SPEED
        self.move_vertical = BALL_SPEED
        # Initialize score counters for both players
        self.score_left = 0    # Player 1's score (left side)
        self.score_right = 0   # Player 2's score (right side)

    def reset_ball(self):
        # Put the ball back in the center after a point is scored
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        # Reset the ball's movement speed to initial values
        self.move_horizontal = BALL_SPEED
        self.move_vertical = BALL_SPEED

    def animation(self):
        # Move the ball by updating its position
        self.rect.x += self.move_horizontal  # Move horizontally
        self.rect.y += self.move_vertical    # Move vertically

        # Make the ball bounce off the top and bottom of the screen
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.move_vertical = -self.move_vertical  # Reverse vertical direction

        # Score points when ball goes past a paddle
        if self.rect.left <= 0:              # Ball passed left side
            self.score_right += 1            # Add point to right player
            self.reset_ball()                # Reset ball position
        elif self.rect.right >= SCREEN_WIDTH:  # Ball passed right side
            self.score_left += 1             # Add point to left player
            self.reset_ball()                # Reset ball position

    def collide(self, sprite_group):
        # Check if the ball hits a paddle
        if pygame.sprite.spritecollide(self, sprite_group, False):
            # Reverse the horizontal direction when hitting a paddle
            self.move_horizontal = -self.move_horizontal
            # Make the ball slightly faster after each hit (max speed cap at 15)
            self.move_horizontal *= 1.1 if abs(self.move_horizontal) < 15 else 1

    def update(self):
        # Update the ball's position and check for collisions
        self.animation()
        self.collide(player_sprites)

# Define the Player class - This creates the paddle objects that players control
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, controls):
        # Call the parent class (Sprite) constructor
        super().__init__()
        # Create a white rectangle for the paddle (size: 20x100 pixels)
        self.image = pygame.Surface([20, 100])
        self.image.fill((255, 255, 255))  # Color is white
        self.rect = self.image.get_rect()
        # Set the paddle's starting position
        self.rect.x = x
        self.rect.y = y
        # Store the control keys for this paddle
        self.controls = controls

    def update(self):
        # Get the current state of all keyboard keys
        keys = pygame.key.get_pressed()
        
        # Move the paddle up if the 'up' key is pressed and paddle isn't at the top
        if keys[self.controls['up']] and self.rect.top > 0:
            self.rect.y -= PADDLE_SPEED
        # Move the paddle down if the 'down' key is pressed and paddle isn't at the bottom
        if keys[self.controls['down']] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += PADDLE_SPEED

# Define the control keys for each player
controls_player1 = {'up': pygame.K_w, 'down': pygame.K_s}           # Player 1 uses W and S keys
controls_player2 = {'up': pygame.K_UP, 'down': pygame.K_DOWN}       # Player 2 uses arrow keys

# Create the paddle objects for both players
player_1 = Player(30, SCREEN_HEIGHT // 2 - 50, controls_player1)                # Left paddle
player_2 = Player(SCREEN_WIDTH - 50, SCREEN_HEIGHT // 2 - 50, controls_player2) # Right paddle

# Create a group to hold all paddle sprites
player_sprites = pygame.sprite.Group()
player_sprites.add(player_1, player_2)

# Create the ball object and add it to a sprite group
ball_sprite = Ball()
ball = pygame.sprite.GroupSingle(ball_sprite)

# Set up the font for displaying scores
font = pygame.font.Font(None, 74)  # None uses default font, 74 is the font size

def draw_score():
    # Create text surfaces for both players' scores
    score_left = font.render(str(ball_sprite.score_left), True, (255, 255, 255))
    score_right = font.render(str(ball_sprite.score_right), True, (255, 255, 255))
    # Draw the scores on the screen
    screen.blit(score_left, (SCREEN_WIDTH // 4, 20))       # Left player's score
    screen.blit(score_right, (3 * SCREEN_WIDTH // 4, 20))  # Right player's score

# Main game loop - This runs continuously while the game is playing
running = True
while running:
    # Handle game events (like quitting the game)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If the window's close button is clicked
            running = False            # Stop the game

    # Fill the screen with black color (RGB: 0, 0, 0)
    screen.fill((0, 0, 0))

    # Draw the center line
    pygame.draw.aaline(screen, (255, 255, 255),  # Draw a white anti-aliased line
                      (SCREEN_WIDTH // 2, 0),     # Start at top center
                      (SCREEN_WIDTH // 2, SCREEN_HEIGHT))  # End at bottom center

    # Update all game objects
    ball.update()         # Update ball position and check collisions
    player_sprites.update()  # Update paddle positions based on key presses
    
    # Draw all game objects on the screen
    ball.draw(screen)
    player_sprites.draw(screen)
    
    # Display the current score
    draw_score()

    # Update the display to show all changes
    pygame.display.flip()
    # Control game speed (60 frames per second)
    clock.tick(60)

# Quit the game properly when the loop ends
pygame.quit()