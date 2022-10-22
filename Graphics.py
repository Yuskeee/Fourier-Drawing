from turtle import begin_poly
import Vector
import pygame

class Graphics:
    def __init__(self, width, length):
        """Initialize the graphics object with 60 fps and a black background named 'Fourier Drawing'.
        
        ### Parameters
        - width: the width of the screen
        - length: the length of the screen
        """
        # Initialize pygame
        pygame.init()
        pygame.display.set_caption("Fourier Drawing")
        self.width = width
        self.length = length
        self.screen = pygame.display.set_mode((width, length))
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((255, 255, 255))
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.done = False

    def render(self, objects:Vector):
        """Render the vectors on the screen and flip the display.
        
        ### Parameters
        - objects: Vector
        """
        if len(objects) > 0:
            x = objects[0].x# + self.width / 2
            y = objects[0].y# + self.length / 2
            begin_point = (0, 0)# (self.width / 2, self.length / 2)
            pygame.draw.line(self.screen, (0, 0, 0), begin_point, (x, y), 1)
            for i in range(1, len(objects)):
                pygame.draw.line(self.screen, (0, 0, 0), (x,y), (objects[i].x + x, objects[i].y + y), 1)
                x = objects[i].x + x
                y = objects[i].y + y
        # for obj in objects:
        #     pygame.draw.line(self.screen, (0, 0, 0), (self.width / 2, self.length / 2), (self.width / 2 + obj.x, self.length / 2 + obj.y))
        pygame.display.flip()
    
    def update(self):
        """Update the screen and checks for events."""
        self.clock.tick(self.fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
        return self.done

    def refresh(self):
        """Refresh the screen."""
        self.screen.blit(self.background, (0, 0))

    def draw_point(self, x, y, color=(0, 0, 0)):
        """Draw a point on the screen with the given color."""
        pygame.draw.circle(self.screen, color, (int(x), int(y)), 1)