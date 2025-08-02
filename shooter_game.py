#Create your own shooter
from pygame import *
from random import *
from time import time as timer

#app
win_widht = 700
win_height = 500
window = display.set_mode((win_widht,win_height))

#background
bg = image.load('galaxy.jpg') 
bg = transform.scale(bg,(700,500))
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire = mixer.Sound('fire.ogg')

#player class
class gamesprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,size_x,size_y,player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image),(size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class player(gamesprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_widht - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = peluru('bullet.png',self.rect.centerx,self.rect.top,15,20,15)
        bullets.add(bullet)
#enemy class
lost = 0 #musuh yang lewat
class enemy(gamesprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 510:
            self.rect.y = 0
            self.rect.x = randint(300,650)
            lost = lost + 1
font.init()
style =font.SysFont(None,36)
style1 = font.Font(None,100)
monsters = sprite.Group()
batu2 = sprite.Group()
for i in range (6):
    monster = enemy('ufo.png',randint(80,win_widht - 80),-40 , 80 , 50 , randint(1, 5))
    monsters.add(monster)
for i in range(3) :
    batu = enemy('asteroid.png',randint(80,win_widht - 80),-40 , 80 , 50 , randint(1,5))
    batu2.add(batu)


#bullet class
class peluru(gamesprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0 :
            self.kill()
bullets = sprite.Group()

lose = style1.render("You lose ",1,(255,0,0))
winner = style1.render("You win ",1,(0,255,0))
#loop
score = 0
win = 0
run = True
finish = False
num_fire = 0
rel_time = False
rocket = player('rocket.png',20,420,65,65,10)
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False :
                    rocket.fire()
                    num_fire += 1
                if num_fire >= 5 and rel_time == False :
                    last_time = timer()
                    rel_time = True             
    if not finish:
        window.blit(bg,(0,0))
        text_lose = style.render("Missed " + str(lost),1,(255,255,255))
        text_score = style.render('Score ' + str(score),1,(255,255,255))
        window.blit(text_lose,(10,50))
        window.blit(text_score,(10,20))
        rocket.reset()
        rocket.update()
        monsters.update()
        batu2.update()
        bullets.update()
        bullets.draw(window)
        batu2.draw(window)
        monsters.draw(window)
        if sprite.spritecollide(rocket,monsters,False) or lost >= 3 :
            finish = True
            window.blit(lose,(200,200))
        if sprite.spritecollide(rocket,batu2,False) or lost >= 3 :
            finish = True
            window.blit(lose,(200,200))
        collides = sprite.groupcollide(monsters,bullets,True,True)
        collides2 = sprite.groupcollide(batu2,bullets,True,True)
        for c in collides:
            score = score + 1
            monster = enemy('ufo.png',randint(80,win_widht - 80),-40 , 80 , 50 , randint(1, 5))
            monsters.add(monster)
            fire.play()
        for d in collides2:
            score = score + 1
            batu = enemy('asteroid.png',randint(80,win_widht - 80),-40 , 80 , 50 , randint(1, 5))
            batu2.add(batu)
            fire.play()
        if score > 10:
            finish = True
            window.blit(winner,(200,200))
        if rel_time == True :
            now_time = timer()
            if now_time - last_time < 3 :
                reload = style.render('Wait, reload...',1,(255,255,255))
                window.blit(reload,(260,460))
            else:
                num_fire = 0
                rel_time = False  
        display.update()
    time.delay(50)

