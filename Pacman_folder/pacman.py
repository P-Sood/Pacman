import pygame
import random as r
import math as m
import time as t
global screen_width, screen_height

pygame.init()


screen_width=800
screen_height=800

pacman_right = [pygame.image.load('pacman60r.png'),pygame.image.load('pacman30r.png'),pygame.image.load('pacman0.png')]
pacman_left = [pygame.image.load('pacman60l.png'),pygame.image.load('pacman30l.png'),pygame.image.load('pacman0.png')]
pacman_up = [pygame.image.load('pacman60u.png'),pygame.image.load('pacman30u.png'),pygame.image.load('pacman0.png')]
pacman_down = [pygame.image.load('pacman60d.png'),pygame.image.load('pacman30d.png'),pygame.image.load('pacman0.png')]

pacman_lives = [pygame.image.load('Pacman1L.png'),pygame.image.load('Pacman2L.png'),pygame.image.load('Pacman3L.png')]

blinky_img = pygame.image.load('blinky.png')
inky_img = pygame.image.load('inky.png')
pinky_img = pygame.image.load('pinky.png')
linky_img = pygame.image.load('linky.png')
scared_img = pygame.image.load('scared_ghost.png')
cherry_img = pygame.image.load('cherry.png')

FONT=pygame.font.SysFont("consolas",70)
font=pygame.font.SysFont("consolas",30) 
##text=font.render( 'Score: ' + str(score) ,1 , (255,255,255))
##win.blit(text,(600,10))

bg = pygame.image.load('pacman_bg.jpg')

pacman_end=pygame.mixer.Sound("pacman_end.wav")
pacman_intro=pygame.mixer.Sound("pacman_beginning.wav")
pacman_death=pygame.mixer.Sound("pacman_death.wav")
chomp_food=pygame.mixer.Sound("pacman_eatfruit.wav")
eat_ghost=pygame.mixer.Sound("pacman_eatghost.wav")
powerup=pygame.mixer.Sound("pacman_chomp.wav")

