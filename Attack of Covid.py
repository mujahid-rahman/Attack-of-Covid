#!/usr/bin/env python
# coding: utf-8

# In[1]:


import math
import random
import os


# In[2]:


#hides the pygame message in terminal 
os.environ['PYGAME_HIDE_SUPPORT_PROMPT']="hide"


# In[3]:


import pygame


# In[4]:


from pygame import mixer


# In[5]:


#start up pygame


# In[6]:


pygame.init()


# In[7]:


#window size set up
screen=pygame.display.set_mode((800,600))


# In[8]:


#set up a background image 
background=pygame.image.load('background.png')


# In[9]:


#sound effects 
mixer.music.load("background_song.wav")


# In[10]:


#loop music indefinitely
mixer.music.play(-1)


# In[11]:


#game name on tab
pygame.display.set_caption("Attack of Covid")


# In[12]:


#player settings and coordinates
player_img=pygame.image.load('player.png')
playerX=375
playerY=490
playerX_change=0


# In[13]:


#enemy settings
enemy_img=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
enemies_num=5


# In[14]:


for i in range(enemies_num):
    enemy_img.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(45,140))
    enemyX_change.append(4)
    enemyY_change.append(40)


# In[15]:


#bullet settings and state
bulletImg=pygame.image.load('bullet.png')
bulletX=0
bulletY=475
bulletX_change=0
bulletY_change=10
#set state to ready
bullet_state="ready"


# In[16]:


#points score and font 
score_value=0
font=pygame.font.Font('freesansbold.ttf',35)
textX=10
testY=10


# In[17]:


#gameover
end_font=pygame.font.Font('freesansbold.ttf',64)


# In[18]:


#display points on top left screen
def show_points(x,y):
    score=font.render("Points: " + str(score_value),True,(0,0,0))
    screen.blit(score,(x,y))


# In[19]:


#display game over page when player loses 
def game_over_message():
    over_text=end_font.render("COVID WON", True,(0,0,0))
    screen.blit(over_text,(210,270))


# In[20]:


#render player object
def player(x,y):
    screen.blit(player_img,(x,y))


# In[21]:


#render enemy object
def enemy(x,y,i):
    screen.blit(enemy_img[i],(x,y))


# In[22]:


#render bullet object
def shoot_bullet(x,y):
    global bullet_state
    bullet_state="fire"
    screen.blit(bulletImg,(x+16,y+10))


# In[23]:


#collsion math
def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance=math.sqrt(math.pow(enemyX-bulletX,2)+ (math.pow(enemyY-bulletY,2)))
    if distance<26:
        return True 
    else:
        return False


# In[24]:


#Loop the game 
running=True
while running:
    
    screen.fill((0,0,0))
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
            
        #deciding movements: left or right 
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                playerX_change=-5
            if event.key==pygame.K_RIGHT:
                playerX_change=5
            if event.key==pygame.K_SPACE:
                if bullet_state is "ready":
                    #release bullet sound effect if ready
                    bulletSound=mixer.Sound("shoot.wav")
                    bulletSound.play()
                    bulletX=playerX
                    shoot_bullet(bulletX,bulletY)
                    
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                playerX_change=0
                
    playerX += playerX_change
    if playerX<=0:
        playerX=0
    elif playerX>=736:
        playerX=736
        
    #enemy movements
    for i in range(enemies_num):
        
        #decides when game is over:
        
        if enemyY[i]>440:
            for j in range(enemies_num):
                enemyY[j]=2000
            game_over_message()
            break
        
enemyX[i]+= enemyX_change[i]
if enemyX_change[i]<=0:
        enemyX_change[i]=4
        enemyY[i]+= enemyY_change[i]
elif enemyX[i]>=735:
        enemyX_change[i]=-4
        enemyY[i]+=enemyY_change[i]
        
    #collision detection
collision=isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
if collision:
        #play explosion sound when hit
        explosionSound=mixer.Sound("explosion.wav")
        explosionSound.play()
        bulletY=480
        bullet_state="ready"
        score_value +=1
        enemyX[i]= random.randint(0,736)
        enemyY[i]= random.randint(50,150)
        
enemy(enemyX[i],enemyY[i],i)

#bullet movements depending on state
if bulletY <=0:
    bulletY=480
    bullet_state="ready"
    
if bullet_state is "fire":
    shoot_bullet(bulletX,bulletY)
    bulletY -= bulletY_change
    
#return functions
player(playerX,playerY)
show_points(textX,testY)
#update portions of screen
pygame.display.update()        

