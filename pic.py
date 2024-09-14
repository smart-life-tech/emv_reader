import pygame
import sys
import time # Import the time module
# Initialize Pygame
pygame.init()

# Set window dimensions
screen_width = 0
screen_height = 0
screen = pygame.display.set_mode((screen_width, screen_height),pygame.FULLSCREEN)

# Load image
image = pygame.image.load("/home/chingup/Downloads/logo.jpg")

# Get image dimensions
image_width = image.get_width()
image_height = image.get_height()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Fill the screen with black
    screen.fill((0, 0, 0))
    
    # Calculate position to center the image
    image_x = (screen_width - image_width) / 2
    image_y = (screen_height - image_height) / 2
    
    # Draw the image on the screen
    screen.blit(image, (image_x, image_y))
    
    # Update the display
    pygame.display.flip()
    time.sleep(5)
    running=False
    break

# Quit Pygame
pygame.quit()
sys.exit()
