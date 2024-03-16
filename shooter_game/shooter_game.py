from pygame import *
from random import randint
from time import time as timer

score = 0                
lost = 0
max_lost = 5
life = 5
rel_time = False
num_fire = 0

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, sixe_x, size_y, player_speed):
       super().__init__()
       self.image = transform.scale(image.load(player_image), (65, 65))
       self.speed = player_speed
      # каждый спрайт должен хранить свойство rect - прямоуг., в который он вписан
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y

    def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 620:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.y = 0
            self.rect.x = randint(80, win_width - 80)
            lost += 1 

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()



#музыка йоу
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
mixer.music.set_volume(0.2)
fire_sound = mixer.Sound('fire.ogg')



img_back = 'galaxy.jpg'
img_hero = 'rocket.png'
img_enemy = 'ufo.png'
img_bullet = 'bullet.png'
img_asteroid = 'asteroid.png'


font.init()
font1 = font.SysFont(None, 80)
win = font1.render('YOU WIN!!!', True, (255,255,255))
lose = font1.render('YOU LOSE!!!', True, (180,0,0))
font2 = font.SysFont(None, 36)

score = 0
lost = 0
max_lost = 10

win_width = 700
win_height = 500
display.set_caption('шутер йоу')
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))


ship = Player(img_hero, 5, win_height - 100, 80, 50, 10)

monsters = sprite.Group()
for i in range(5):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1,5))
    monsters.add(monster)

bullets = sprite.Group()

asteroids = sprite.Group()
for i in range(3):
    asteroid = Enemy(img_asteroid, randint(30, 670), -40, 80, 50, randint(1,7))
    asteroids.add(asteroid)

finish = False
run = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 367828763623964332572475875027083 and rel_time == False:
                    num_fire += 1
                    ship.fire()
                    fire_sound.play()

                if num_fire >= 367828763623964332572475875027083 and rel_time == False:
                    last_time = timer()
                    rel_time = True


    if not finish:
        window.blit(background, (0,0))


        text = font2.render('Счёт: ' + str(score), 1, (255,255,255))
        window.blit(text, (10,20))
        text_lose = font2.render('Пропущено: ' + str(lost), 1, (255,255,255))
        window.blit(text_lose, (10,50))

        ship.update()
        monsters.update()
        bullets.update()
        asteroids.update()
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)

        if rel_time == True:
            now_time = timer() #считываем время
       
            if now_time - last_time < 3: 
                reload = font2.render('Wait, reload...', 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0   #обнуляем счётчик пуль
                rel_time = False #сбрасываем флаг перезарядки


        #если спрайт коснулся врага, уменьшает жизнь
        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship, monsters, True)
            sprite.spritecollide(ship, asteroids, True)
            life = life -1
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1,5))
            monsters.add(monster)

        if life == 0 or lost >= max_lost:
            finish = True
            window.blit(lose, (200,200))

        if score >= 30:
            finish = True
            window.blit(win, (200,200))

        text_life = font1.render(str(life), 1, (208, 0, 205))
        window.blit(text_life, (650, 10))
        display.update()

    else:
        finish = False
        score = 0
        lost = 0
        life = 5
        num_fire = 0
        rel_time = False

        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()

        for a in asteroids:
            a.kill()

        time.delay(60)
        for i in range(5):
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1,5))
            monsters.add(monster)   
        
        for i in range(3):
            asteroid = Enemy(img_asteroid, randint(30, 670), -40, 80, 50, randint(1,7))
            asteroids.add(asteroid) 

    time.delay(60)
