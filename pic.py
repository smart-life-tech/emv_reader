import pygame
import sys
import time
import os
# Initialize Pygame
pygame.init()

# Set the display to full screen
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

# Get the screen dimensions
screen_width, screen_height = screen.get_size()

# Load image
image = pygame.image.load("/home/chingup/Downloads/logo.jpg")

# Scale the image to fit the full screen
image = pygame.transform.scale(image, (700, 700))

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with black
    screen.fill((0, 0, 0))

    # Draw the stretched image on the screen
    screen.blit(image, (0, 0))

    # Update the display
    pygame.display.flip()

    # Display the image for 5 seconds
    time.sleep(10)
    file_path = '/home/chingup/emv_reader/pic.txt'
    file_size = os.path.getsize(file_path)
    if file_size>0:
        running = False
        break

# Quit Pygame
pygame.quit()
sys.exit()
