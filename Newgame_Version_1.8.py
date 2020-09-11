import pygame
import pygame.mixer
import pygame.mixer_music
import os
import sys
pygame.init()
pygame.mixer.init()
pygame.font.init()


W, H = 800, 447
win = pygame.display.set_mode((W,H))
pygame.display.set_caption('Side Scroller')

bg = pygame.image.load(os.path.join('images','bg2.png')).convert()
bgX = 0
bgX2 = bg.get_width()

unistr = "❤"
uniarrow = "➳"

clock = pygame.time.Clock()

hitcount = 0

health = 6        

#win = pygame.display.set_mode((500, 480)) #screen/GUI

screenSize = 800 # var for main loop calls
pygame.display.set_caption("Scroller Game")


#hero image/sprite resource locations
walkRight = [pygame.image.load('images/R1.png'), pygame.image.load('images/R2.png'), pygame.image.load('images/R3.png'), pygame.image.load('images/R4.png'), pygame.image.load('images/R5.png'), pygame.image.load('images/R6.png'), pygame.image.load('images/R7.png'), pygame.image.load('images/R8.png'), pygame.image.load('images/R9.png')]
walkLeft = [pygame.image.load('images/L1.png'), pygame.image.load('images/L2.png'), pygame.image.load('images/L3.png'), pygame.image.load('images/L4.png'), pygame.image.load('images/L5.png'), pygame.image.load('images/L6.png'), pygame.image.load('images/L7.png'), pygame.image.load('images/L8.png'), pygame.image.load('images/L9.png')]


#bg = pygame.image.load('images/bg.jpg')


char = pygame.image.load('images/standing.png')



bulletSound = pygame.mixer.Sound('sounds/freesoundsounds/gun-shot.wav')
hitSound = pygame.mixer.Sound('sounds/hit.wav')
#punchSound = pygame.mixer.Sound('sounds/punch.wav')
#bulletSound.play()

music = pygame.mixer.music.load('sounds/music.mp3')
pygame.mixer.music.play(-1)





