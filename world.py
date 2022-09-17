
# Import Modules
import os
import pygame as pg
# from pygame.compat import geterror


main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "data")


# functions to create our resources
def load_image(name, colorkey=None):
    fullname = os.path.join(data_dir, name)
    try:
        image = pg.image.load(fullname)
    except pg.error:
        print("Cannot load image:", fullname)
        raise SystemExit(str(geterror()))
    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pg.RLEACCEL)
    return image, image.get_rect()




pg.init()
screen = pg.display.set_mode((480, 320))
pg.display.set_caption("Super Girl")
pg.mouse.set_visible(0)

# Create The Backgound
background = pg.Surface(screen.get_size())
background = background.convert()
background.fill((50, 250, 50))

sky = pg.Surface(screen.get_size())
sky = sky.convert()
sky.fill((100, 100, 250))


class Brick(pg.sprite.Sprite):
    
    def __init__(self, index, h):
        pg.sprite.Sprite.__init__(self)  # call Sprite intializer
        self.image, self.rect = load_image("2.png", -1)
        screen = pg.display.get_surface()
        self.area = screen.get_rect()      
        self.rect.topleft = index * self.rect.width, h

class Water(pg.sprite.Sprite):
    
    def __init__(self, index, h):
        pg.sprite.Sprite.__init__(self)  # call Sprite intializer
        self.image, self.rect = load_image("17.png", -1)
        screen = pg.display.get_surface()
        self.area = screen.get_rect()      
        self.rect.topleft = index * self.rect.width, h

class Sign(pg.sprite.Sprite):
    
    def __init__(self, index, h):
        pg.sprite.Sprite.__init__(self)  # call Sprite intializer
        self.image, self.rect = load_image("Sign_2.png", -1)
        screen = pg.display.get_surface()
        self.area = screen.get_rect()      
        self.rect.topleft = index * self.rect.width, h

class Girlsprite(pg.sprite.Sprite):

    def __init__(self, x, h, filename, flip):
        pg.sprite.Sprite.__init__(self)  # call Sprite intializer
        self.image, self.rect = load_image(filename, -1)
        self.image = pg.transform.smoothscale(self.image, (128, 128))
        if flip:
            self.image = pg.transform.flip(self.image, 1, 0)
        screen = pg.display.get_surface()
        self.area = screen.get_rect()      
        self.h = h
        self.x = x
        self.rect.topleft = self.x, h
        

    

class Girl:
    state = 0 # 0 = idle, 1 = right, 2 = left

    idleSprites = []
    runSprites = []
    runSprites1 = []
    sprites = idleSprites

    frame = 0
    def __init__(self, x, h):
        for i in range(1,17):
            filename = "Idle (" + str(i) +  ").png"
            sprite=Girlsprite(x, h, filename, 0)
            self.idleSprites.append(sprite)
        for i in range(1,21):
            filename = "Run (" + str(i) +  ").png"
            sprite=Girlsprite(x, h, filename, 0)
            self.runSprites.append(sprite)
            sprite=Girlsprite(x, h, filename, 1)
            self.runSprites1.append(sprite)
        self.x = x
        self.h = h

    def currentSprite(self):
        return self.sprites[self.frame]

    def right(self):
        self.state = 1
        self.sprites = self.runSprites
        self.frame = 0
        self.currentSprite().rect.topleft = self.x, self.h
        
    
    def left(self):
        self.state = 2
        self.sprites = self.runSprites1
        self.frame = 0
        self.currentSprite().rect.topleft = self.x, self.h

    def next(self):
        if self.state == 1:
            self.x = self.x + 3            
        elif self.state == 2:
            self.x = self.x - 3
        
        self.currentSprite().rect.topleft = self.x, self.h
        self.frame = self.frame + 1
        if self.frame == len(self.sprites) - 1:
            self.frame = 0
        self.currentSprite().rect.topleft = self.x, self.h

    def stop(self):
        self.state = 0
        self.sprites = self.idleSprites
        self.frame = 0
        self.currentSprite().rect.topleft = self.x, self.h



    


going = True

brick1 = Brick(0, 200)
brick2 = Brick(1, 200)
water1 = Water(2, 250)
brick3 = Brick(3, 200)
girl1 = Girl(0, 90)
sign1 = Sign(3, 150)


clock = pg.time.Clock()

while going:
    
    sprites = pg.sprite.RenderPlain((brick1, brick2, brick3, water1, girl1.currentSprite(), sign1))

    # Draw Everything
    screen.blit(sky, (0, 0))
    screen.blit(background, (0, 50))


    sprites.update();

    sprites.draw(screen)


    pg.display.flip()

    clock.tick(24)
    girl1.next()

    for event in pg.event.get():
            if event.type == pg.QUIT:
                going = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                going = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_RIGHT:
                print("right")
                girl1.right()
            elif event.type == pg.KEYDOWN and event.key == pg.K_LEFT:
                print("left")
                girl1.left()
            elif event.type == pg.KEYDOWN and event.key == pg.K_UP:
                print("up")
            elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                girl1.stop()
pg.quit()
