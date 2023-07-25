# Import required libraries
import pygame
import time
import settings
import random

# Initialize pygame and set window caption and size
pygame.init()
pygame.font.init()
pygame.display.set_caption("Brick Breaker - The Game")
WINDOW = pygame.display.set_mode(settings.WINDOWSIZE)
CLOCK = pygame.time.Clock()

# Create a class to define the Brick objects
class Brick:
    def __init__(self):
        self.height = (settings.HEIGHT//4)//settings.NOOFROWS  # 
        self.width =  settings.WIDTH // settings.NOOFCOLS
        self.color = settings.BRICKCOLOR
        self.bricks = self.create_bricks()
        #create bricks when object is created depending of window size

    def draw(self, surface):
        for brick_rect in self.listOfBricks:
            pygame.draw.rect(surface, self.color, brick_rect)

    def create_bricks(self):
        self.listOfBricks = [] 
        # set the spacing between the bricks   
        spacing_x=10 
        spacing_y=10
        pos_x = spacing_x
        pos_y = spacing_y
        self.width=settings.WIDTH//settings.NOOFCOLS-spacing_x
        # Create bricks in a grid pattern
        for rows in range(settings.NOOFROWS):
            for cols in range(settings.NOOFCOLS):
                brick_rect = pygame.Rect(pos_x, pos_y, self.width, self.height)
                if(pos_x+self.width<settings.WIDTH):
                    self.listOfBricks.append(brick_rect)
                pos_x += self.width + spacing_x  # position of next brick x coordinate
            pos_x  = spacing_x # reset the x position after drawing row columns
            pos_y += self.height + spacing_y  # change the row to the next
        return self.listOfBricks


# Create a class to define the Block (paddle) object
class Block:
    def __init__(self):
        self.color = settings.BLOCKCOLOR
        self.vel = settings.BLOCKVEL
        self.width = settings.BLOCKWIDTH
        self.height = settings.BLOCKHEIGHT
        self.posx, self.posy = settings.BLOCKPOSX, settings.BLOCKPOSY

    def update(self):
        # Check for key presses to move the Block left or right
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.posx > 0:
            self.posx -= self.vel
        if keys[pygame.K_RIGHT] and self.posx < settings.WINDOWSIZE[0] - self.width:
            self.posx += self.vel
        # Draw the Block on the window surface
        pygame.draw.rect(WINDOW, settings.BLOCKCOLOR, (self.posx, self.posy, self.width, self.height))
        pygame.display.update()


# Create a class to define the Ball object
class Ball:
    def __init__(self):
        self.color = settings.BALLCOLOR
        self.posx = settings.WIDTH // 2
        self.posy = settings.HEIGHT // 2
        self.radius = settings.BALLRADIUS
        self.vel = settings.BALLVEL
        self.lives = settings.LIVES
        self.ball_rect = pygame.draw.circle(surface=WINDOW, color=self.color, center=[self.posx, self.posy], radius=self.radius)
        # Draw the circle when initialized

    def update(self, Brickobject: Brick, Blockobject: Block):
        # Redraw the circle object each time update is called to new x,y center positions
        self.ball_rect = pygame.draw.circle(surface=WINDOW, color=self.color, center=[self.posx, self.posy], radius=self.radius)
        # Check for collisions 
        self.checkBrickCollision(Brickobject)
        self.checkWindowCollision()
        self.checkBlockCollision(Blockobject)
        # Update the position of the Ball based on its velocity
        self.posx += self.vel[0]
        self.posy += self.vel[1]
        return

    def checkBrickCollision(self,Brickobject:Brick):
        for brick in Brickobject.listOfBricks:
            if self.ball_rect.colliderect(brick):
                Brickobject.listOfBricks.remove(brick)
                settings.SCORE += settings.SCOREINCREMENT
                self.vel[1] = -self.vel[1]
        return
    
    def checkBlockCollision(self,Blockobject):
    # Check for collisions with the Block and bounce off if necessary
        circle_right = self.posx + self.radius
        circle_bottom = self.posy + self.radius
        circle_left = self.posx - self.radius
        if(circle_bottom>=Blockobject.posy):
            if (circle_right >= Blockobject.posx) and (circle_left <= (Blockobject.posx + Blockobject.width)):
                    self.vel[1] = -self.vel[1]
            elif (circle_right == Blockobject.posx):
                # Collided with the left side of the block
                self.vel[0] = -self.vel[0]
            elif (circle_left == (Blockobject.posx + Blockobject.width)):
                # Collided with the right side of the block
                self.vel[0] = -self.vel[0]
        return
    
    def checkWindowCollision(self):
        # Check for collisions with the window edges and bounce off if necessary
        if self.ball_rect.left <= 0 or self.ball_rect.right >= settings.WINDOWSIZE[0]:
            self.vel[0] = -self.vel[0]
        elif self.ball_rect.top <= 0:
            self.vel[1] = -self.vel[1]
        elif self.ball_rect.bottom >= settings.WINDOWSIZE[1]:
            settings.LIVES -= 1
            self.posx = settings.WIDTH//2
            self.posy = settings.HEIGHT//2
        pass 

def Refresh(mybrick,myball,myblock):
    back_buffer = pygame.Surface(settings.WINDOWSIZE)
    back_buffer.fill(settings.BACKGROUND)
    # Draw bricks on the back buffer surface
    mybrick.draw(back_buffer)
    # Draw the ball on the back buffer surface
    pygame.draw.circle(back_buffer, myball.color, (myball.posx, myball.posy), myball.radius)
    # Draw the block on the back buffer surface
    pygame.draw.rect(back_buffer, myblock.color, (myblock.posx, myblock.posy, myblock.width, myblock.height))
    # Blit the score text on the back buffer surface
    myball.update(mybrick, myblock)
    myblock.update()
    # Swap the back buffer and the main window surface
    WINDOW.blit(back_buffer, (0, 0))
    pygame.display.flip()  # Update the window display


def main():
    # Create instances of the Block, Brick, and Ball objects
    myblock = Block()
    mybrick = Brick()
    myball = Ball()
    mybrick.create_bricks()
    Mainfont = pygame.font.Font(None, 36)

    running = True
    while running:  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # Create a back buffer surface
        Refresh(mybrick,myball,myblock)
        # Update the ball, block, and brick
        # Check for game over conditions
        if settings.SCORE >= 150:
            running = False
            time.sleep(2)
        if settings.LIVES == 0:
            running = False

    pygame.quit()


# Run the main game function if this script is executed directly
if __name__ == "__main__":
    main()
