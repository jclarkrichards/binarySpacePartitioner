import pygame
from Primitives.vectors import Vector2
from math import sin, cos, pi   

class Player(object):
    def __init__(self, x, y):
        self.position = Vector2(x, y)
        self.facingAngle = 0 #45*pi/180
        self.movingDirection = Vector2(0,0)
        self.movingSpeed = 100
        self.turningSpeed = 360 / 1.0 #degrees / second (ex. 1 full rotation in 3 seconds)
        self.fovAngle = 40 #Field of View angle from the facingAngle direction
        self.fovRight = Vector2()  #Right-edge field of view
        self.fovLeft = Vector2() #Left-edge field of view
        self.setDirections()
        
    def update(self, dt):
        pass

    def rotateCW(self, dt):
        self.facingAngle += self.turningSpeed * dt
        self.facingAngle %= 360
        self.setDirections()
        
    def rotateCCW(self, dt):
        self.facingAngle -= self.turningSpeed * dt
        self.facingAngle %= 360
        self.setDirections()
        
    def moveForward(self, dt):
        '''Move in the direction you are facing'''
        self.position += self.facingDirection * self.movingSpeed * dt

    def moveBackward(self, dt):
        self.position -= self.facingDirection * self.movingSpeed * dt

    def strafeRight(self, dt):
        self.position += self.strafeDirection * self.movingSpeed * dt

    def strafeLeft(self, dt):
        self.position -= self.strafeDirection * self.movingSpeed * dt

    def setDirections(self):
        self.facingDirection = Vector2(cos(self.facingAngle*pi/180), sin(self.facingAngle*pi/180))
        self.fovRight = Vector2(cos((self.facingAngle+self.fovAngle)*pi/180), sin((self.facingAngle+self.fovAngle)*pi/180))
        self.fovLeft = Vector2(cos((self.facingAngle-self.fovAngle)*pi/180), sin((self.facingAngle-self.fovAngle)*pi/180))
        x, y = self.facingDirection.toTuple()
        self.strafeDirection = Vector2(-y, x)        

    def constructWalls(self, data):
        '''Getting a list of segments that may need to be drawn.  Check which segments or portion of segmetns are within field of view.  
        '''
        if type(data) is list:
            for d in data:
                print(d)
        else:
            print(data)

        print("")
        print("")
            
    def render(self, screen):
        '''Render the player as a circle with a line showing facing direction'''
        x, y = self.position.toTuple()
        x2, y2 = self.facingDirection.toTuple()
        x3, y3 = self.fovRight.toTuple()
        x4, y4 = self.fovLeft.toTuple()
        pygame.draw.circle(screen, (255,255,0), (int(x), int(y)), 10)
        pygame.draw.line(screen, (255,0,0), (x, y), (x+(x2*15), y+(y2*15)), 2)
        pygame.draw.line(screen, (255,255,255), (x, y), (x+(x3*20), y+(y3*20)), 2)
        pygame.draw.line(screen, (255,255,255), (x, y), (x+(x4*20), y+(y4*20)), 2)