class player():
    def __init__(self,x_pos,y_pos,Char_W,Char_H,matrix_row,matrix_col):
        self.x_pos=x_pos
        self.y_pos=y_pos
        self.Char_W=Char_W
        self.Char_H=Char_H
        self.matrix_row=matrix_row
        self.matrix_col=matrix_col

        self.lives=3
        self.VEL=8
        self.left=False
        self.right=False
        self.up=False
        self.down=False
        self.walk_count=0
        self.hitbox=[self.x_pos,self.y_pos,self.Char_W,self.Char_H]

    def draw(self,win):
        if self.lives>0:

            text=font.render( 'Lives: ' ,1 , (255,255,255))
            win.blit(text,(60,5))
            win.blit(pacman_lives[self.lives-1],(160,0))
            
            if self.walk_count+1>=9:
                self.walk_count=0
                
            if self.left:
                win.blit(pacman_left[self.walk_count//3],(self.x_pos,self.y_pos))
                self.walk_count+=1
                pygame.display.update()
                
            elif self.right:
                win.blit(pacman_right[self.walk_count//3],(self.x_pos,self.y_pos))
                self.walk_count+=1
                pygame.display.update()

            elif self.down:
                win.blit(pacman_down[self.walk_count//3],(self.x_pos,self.y_pos))
                self.walk_count+=1
                pygame.display.update()
                    
            else:
                win.blit(pacman_up[self.walk_count//3],(self.x_pos,self.y_pos))
                self.walk_count+=1
                pygame.display.update()
        else:
            pacman_end.play()
            text90=FONT.render( 'GAME OVER',1 ,(255,0,0))
            win.fill((0,0,0))
            win.blit(text90,(screen_width/2-150,screen_height/2-100))
            pygame.display.update()
            pygame.time.delay(10000000)
            pygame.quit()


    def hit(self,win):

        self.x_pos=400
        self.y_pos=400
        self.matrix_row=12
        self.matrix_col=12
        self.lives-=1
        i=0
        self.left=False
        self.right=False
        self.up=False
        self.down=False
        while i<100:
            pygame.time.delay(10)
            i+=1
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    i=301
                    pacman_end.play()
                    pygame.quit()



class enemies():
    def __init__(self,x_pos,y_pos,Enem_W,Enem_H,color,matrix_row,matrix_col,img,img_scared):
        self.x_pos=x_pos
        self.y_pos=y_pos
        self.Enem_W=Enem_W
        self.Enem_H=Enem_H
        self.img=img
        self.img_scared=img_scared
        self.color=color
        self.matrix_col=matrix_col
        self.matrix_row=matrix_row

        self.visible=True
        self.start_x=x_pos
        self.start_y=y_pos
        self.start_r=matrix_row
        self.start_c=matrix_col
        self.VEL=8
        self.left=False
        self.right=False
        self.up=False
        self.down=False
        
        
        self.hitbox=[self.x_pos,self.y_pos,self.Enem_W,self.Enem_H]

    def scared(self,win):
        if self.visible:
            self.move()
            win.blit(self.img_scared,(self.x_pos,self.y_pos))


    def isKilled(self):
        if (self.visible==False):
            return True
        return False




    def killed(self,win):
        self.x_pos=0
        self.y_pos=0
        self.matrix_row=0
        self.matrix_col=0
        self.visible=False
        
        

    def hit(self,win):
        if self.visible:
            self.x_pos=400
            self.y_pos=400
            self.matrix_row=12
            self.matrix_col=12
            i=0
            self.left=False
            self.right=False
            self.up=False
            self.down=False
            while i<100:
                pygame.time.delay(10)
                i+=1
                for event in pygame.event.get():
                    if event.type==pygame.QUIT:
                        i=301
                        pacman_end.play()
                        pygame.quit()

    def reset(self,win):
    
        
        if self.visible:
            self.x_pos=self.start_x
            self.y_pos=self.start_y
            self.matrix_row=self.start_r        
            self.matrix_col=self.start_c
            win.blit(self.img,(self.start_x,self.start_y))        
            i=0
            self.left=False
            self.right=False
            self.up=False
            self.down=False



    def draw(self,win):
        if self.visible:
            self.move()
            win.blit(self.img,(self.x_pos,self.y_pos))
            self.move()

        
## did not use AI here
    def move(self):
        if self.visible:
            matrix1=movement_map(25,25)
            matrix1.map()
            if self.left==True:
                self.x_pos-=self.VEL
                self.matrix_col-=.25

            if self.right==True:
                self.x_pos+=self.VEL
                self.matrix_col+=.25

            if self.up==True:
                self.y_pos-=self.VEL
                self.matrix_row-=.25

            if self.down==True:
                self.y_pos+=self.VEL
                self.matrix_row+=.25
                
            self.ran_int=r.randint(0,101)
            self.ran_int_block=r.randint(0,101)



            
        #If right and left blocked
            if matrix1.move_map[m.ceil(self.matrix_row)][m.ceil(self.matrix_col+1)]==1 and matrix1.move_map[m.ceil(self.matrix_row)][m.ceil(self.matrix_col-1)]==1:
                self.randLeftRight = r.randint(0,101)%2
                if (self.randLeftRight==0):
                    self.y_pos+=self.VEL
                    self.matrix_row+=.25
                    self.down=True
                    self.right=False
                    self.left=False
                    self.up=False
                elif (self.randLeftRight==1):
                    self.y_pos-=self.VEL
                    self.matrix_row-=.25
                    self.up=True
                    self.right=False
                    self.left=False
                    self.down=False
              

    
        # if down and up is blocked
            if matrix1.move_map[m.ceil(self.matrix_row)+1][m.ceil(self.matrix_col)]==1 and matrix1.move_map[m.ceil(self.matrix_row)-1][m.ceil(self.matrix_col)]==1:    
                self.randUpDown = r.randint(0,101)%2
                if (self.randUpDown==0):
                    self.x_pos+=self.VEL
                    self.matrix_col+=.25
                    self.right=True
                    self.down=False
                    self.left=False
                    self.up=False
                elif (self.randUpDown==1):
                    self.x_pos-=self.VEL
                    self.matrix_col-=.25
                    self.left=True
                    self.down=False
                    self.right=False
                    self.up=False



    #------------------------------------       This is coding based on next movement_map       ---------------------------------------
            ##RIGHT
            if self.ran_int%4==0 and matrix1.move_map[m.ceil(self.matrix_row)][m.ceil(self.matrix_col+1)]==0 and self.matrix_col<23:
                self.x_pos+=self.VEL
                self.matrix_col+=.25
                self.right=True
                self.down=False
                self.left=False
                self.up=False
            ##LEFT
            elif self.ran_int%4==1 and matrix1.move_map[m.ceil(self.matrix_row)][m.ceil(self.matrix_col-1)]==0 and self.matrix_col>1:
                self.x_pos-=self.VEL
                self.matrix_col-=.25
                self.left=True
                self.down=False
                self.right=False
                self.up=False
            ##DOWN
            elif self.ran_int%4==2 and matrix1.move_map[m.ceil(self.matrix_row+1)][m.ceil(self.matrix_col)]==0 and self.matrix_row<23:
                self.y_pos+=self.VEL
                self.matrix_row+=.25
                self.down=True
                self.right=False
                self.left=False
                self.up=False
            ##UP
            elif self.ran_int%4==3 and matrix1.move_map[m.ceil(self.matrix_row-1)][m.ceil(self.matrix_col)]==0 and self.matrix_row>1:
                self.y_pos-=self.VEL
                self.matrix_row-=.25
                self.up=True
                self.down=False
                self.left=False
                self.right=False



class movement_map():
##OUR MATRIX IS 25*25 WHICH MEANS EACH POSIITON IN THE MATRIX WILL BE 32 PIXELS BIG
## THEREFORE WE JUST NEED TO CODE WHERE PACMAN CAN WALK WITH ZEROES AND ITLL BE fine



##Remember that moving in x direction you are actually moving columns and in the y you are moving rows


    def __init__(self,numRows,numCols):
        self.numRows=numRows
        self.numCols=numCols
        self.move_map=[[1 for x in range(self.numRows)] for y in range(self.numCols)]
    def map(self):
#HORIZONTAL

        for k in range (2,23):
            self.move_map[21][k] = 0
            self.move_map[22][k] = 0
            self.move_map[13][k]=0
            self.move_map[12][k]=0 #Center

            self.move_map[7][k] =0
            self.move_map[8][k] =0 #CenterAbove
            self.move_map[16][k]=0#CenterBelow
            self.move_map[17][k] = 0
            self.move_map[1][k]=0
            self.move_map[2][k] = 0

        for k in range (8,16):
            self.move_map[1][k] = 0 #TOPRIGHT
            self.move_map[2][k] = 0



        for k in range (16,23):
            self.move_map[4][k] = 0
            self.move_map[5][k] = 0#TOPRIGHT

        for k in range (3,8):


            self.move_map[4][k] = 0
            self.move_map[5][k] = 0#TOPLEFT



#VERTICAL
        for j in range(1,23):
            # self.move_map[j][12]=0 #Center
            self.move_map[j][8]=0 #CenterLEFT
            self.move_map[j][9]=0
            self.move_map[j][16]=0
            self.move_map[j][17]=0#CenterRIGHT

        for j in range (8,22):
            self.move_map[j][12]=0 #Center
            self.move_map[j][13]=0

        for j in range (16, 22):
            self.move_map[j][2] = 0 #TOPRIGHT
            self.move_map[j][22] = 0 #BOTTOMRIGHT

        for j in range (2,22):
            self.move_map[j][2] = 0  #TOPLEFT
            self.move_map[j][3] = 0
            self.move_map[j][22] = 0#BOTTOMLEFT
            self.move_map[j][21] = 0






class food_map():
#Essentialy the same as movement map as food will only allign along areas of movement
# Coins will be placed at every matrix point

    def __init__(self,x_pos,y_pos,Radius):
        self.x_pos=x_pos
        self.y_pos=y_pos
        self.Radius=Radius
        self.visible=True

    def draw(self,win):
        pygame.draw.circle(win,(255,255,255),(self.x_pos,self.y_pos),self.Radius)

#       This class draws all the walls
class background_map():


    def __init__(self):
        self.flag=True

    def draw_walls(self,win):
        matrix2=movement_map(25,25)
        matrix2.map()
        for k in range(25):
            for j in range (25):
                if matrix2.move_map[k][j]==0:
                    pygame.draw.rect(win, (255,0,255) , (32*j,32*k,32,32))
                else:
                    pygame.draw.rect(win, (0,0,0) , (32*j,32*k,32,32))
                    #This makes it so i dont need a black background
                    

class coin_map():
#Essentialy the same as movement map as food will only allign along areas of movement
# Coins will be placed at every matrix point

    def __init__(self,x_pos,y_pos,Radius):

        self.x_pos=x_pos
        self.y_pos=y_pos
        self.Radius=Radius
        self.visible=True

    def draw(self,win):
        win.blit(cherry_img,(self.x_pos,self.y_pos))

def main():
    ## define variables and instances here

    clock=pygame.time.Clock()


    cherry=False
    win=pygame.display.set_mode((screen_width, screen_height))
    pacman=player(400,400,32,32,12,12)
    
    blinky=enemies(448,384,32,32,(255,0,0),12,14,blinky_img,scared_img)
    inky=enemies(576,384,32,32,(0,0,255),12,18,inky_img,scared_img)
    pinky=enemies(128,384,32,32,(255,20,147),12,4,pinky_img,scared_img)
    linky=enemies(256,384,32,32,(255,140,0),12,8,linky_img,scared_img)
    
    pygame.display.set_caption("Pacman")
    matrix=movement_map(25,25)
    matrix.map()
    food_list=[]
    coin_list=[]

#HORIZON food made here

    for k in range(2,22,1):
        food_list.append(food_map(32*k+32,32*13,5))
        food_list.append(food_map(32*k+32,32*8,5))
        food_list.append(food_map(32*k+32,32*17,5))
        food_list.append(food_map(32*k+32,32*22,5))


    for k in range (16, 22,1):
        food_list.append(food_map(32*k+32,32*5,5))

    for k in range (2, 4, 1):
         food_list.append(food_map(32*k+32,32*5,5))

    for k in range (6, 9, 1):
         food_list.append(food_map(32*k+32,32*5,5))

    for k in range (9, 11, 1):
         food_list.append(food_map(32*k+32,32*2,5))

    for k in range (13, 16, 1):
         food_list.append(food_map(32*k+32,32*2,5))

    coin_list.append(coin_map(32*12+32,32*2,5))
    coin_list.append(coin_map(32*5+32,32*5,5))

    #VERTICAL
    for j in range(1,22, 1):
        food_list.append(food_map(32*9,32*j+32,5))
        food_list.append(food_map(32*17,32*j+32,5))
        food_list.append(food_map(32*22,32*j+32,5))

    for j in range (4,12,1):
        food_list.append(food_map(32*3,32*j+32,5))

    for j in range (14,22,1):
        food_list.append(food_map(32*3,32*j+32,5))


    for j in range (8,17,1):
        food_list.append(food_map(32*13,32*j+32,5))

    for j in range (19,22,1):
        food_list.append(food_map(32*13,32*j+32,5))

    coin_list.append(coin_map(32*3,32*13+32,5))
    coin_list.append(coin_map(32*13,32*18+32,5))
    

    food_list_iter1=len(food_list)
    score=-2
    background=background_map()

    def redrawGameWindow():
        text=font.render( 'Score: ' + str(score) ,1 , (255,255,255))
        background.draw_walls(win)
        pacman.draw(win)
        for food in food_list:
            food.draw(win)
        for coin in coin_list:
            coin.draw(win)
        
        if cherry==True:
            blinky.scared(win)
            linky.scared(win)
            inky.scared(win)
            pinky.scared(win)
        else:
            blinky.draw(win)
            inky.draw(win)
            pinky.draw(win)
            linky.draw(win)
            
    
        win.blit(text,(582,5))

        pygame.display.update()

    
        

    text3=FONT.render( 'PRESS ENTER TO START',1 ,(255,255,255))
    win.blit(text3,(screen_width/2-399,screen_height/2-100))
    pygame.display.update()
    pygame.time.delay(1000)
    run=False
    i=0
    while i<1000000:
        for event in pygame.event.get():
            i+=1
            if event.type==pygame.QUIT:
                pacman_end.play()
                text11=FONT.render( 'GAME OVER',1 ,(255,0,0))
                win.fill((0,0,0))
                win.blit(text11,(screen_width/2-150,screen_height/2-100))
                pygame.display.update()
                pygame.time.delay(10000000)
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pacman_intro.play()
                    i=1000001
                    win.fill((0,0,0))
                    text20=FONT.render( 'P A C M A N',1 ,(255,255,51))
                    win.blit(text20,(screen_width/2-200,screen_height/2))
                    pygame.display.update()
                    pygame.time.delay(1500)
                    run=True


    while run:
        clock.tick(36)
        keys=pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                text1=FONT.render( 'GAME OVER',1 ,(255,0,0))
                win.fill((0,0,0))
                pacman_end.play()
                win.blit(text1,(screen_width/2-150,screen_height/2-100))
                pygame.display.update()
                pygame.time.delay(1000)
                run=False
                pygame.quit()
##            if event.type==pygame.K_LEFT:


        for food in food_list:
            if food.y_pos-food.Radius<pacman.y_pos+pacman.Char_H and food.y_pos+food.Radius>pacman.y_pos:
##                print(pacman.x_pos)
                if food.x_pos+food.Radius>pacman.x_pos and food.x_pos-food.Radius<pacman.x_pos+pacman.hitbox[2]:
                    pygame.time.delay(2)
                    chomp_food.play()
                    pygame.time.delay(2)
                    food_list.pop(food_list.index(food))
                    score+=1

        for coin in coin_list:
            if coin.y_pos-coin.Radius<pacman.y_pos+pacman.Char_H and coin.y_pos+coin.Radius>pacman.y_pos:
##                print(pacman.x_pos)
                if coin.x_pos+coin.Radius>pacman.x_pos and coin.x_pos-coin.Radius<pacman.x_pos+pacman.hitbox[2]:
                    pygame.time.delay(2)
                    powerup.play()
                    pygame.time.delay(2)
                    cherry=True
                    coin_list.pop(coin_list.index(coin))

        if cherry==True:
            blinky.scared(win)
            linky.scared(win)
            inky.scared(win)
            pinky.scared(win)
                    #This is how ghosts act dependant on the abilities
            if blinky.x_pos+blinky.Enem_W>=pacman.x_pos and blinky.x_pos<=pacman.x_pos+pacman.Char_W:
                if blinky.y_pos+blinky.Enem_H>=pacman.y_pos and blinky.y_pos<pacman.y_pos+pacman.Char_H:##or man.hitbox[1]+man.hitbox[3]<=goblin.hitbox[1]+goblin.hitbox[3]:
                    blinky.hit(win)
                    blinky.killed(win)
                    inky.reset(win)
                    linky.reset(win)
                    pinky.reset(win)
                    cherry=False
                    score+=5
            elif inky.x_pos+inky.Enem_W>=pacman.x_pos and inky.x_pos<=pacman.x_pos+pacman.Char_W:
                if inky.y_pos+inky.Enem_H>=pacman.y_pos and inky.y_pos<pacman.y_pos+pacman.Char_H:##or man.hitbox[1]+man.hitbox[3]<=goblin.hitbox[1]+goblin.hitbox[3]:
                    inky.hit(win)
                    inky.killed(win)
                    blinky.reset(win)
                    linky.reset(win)
                    pinky.reset(win)
                    cherry=False
                    score+=5
            elif linky.x_pos+linky.Enem_W>=pacman.x_pos and linky.x_pos<=pacman.x_pos+pacman.Char_W:
                if linky.y_pos+linky.Enem_H>=pacman.y_pos and linky.y_pos<pacman.y_pos+pacman.Char_H:##or man.hitbox[1]+man.hitbox[3]<=goblin.hitbox[1]+goblin.hitbox[3]:
                    linky.hit(win)
                    linky.killed(win)
                    blinky.reset(win)
                    inky.reset(win)
                    pinky.reset(win)
                    cherry=False
                    score+=5
            elif pinky.x_pos+pinky.Enem_W>=pacman.x_pos and pinky.x_pos<=pacman.x_pos+pacman.Char_W:
                if pinky.y_pos+pinky.Enem_H>=pacman.y_pos and pinky.y_pos<pacman.y_pos+pacman.Char_H:##or man.hitbox[1]+man.hitbox[3]<=goblin.hitbox[1]+goblin.hitbox[3]:
                    pinky.hit(win)
                    pinky.killed(win)
                    blinky.reset(win)
                    inky.reset(win)
                    linky.reset(win)
                    cherry=False
                    score+=5

 
        else:
            if blinky.x_pos+blinky.Enem_W>=pacman.x_pos and blinky.x_pos<=pacman.x_pos+pacman.Char_W:
                if blinky.y_pos+blinky.Enem_H>=pacman.y_pos and blinky.y_pos<pacman.y_pos+pacman.Char_H:##or man.hitbox[1]+man.hitbox[3]<=goblin.hitbox[1]+goblin.hitbox[3]:
                    
                    blinky.reset(win)
                    inky.reset(win)
                    linky.reset(win)
                    pinky.reset(win)
                    pacman.hit(win)
                    score-=5
                    pacman_death.play()
            elif inky.x_pos+inky.Enem_W>=pacman.x_pos and inky.x_pos<=pacman.x_pos+pacman.Char_W:
                if inky.y_pos+inky.Enem_H>=pacman.y_pos and inky.y_pos<pacman.y_pos+pacman.Char_H:##or man.hitbox[1]+man.hitbox[3]<=goblin.hitbox[1]+goblin.hitbox[3]:
                    
                    blinky.reset(win)
                    inky.reset(win)
                    linky.reset(win)
                    pinky.reset(win)
                    pacman.hit(win)
                    score-=5
                    pacman_death.play()
            elif linky.x_pos+linky.Enem_W>=pacman.x_pos and linky.x_pos<=pacman.x_pos+pacman.Char_W:
                if linky.y_pos+linky.Enem_H>=pacman.y_pos and linky.y_pos<pacman.y_pos+pacman.Char_H:##or man.hitbox[1]+man.hitbox[3]<=goblin.hitbox[1]+goblin.hitbox[3]:
                    
                    blinky.reset(win)
                    inky.reset(win)
                    linky.reset(win)
                    pinky.reset(win)
                    pacman.hit(win)
                    score-=5
                    pacman_death.play()
            elif pinky.x_pos+pinky.Enem_W>=pacman.x_pos and pinky.x_pos<=pacman.x_pos+pacman.Char_W:
                if pinky.y_pos+pinky.Enem_H>=pacman.y_pos and pinky.y_pos<pacman.y_pos+pacman.Char_H:##or man.hitbox[1]+man.hitbox[3]<=goblin.hitbox[1]+goblin.hitbox[3]:
                    
                    blinky.reset(win)
                    inky.reset(win)
                    linky.reset(win)
                    pinky.reset(win)
                    pacman.hit(win)
                    score-=5
                    pacman_death.play()
        redrawGameWindow()

        if (keys[pygame.K_LEFT] or pacman.left==True) and matrix.move_map[m.ceil(pacman.matrix_row)][m.ceil(pacman.matrix_col-1)]==0 and pacman.matrix_col>1:
            pacman.matrix_col-=.25
            pacman.x_pos -= pacman.VEL
            pacman.walk_count+=1
            pacman.left=True
            pacman.right=False
            pacman.up=False
            pacman.down=False




        if (keys[pygame.K_RIGHT] or pacman.right==True) and matrix.move_map[round(pacman.matrix_row)][m.ceil(pacman.matrix_col+1)]==0 and pacman.matrix_col<23:
            pacman.matrix_col+=.25
            pacman.x_pos += pacman.VEL
            pacman.walk_count+=1
            pacman.left=False
            pacman.right=True
            pacman.up=False
            pacman.down=False

        if (keys[pygame.K_UP] or pacman.up==True) and matrix.move_map[m.ceil(pacman.matrix_row-1)][m.ceil(pacman.matrix_col)]==0 and pacman.matrix_row>1:
            pacman.matrix_row-=.25
            pacman.y_pos -= pacman.VEL
            pacman.walk_count+=1
            pacman.left=False
            pacman.right=False
            pacman.up=True
            pacman.down=False


        if (keys[pygame.K_DOWN] or pacman.down==True) and matrix.move_map[m.ceil(pacman.matrix_row+1)][m.ceil(pacman.matrix_col)]==0 and pacman.matrix_row<23:

            pacman.matrix_row+=.25
            pacman.y_pos += pacman.VEL
            pacman.walk_count+=1
            pacman.left=False
            pacman.right=False
            pacman.up=False
            pacman.down=True

        if (blinky.isKilled() and linky.isKilled() and inky.isKilled() and pinky.isKilled()):
            text1=FONT.render( 'YOU WON',1 ,(255,0,0))
            win.fill((0,0,0))
            pacman_end.play()
            win.blit(text1,(screen_width/2-150,screen_height/2-100))
            pygame.display.update()
            pygame.time.delay(1000)
            run=False
            pygame.quit()

#This is where I call everything and run it all
if __name__=='__main__':
    pygame.init()
    main()
    pygame.quit()