#player/hero class
class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.left = False
        self.right = True
        self.walkCount = 0
        self.jumpCount = 10
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52) # x,y width and height
        #self.health = str("❤️❤️❤️❤️❤️") #unused

    def draw(self,win):
        if self.walkCount + 1 >= 27: #9 sprites, prevents index error from going above 27(sprite displayed for 3 frames)
            self.walkCount = 0
        

        if not(self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount//3], (round(self.x), round(self.y))) #//3 integer devision excludes decimals/floats       #~~~FLOAT ERROR~~~# fixed
                self.walkCount += 1 #increments walkcount value
            elif self.right:
                win.blit(walkRight[self.walkCount//3], (round(self.x), round(self.y)))         #~~~FLOAT ERROR~~~# fixed
                self.walkCount += 1
        else:
            if self.right:
                win.blit(walkRight[0], (round(self.x), round(self.y))) #sets character sprite to face right while standing still              #~~~FLOAT ERROR~~~# fixed
            else:
                win.blit(walkLeft[0], (round(self.x), round(self.y))) #sets character sprite to face left while standing still
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        #pygame.draw.rect(win, (255,0,0), self.hitbox,2) # To draw the hit box around the player

    


#hit/score text bar in top right
    def hit(self): 
        self.isJump = False
        self.jumpCount = 10
        self.x = 80 # moves charcater on x axis after hit
        self.y = 310 # moves charcater on y axis after hit
        self.walkCount = 0 # sets char sprite to standing/default 
        font1 = pygame.font.SysFont('comicsans', 100)
        text = font1.render('-5', 1, (255,0,0))
        win.blit(text, (400 - (text.get_width()//2),220)) #half of screen size to find center
        pygame.display.update()
        print('hero hit')
        i = 0
        while i < 100:
            pygame.time.delay(10) #delays the display of text
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()

class projectile(object):                          #dont need to write object
    def __init__(self,x,y,radius,colour,facing):   #facing determines direction of projectile
        self.x = x
        self.y = y
        self.radius = radius
        self.colour = colour
        self.facing = facing
        self.vel = 16 * facing

    def draw(self,win):
        #win.blit(a.render(unistr,True,(0,0,0)),(128, 0))
        pygame.draw.circle(win, self.colour, (round(self.x), round(self.y)), self.radius)
        

class platforms(object):
    platformimage = pygame.image.load('platforms/brickblock64x64.png')
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = (self.x, self.y)

    def draw(self,win):
        win.blit(self.platformimage, (round(self.x) + 80, round(self.y) + 180))
        #win.blit(self.platformimage, (round(self.x), round(self.y) -  20, 50, 10))     #works

        #pygame.draw.rect(win, (255,0,0), self.hitbox,2)
        #pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))


#enemy class
class enemy(object):
    walkRight = [pygame.image.load('images/R1E.png'), pygame.image.load('images/R2E.png'), pygame.image.load('images/R3E.png'), pygame.image.load('images/R4E.png'), pygame.image.load('images/R5E.png'), pygame.image.load('images/R6E.png'), pygame.image.load('images/R7E.png'), pygame.image.load('images/R8E.png'), pygame.image.load('images/R9E.png'), pygame.image.load('images/R10E.png'), pygame.image.load('images/R11E.png')]
    walkLeft = [pygame.image.load('images/L1E.png'), pygame.image.load('images/L2E.png'), pygame.image.load('images/L3E.png'), pygame.image.load('images/L4E.png'), pygame.image.load('images/L5E.png'), pygame.image.load('images/L6E.png'), pygame.image.load('images/L7E.png'), pygame.image.load('images/L8E.png'), pygame.image.load('images/L9E.png'), pygame.image.load('images/L10E.png'), pygame.image.load('images/L11E.png')]

    def __init__(self,x,y,width,height,end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]  # This will define where our enemy starts and finishes their path.
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 10
        self.visible = True #used to make character invisible when health reaches 0
    
    def draw(self,win): #draws the goblin
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0
            
            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount //3], (round(self.x), round(self.y)))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount //3], (round(self.x), round(self.y)))
                self.walkCount += 1
            
            pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10)) #last 3 = raise 20pix above y cord of hitbox, length and height of health bar
            pygame.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (round(50/10) * (10 - self.health)), 10))
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)
            #pygame.draw.rect(win, (255,0,0), self.hitbox,2) # To draw the hit box around the enemy

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else: 
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

    """
    Enemy moves along the x axis, if you want it to move up and down, edit the y axis. (self.y)

    """

    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False
        #print('hit')
        pass

class enemy2(object):
    walkRight = [pygame.image.load('images/R1E.png'), pygame.image.load('images/R2E.png'), pygame.image.load('images/R3E.png'), pygame.image.load('images/R4E.png'), pygame.image.load('images/R5E.png'), pygame.image.load('images/R6E.png'), pygame.image.load('images/R7E.png'), pygame.image.load('images/R8E.png'), pygame.image.load('images/R9E.png'), pygame.image.load('images/R10E.png'), pygame.image.load('images/R11E.png')]
    walkLeft = [pygame.image.load('images/L1E.png'), pygame.image.load('images/L2E.png'), pygame.image.load('images/L3E.png'), pygame.image.load('images/L4E.png'), pygame.image.load('images/L5E.png'), pygame.image.load('images/L6E.png'), pygame.image.load('images/L7E.png'), pygame.image.load('images/L8E.png'), pygame.image.load('images/L9E.png'), pygame.image.load('images/L10E.png'), pygame.image.load('images/L11E.png')]

    def __init__(self,x,y,width,height,end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]  # This will define where our enemy starts and finishes their path.
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 10
        self.visible = True #used to make character invisible when health reaches 0
    
    def draw(self,win): #draws the goblin
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0
            
            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount //3], (round(self.x), round(self.y)))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount //3], (round(self.x), round(self.y)))
                self.walkCount += 1
            
            pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10)) #last 3 = raise 20pix above y cord of hitbox, length and height of health bar
            pygame.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (round(50/10) * (10 - self.health)), 10))
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else: 
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

    """
    Enemy moves along the x axis, if you want it to move up and down, edit the y axis. (self.y)

    """
    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False
        #print('hit')
        pass


#win.blit(h.render(unistr,True,(255,0,0)),(0,0))
#pygame.display.update()

def redrawGameWindow():
    win.blit(bg, (0,0)) #win.blit main method to import images
    textscore = font.render('Hits: ' + str(hitcount), 1, (255,128,0)) #defines text on screen plus print var(hitcount)
    win.blit(textscore, (700, 10)) #defines locations of hit/score text
    if health >= 1:
        win.blit(h.render(unistr,True,(255,0,0)),(0, 0))
    if health >= 2:
        #win.blit(h.render(unistr,True,(255,0,0)),(0, 0)) renders unicode heart symbol representing 1 health
        win.blit(h.render(unistr,True,(255,0,0)),(32, 0))
    if health >= 3:
        win.blit(h.render(unistr,True,(255,0,0)),(64, 0))
    if health >= 4:
        win.blit(h.render(unistr,True,(255,0,0)),(96, 0))
    if health >= 5:
        win.blit(h.render(unistr,True,(255,0,0)),(128, 0))
    if health > 5:
        win.blit(p.render("+",True,(255,0,0)),(160, 4))
    hero.draw(win)
    platform1.draw(win)
    goblin.draw(win)
    goblin2.draw(win) # looks at def draw(self,win): in enemy2
    for bullet in bullets:
        bullet.draw(win)

    pygame.display.update()#need to update to exist

