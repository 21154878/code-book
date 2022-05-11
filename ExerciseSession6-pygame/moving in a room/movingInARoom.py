import pygame
import math

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
SCREEN = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
CLOCK = pygame.time.Clock()

WINDOW_WIDTH = 300
WINDOW_HEIGHT = 300
MODEL_SURFACE = pygame.Surface((WINDOW_WIDTH,WINDOW_HEIGHT))
MODEL_RECT = pygame.Rect(60,50,WINDOW_WIDTH,WINDOW_HEIGHT)

VIEW_SURFACE = pygame.Surface((WINDOW_WIDTH,WINDOW_HEIGHT))
VIEW_RECT = pygame.Rect(440,50,WINDOW_WIDTH,WINDOW_HEIGHT)

FONT_NAME = pygame.font.match_font('arial')

def text(surf, text, size, x, y):
    font = pygame.font.Font(FONT_NAME, size)
    text_surface = font.render(text, True, 'white')
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def round(point):
    return (int(point[0]),int(point[1]))

def move(point,move):
    (x,y) = point
    (dx,dy) = move
    return (x + dx,y + dy)

def rotate_point(point,angle):
    (x,y) = point
    theta = math.radians(angle)
    rotated_x = x*math.cos(theta) + y*math.sin(theta)
    rotated_y = -x*math.sin(theta) + y*math.cos(theta)
    return (rotated_x,rotated_y)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.radius = 16
        self.position = (150,150)
        self.direction = 0
        self.speed = 2

        self.near_plane = ((-32,0),(32,0))

        self.original_image = pygame.Surface((32,32))
        pygame.draw.circle(self.original_image,'red',(16,16),self.radius)
        pygame.draw.line(self.original_image,'white',(16,16),(32,16))#agent

        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()



    def update(self):
        keystate = pygame.key.get_pressed()

        if keystate[pygame.K_LEFT]:
            self.direction += 3
            if self.direction > 360:
                self.direction -= 360

        if keystate[pygame.K_RIGHT]:
            self.direction -= 3
            if self.direction < 0:
                self.direction += 360

        if keystate[pygame.K_UP]:
            dx =  self.speed*math.cos(math.radians(self.direction))
            dy = -self.speed*math.sin(math.radians(self.direction))
            change_in_position = (dx,dy)
            self.position = (move(self.position,change_in_position))
            (i,j)=self.position
            # Don't update to i since it's old
            if i<=10+self.radius:
                self.position=(10+self.radius,self.position[1])
            if i>=290-self.radius:
                self.position=(290-self.radius,self.position[1])
            if j<=10+self.radius:
                self.position=(self.position[0],10+self.radius)
            if j>=290-self.radius:
                self.position=(self.position[0],290-self.radius)

        if keystate[pygame.K_DOWN]:
            dx = -self.speed*math.cos(math.radians(self.direction))
            dy =  self.speed*math.sin(math.radians(self.direction))
            change_in_position = (dx,dy)
            self.position = move(self.position,change_in_position)
            (i,j)=self.position
            if i<=10+self.radius:
                self.position=(10+self.radius,self.position[1])
            if i>=290-self.radius:
                self.position=(290-self.radius,self.position[1])
            if j<=10+self.radius:
                self.position=(self.position[0],10+self.radius)
            if j>=290-self.radius:
                self.position=(self.position[0],290-self.radius)

        self.model_to_world_transform()
        self.world_to_view_transform()

    def model_to_world_transform(self):
        #rotate before moving
        self.image = pygame.transform.rotate(self.original_image, self.direction)
        #move
        self.rect = self.image.get_rect()
        self.rect.center = round(self.position)

    def world_to_view_transform(self):
        #apply world to view transformation
        rotated_image = pygame.transform.rotate(self.original_image, 90)
        rotated_rect = rotated_image.get_rect()
        rotated_rect.center = (WINDOW_WIDTH//2,WINDOW_HEIGHT//2)

        VIEW_SURFACE.blit(rotated_image,rotated_rect)

class Wall(pygame.sprite.Sprite):
    def __init__(self,pos_a,pos_b,color):
        pygame.sprite.Sprite.__init__(self)
        self.pos_a = pos_a
        self.pos_b = pos_b
        self.color = color

        width = max(abs(pos_a[0] - pos_b[0]),1)
        height = max(abs(pos_a[1] - pos_b[1]),1)
        left = min(pos_a[0],pos_b[0])
        top = min(pos_a[1],pos_b[1])
        self.image = pygame.Surface((width,height))

        pygame.draw.line(self.image,self.color,(self.pos_a[0]-left,self.pos_a[1]-top),(self.pos_b[0]-left,self.pos_b[1]-top))
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top

    def update(self):
        self.world_to_view_transform()


    def world_to_view_transform(self):
        #find position relative to camera
        cam = (-player.position[0],-player.position[1])
        self.pos_a_view = move(self.pos_a,cam)
        self.pos_b_view = move(self.pos_b,cam)
        #rotate 90 degrees counter clockwise, then opposite camera motion
        opposite_cam = 90-player.direction
        self.pos_a_view = rotate_point(self.pos_a_view,opposite_cam)
        self.pos_b_view = rotate_point(self.pos_b_view,opposite_cam)
        pygame.draw.line(VIEW_SURFACE,self.color,round(move(self.pos_a_view,(150,150))),round(move(self.pos_b_view,(150,150))))

player = Player()
GAME_OBJECTS = pygame.sprite.Group()
RESTRICTED = pygame.sprite.Group()
GAME_OBJECTS.add(player)

wall = Wall((10,10),(290,10),'lightblue')
GAME_OBJECTS.add(wall)
RESTRICTED.add(wall)
wall = Wall((290,10),(290,290),'green')
GAME_OBJECTS.add(wall)
RESTRICTED.add(wall)
wall = Wall((290,290),(10,290),'yellow')
GAME_OBJECTS.add(wall)
RESTRICTED.add(wall)
wall = Wall((10,290),(10,10),'blue')
GAME_OBJECTS.add(wall)
RESTRICTED.add(wall)

running = True
while running:
    VIEW_SURFACE.fill('black')
    MODEL_SURFACE.fill('black')

    SCREEN.fill('black')

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running = False

    GAME_OBJECTS.update()

    GAME_OBJECTS.draw(MODEL_SURFACE)

    SCREEN.blit(MODEL_SURFACE,MODEL_RECT)
    SCREEN.blit(VIEW_SURFACE,VIEW_RECT)


    pygame.draw.rect(SCREEN,'white',MODEL_RECT,1)
    text(SCREEN,"World",16,70,20)
    pygame.draw.rect(SCREEN,'white',VIEW_RECT,1)
    text(SCREEN,"View",16,450,20)


    CLOCK.tick(60)
    fps = CLOCK.get_fps()
    pygame.display.set_caption("Running at "+str(int(fps))+" fps")
    pygame.display.update()


pygame.quit()
