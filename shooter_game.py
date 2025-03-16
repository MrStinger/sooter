#Создай собственный Шутер!

from pygame import *
from random import randint

class GameSprite(sprite.Sprite):
    def __init__(self, img, x, y, w, h, speed):
        super().__init__()
        self.image = transform.scale(image.load(img), (w,h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def collidepoint(self,x,y):
        return self.rect.collidepoint(x,y)

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 10:
            self.rect.x-=self.speed
        if keys[K_d] and self.rect.x<700 -10- self.rect.width:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bomb.png', self.rect.centerx, self.rect.y, 30, 45, 5)
        bullets.add(bullet)
            

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > 500-self.rect.height:
            self.rect.x = randint(10, 700-10-self.rect.width)
            self.rect.y = -self.rect.height
            self.speed = randint(2,5)
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()


window = display.set_mode((700,500))
display.set_caption('Шутер')

background = transform.scale(image.load('fonc.jpg'), (700,500))

mixer.init()
mixer.music.load('theme.mp3')
mixer.music.play()

font.init()
#font1 = font.Font(None, 36)
font1 = font.SysFont('Arial', 36)


player = Player('redik.png', 320,400,110,100,5)
bullets = sprite.Group()
enemy_count = 6
enemyes = sprite.Group()

button = GameSprite('play.png', 300, 200, 100, 50, 0)

for i in range(enemy_count):
    enemy = Enemy('flypig.png', randint(10, 700-10-70), -40, 140, 140, randint(2,3))
    enemyes.add(enemy)

game = True
finish = True
menu = True
lost = 0
score = 0
clock = time.Clock()
fps = 60

while game:

    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()

    if menu:
        window.blit(background, (0,0))
        button.reset()
        pressed = mouse.get_pressed()
        pos = mouse.get_pos()
        if pressed[0]:
            if button.collidepoint(pos[0], pos[1]):
                menu = False
                finish = False

    if not finish:
        window.blit(background, (0,0))


        player.update()
        player.reset()

        enemyes.update()
        enemyes.draw(window)

        bullets.update()
        bullets.draw(window)

        lost_enemy = font1.render('Пропущено:'+str(lost), 1, (0,0,0))
        window.blit(lost_enemy, (10,10))
        score_enemy = font1.render('Убито:'+str(score), 1, (0,0,0))
        window.blit(score_enemy, (9,50))


        sprite_list = sprite.groupcollide(enemyes, bullets, True, True)
        for i in range(len(sprite_list)):
            score += 1
            enemy = Enemy('flypig.png', randint(10, 700-10-70), -40, 140, 140, randint(2,3))
            enemyes.add(enemy)


        if score>=10:
            finish = True
            text_win = font1.render('WIN!',1,(0,0,0))
            window.blit(text_win, (350, 250))

        sprite_list = sprite.spritecollide(player, enemyes, True)
        if lost >= 10 or len(sprite_list)>0:
            finish = True
            text_loose = font1.render('LOSE!',1,(0,0,0))
            window.blit(text_loose, (350, 250))


    clock.tick(fps)
    display.update()
