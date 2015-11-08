import sys, pygame
pygame.init()

# Set screen size
size = width, height = 640, 480
screen = pygame.display.set_mode(size)

while 1:
    for event in pygame.event.get():
        # Exit program if "x" is pressed
        if event.type == pygame.QUIT:
            pygame.quit();
            sys.exit()

        # Draw sphere

        # Fill screen
        screen.fill((0,32,0))
        pygame.display.flip()