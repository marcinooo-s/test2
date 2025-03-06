

from pygame import *
from random import randint
import time as real_time
import os
clock = time.Clock()
print('Czekam 1 sekundę')
real_time.sleep(1)
#background music
mixer.init()
mixer.music.load('sneaky_adventure.mp3')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
auc_sound = mixer.Sound('auc_sound1.ogg')

if not os.path.exists("fire.ogg"):
    print("Ścieżka do pliku fire.ogg nie istnieje!")
#fonts and captions
print('Próbuje zainicjować czcionki')
font.init()
font1 = font.SysFont('Arial', 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))

font2 = font.SysFont('Arial', 36)

print('Przechodzę inicjalizowania klas')
#we need the following images:
img_back = "galaxy.jpg" #game background
img_hero = "rocket.png" #hero
img_bullet = "bullet.png" #bullet
#img_enemy = "puszi2.gif" #enemy
img_enemy = 'ufo.png'

score = 0 #ships destroyed
lost = 0 #ships missed
max_lost = 3 #lose if you miss that many


#parent class for other sprites
class GameSprite(sprite.Sprite):
 #class constructor
   def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
       #Call for the class (Sprite) constructor:
       sprite.Sprite.__init__(self)


       #every sprite must store the image property
       self.image = transform.scale(image.load(player_image), (size_x, size_y))
       self.speed = player_speed


       #every sprite must have the rect \property that represents the rectangle it is fitted in
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y
 #method drawing the character on the window
   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))


#main player class
class Player(GameSprite):
   #method to control the sprite with arrow keys
   def update(self):
       keys = key.get_pressed()
       if keys[K_LEFT] and self.rect.x > 5:
           self.rect.x -= self.speed
       if keys[K_RIGHT] and self.rect.x < win_width - 80:
           self.rect.x += self.speed
 #method to "shoot" (use the player position to create a bullet there)
   def fire(self):
       bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
       bullets.add(bullet)


#enemy sprite class  
class Enemy(GameSprite):
   #enemy movement
   def update(self):
       self.rect.y += self.speed
       global lost
       #disappears upon reaching the screen edge
       if self.rect.y > win_height:
           self.rect.x = randint(80, win_width - 80)
           self.rect.y = 0
           lost = lost + 1


#bullet sprite class  
class Bullet(GameSprite):
   #enemy movement
   def update(self):
       self.rect.y += self.speed
       #disappears upon reaching the screen edge
       if self.rect.y < 0:
           self.kill()


#Create a window
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))


#create sprites
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)


monsters = sprite.Group()
for i in range(1, 6):
   monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 60, randint(1, 3))
   monsters.add(monster)


bullets = sprite.Group()


#the "game is over" variable: as soon as True is there, sprites stop working in the main loop
finish = False
#Main game loop:
run = True #the flag is reset by the window close button
start_time = real_time.time()
lost = 0
while run:
   #"Close" button press event
   for e in event.get():
       if e.type == QUIT:
           run = False
       #event of pressing the spacebar - the sprite shoots
       elif e.type == KEYDOWN:
           if e.key == K_SPACE:
               fire_sound.play()
               ship.fire()


   if not finish:
       #update the background
       window.blit(background,(0,0))


       #write text on the screen
       text = font2.render("Score: " + str(score), 1, (255, 255, 255))
       window.blit(text, (10, 20))


       text_lose = font2.render("Missed: " + str(lost), 1, (255, 255, 255))
       window.blit(text_lose, (10, 50))

       timer = font1.render(str(int(real_time.time() - start_time)), True, (255, 255, 255))
       window.blit(timer, (10, 70))
       collision_list = sprite.spritecollide(ship, monsters, False)
       for spritecol in collision_list:
           spritecol.rect.y = -20
           spritecol.rect.x = randint(0, win_width - 80)
           lost += 1

       collision_list2 = sprite.groupcollide(monsters, bullets, True, True)
       for spritecol in collision_list2:
           #dźwięk ała
           #auc_sound.play()
           monster = Enemy(img_enemy, randint(0, win_width - 80), -20, 80, 60, randint(1, 3))
           monsters.add(monster)
           score += 1
    
        
    

       #launch sprite movements
       ship.update()
       monsters.update()
       bullets.update()
       if lost >= 5:
           finish = True


       #update them in a new location in each loop iteration
       ship.reset()
       monsters.draw(window)
       bullets.draw(window)
   clock.tick(60)
   display.update()
    
   #the loop is executed each 0.05 sec
   



