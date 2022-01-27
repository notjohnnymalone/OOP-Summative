###########################
#Frog-Like OOP Summative
# Reid Martin
# December 20
###########################
#1 The difference between OOP and procedural coding is that OOP
# uses objects and classes to work, while procedural coding uses plain functions
#
#2 The program would have a LOT of functions and not just little ones, long ones
# and I would have to have lists to pass arguments into it... I also just can't imagine how that would work
#
#3 With OOP you can easily pass arguements into an object without having to repeatedly set individual objects
# It is quicker than procedural coding
#
#4 The main drawback is that there is a learning curve... I still don't fully get it
# and you really have to know what you are doing to be successful with this.
######################################################################################
import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

WIDTH = 480
HEIGHT = 600
FPS = 60
POWERUP_TIME = 5000

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

x_coor =[-50, -100]
y_coor = [75, 200, 350, 475]

car = [50, 100, 150, 200]
# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shmup!")
clock = pygame.time.Clock()
win = False


font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)


def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (40, 28))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 5
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH/2
        self.rect.x = 240
        self.rect.y = 550
        self.speedx = 0
        self.speedy = 0
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()


    def update(self):

        # unhide if hidden
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.x = 240
            self.rect.y = 550

        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        if keystate[pygame.K_UP]:
            self.speedy = -8
        if keystate[pygame.K_DOWN]:
            self.speedy = 8
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            win = True
        if self.rect.left < 0:
            self.rect.left = 0



    def hide(self):
        # hide the player temporarily
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = random.choice(meteor_images)
        self.image.set_colorkey(BLACK)
#         pygame.draw.rect(self.image, RED, [0, 0, WIDTH, HEIGHT])
        self.rect = self.image.get_rect()
        self.rect.y = random.choice(y_coor)
        self.rect.x = random.choice(car)
        self.speedx = random.randrange(5,8)


    def update(self):
        self.rect.x += self.speedx
        if self.rect.left > WIDTH + 10:
            self.rect.x = -50



def show_go_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "Frog-Like", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Arrow keys move", 22,
              WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Press a key to begin", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False
                
def end_screen():#this is the big ending screen
    screen.blit(background, background_rect)
    draw_text(screen, "You Win!", 64, WIDTH/2, HEIGHT/4)
    pygame.display.flip()
# Load all game graphics
background = pygame.image.load(path.join(img_dir, "roads_final.png")).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "froggy.png")).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)
bullet_img = pygame.image.load(path.join(img_dir, "laserRed16.png")).convert()
meteor_images = []
meteor_list = ['car-truck1.png', 'car-truck2.png', 'car-truck3.png', 'car-truck4.png', 'car-truck5.png']
for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())
explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)
    filename = 'sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    explosion_anim['player'].append(img)
powerup_images = {}
powerup_images['shield'] = pygame.image.load(path.join(img_dir, 'shield_gold.png')).convert()
powerup_images['gun'] = pygame.image.load(path.join(img_dir, 'bolt_gold.png')).convert()


# Load all game sounds
player_die_sound = pygame.mixer.Sound(path.join(snd_dir, 'rumble1.ogg'))
pygame.mixer.music.load(path.join(snd_dir, 'never_good.wav'))
pygame.mixer.music.set_volume(0.4)
 
pygame.mixer.music.play(loops=-1)
# Game loop
game_over = True
running = True
while running:
    if game_over:
        show_go_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(8):
            newmob()

    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update()



    # check to see if a mob hit the player
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        newmob()
        player.hide()
        player.lives -=1
        player_die_sound.play()


    # if the player died and the explosion has finished playing
    if player.lives == 0:
        game_over = True

    # Draw / render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