# Better to draw opjects outside main loop

#main loop
a = pygame.font.Font("seguisym.ttf", 16)
h = pygame.font.Font("seguisym.ttf", 32)
p = pygame.font.SysFont('comicsans', 48)
font = pygame.font.SysFont('comicsans', 30, True, False) #First true bold, second italic
#font2 = pygame.font.SysFont('comicsans', 30, True, False)
hero = player(80, 310, 64, 64) #x y height width initial hero spawn locations
goblin = enemy(300, 310, 64, 64, 750)
goblin2 = enemy2(260, 310, 64, 64, 750) #x y height width initial spawn locations and end x cord for patrol
platform1 = platforms(64, 64, 64, 64)
shootLoop = 0
bullets = []

run = True
while run:
    clock.tick(27)

    if health == 0:
        #font2.render('Game Over', 1, (255,128,0))
        run = False

    if goblin.visible == True:
        if hero.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and hero.hitbox[1] + hero.hitbox[3] > goblin.hitbox[1]:
            if hero.hitbox[0] + hero.hitbox[2] > goblin.hitbox[0] and hero.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
                #hitSound.play()
                hero.hit()
                hitcount -= 5
                health -= 1
    
    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0
                
    if goblin2.visible == True:
        if hero.hitbox[1] < goblin2.hitbox[1] + goblin2.hitbox[3] and hero.hitbox[1] + hero.hitbox[3] > goblin2.hitbox[1]:
            if hero.hitbox[0] + hero.hitbox[2] > goblin2.hitbox[0] and hero.hitbox[0] < goblin2.hitbox[0] + goblin2.hitbox[2]:
                #hitSound.play()
                hero.hit()
                hitcount -= 5
                health -= 1

    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    for bullet in bullets:
        if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
            if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                if goblin.visible == True:
                    hitSound.play()
                    goblin.hit()
                    hitcount += 1
                    bullets.pop(bullets.index(bullet))

        if bullet.y - bullet.radius < goblin2.hitbox[1] + goblin2.hitbox[3] and bullet.y + bullet.radius > goblin2.hitbox[1]:
            if bullet.x + bullet.radius > goblin2.hitbox[0] and bullet.x - bullet.radius < goblin2.hitbox[0] + goblin2.hitbox[2]:
                if goblin2.visible == True:
                    hitSound.play()
                    goblin2.hit()
                    hitcount += 1
                    bullets.pop(bullets.index(bullet))

        """
        Checks if projectile is in hitbox of goblin. 
        bullet.y - radius < goblin.hitbox[1] + goblin.hitbox[3] = checks if above bottom of rectangle
        bullet.y + bullet.radius > goblin.hitbox[1] = checks if below top of rectangle
        bullet.x + bullet.radius > goblin.hitbox[0] = checks if projectile is on the right of the left side of rectangle
        bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2] = checks on left of right side of rectangle
        """
        if bullet.x < 750 and bullet.x > 0:   # sets bullet range before deletion
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))
    """
    keys for movement
    """
    keys = pygame.key.get_pressed()#movement based on continuous key press
    #grid values start at top left - (0,0) top right (500,0) bottom right (500,500) bottom left (0,500)
    if keys[pygame.K_SPACE] and shootLoop == 0:
        if hero.left:
            facing = -1
        else:
            facing = 1
        
        if len(bullets) < 5:
            bullets.append(projectile(round(hero.x + hero.width //2), round(hero.y + hero.height//2), 6, (255,200,0), facing))
            bulletSound.play()

        shootLoop = 1

    if keys[pygame.K_LEFT] and hero.x > hero.vel:#prevents moving off screen
        hero.x -= hero.vel
        hero.left = True
        hero.right = False
        hero.standing = False
    elif keys[pygame.K_RIGHT] and hero.x < screenSize - hero.width - hero.vel:#stops moving over right side
        hero.x += hero.vel
        hero.right = True
        hero.left = False
        hero.standing = False
    else:
        hero.standing = True
        hero.walkCount = 0

    if not(hero.isJump):
        if keys[pygame.K_UP]:#quadratic function
            hero.isJump = True
            #hero.right = False
            #hero.left = False
            hero.walkCount = 0
    else:
        if hero.jumpCount >= -10:
            neg = 1
            if hero.jumpCount < 0:
                neg = -1
            hero.y -= (hero.jumpCount ** 2) * 0.5 *neg #moves player up during jump to the power of 2
            hero.jumpCount -= 1 # moves the player down
        else:
            hero.isJump = False
            hero.jumpCount = 10

    redrawGameWindow() #calls drawing function



pygame.quit() #allows end game/exit without errors
