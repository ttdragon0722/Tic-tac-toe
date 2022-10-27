import pygame
from pygame import Vector2
from sys import exit
from os import path
from random import randint,choice
"""
date:2022.4.27;
ooxx online!
oh no i fail

so....

date:2022.5.10;
fix
"""

#todo
# back鍵改home
# 開始鍵移中間

# 流程:home  -->介紹 <<霧面畫面>>-->開始

# block hover 改淺




#finish
# block操作微調
# restart init

# player 加粗
# 圓太鋸齒畫
# 棋子美化
# player data 改成抽屜式
# player 可以改中間一點


#基礎設置
pygame.init()
pygame.font.init()
width = 800
height = 600

grid_width = 150
grid_x,grid_y = (width/2-(grid_width*3)/2),(height/2-(grid_width*3)/2)

pygame.display.set_icon(pygame.image.load(path.join("ooxx","data","title_icon.png")))
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption(" # game")
clock = pygame.time.Clock()
fonts_name = path.join("ooxx","data","BugMaruGothic.ttc")

def lines(): # 畫線
    pygame.draw.line(screen,(0,0,0),(grid_x+grid_width,grid_y),(grid_x+grid_width,grid_y+3*grid_width),10)
    pygame.draw.line(screen,(0,0,0),(grid_x+2*grid_width,grid_y),(grid_x+2*grid_width,grid_y+3*grid_width),10)
    pygame.draw.line(screen,(0,0,0),(grid_x,grid_y+grid_width),(grid_x+3*grid_width,grid_y+grid_width),10)
    pygame.draw.line(screen,(0,0,0),(grid_x,grid_y+2*grid_width),(grid_x+3*grid_width,grid_y+2*grid_width),10)

def blocks_update(pos): # 全部格子更新
    for block_obj in blocks:
        block_obj.update(pos)

def blocks_click(): # 某個格子被點擊時鎖定點擊
    for block_obj in blocks:
        block_obj.clicked = True

def blocks_kill(): # 某個格子被點擊時鎖定點擊
    for block_obj in blocks:
        block_obj.isalive = False

def blocks_unclick(): # 解除點擊
    for block_obj in blocks:
        block_obj.clicked = False

def chat_btn_lock():
    for chat in chats:
        for btn in chat.chat_btns:
            btn.clicked = True

def chat_update(): # 對話框更新
    for chat_obj in chats:
        chat_obj.update()

def chat_fix(): # 對話框修正
    global chats
    if len(chats) >= 2 :
        temp = chats[-1] 
        chats = []
        chats.append(temp)

def draw_text(surf,text,size,x,y,color,bold=False,fix=True,shadow=False,showdow_color=None,outline=False,outline_color=None,outline_width=0): # 文字
    font=pygame.font.Font(fonts_name,size)
    if bold == True:
        font.set_bold(bold)
    text_surface=font.render(text,True,color)
    text_rect=text_surface.get_rect()
    text_rect.x=x
    text_rect.y=y
    if fix == True:
        if text_rect.right > width:
            text_rect.right = width
        if text_rect.left < 0:
            text_rect.left = 0
    if shadow == True:
        draw_text(screen,text,size,x+4,y+4,showdow_color,bold,fix)
    if outline == True:
        draw_text(screen,text,size,x+outline_width,y,outline_color,bold,fix)
        draw_text(screen,text,size,x-outline_width,y,outline_color,bold,fix)
        draw_text(screen,text,size,x,y+outline_width,outline_color,bold,fix)
        draw_text(screen,text,size,x,y-outline_width,outline_color,bold,fix)
    surf.blit(text_surface,text_rect)
    return text_rect

def button_init():
    for btn_obj in buttons:
        btn_obj.isalive = False

def start_button_init():
    for btn_obj in start_btns:
        btn_obj.isalive = False

def button_update(pos): #* 按鈕事件 & 按鈕更新
    for btn_obj in buttons:
        btn_result = btn_obj.update(pos)
        match btn_result:
            case "local":
                start_button_init()
                blocks_click()
                if len(start_btns) != 3 :
                    start_btns.append(Button("start",pygame.image.load(path.join("ooxx","data","startbtn.png")).convert_alpha(),width-90,height-175,scale=0.35))
                game.mode = "local"

            case "exit":
                pygame.quit()
                exit()

            case _:
                pass

def player_win_restart():
    for player in players:
        player.win = 0

def players_reset():
    for player in players:
        player.restart()

def start_btn_update(pos):
    for btn_obj in start_btns:
        start_btn_result = btn_obj.update(pos)
        match start_btn_result:
            case "start":
                game.now = True
                blocks_unclick()
                del start_btns[-1]
            case "replay":
                if len(start_btns) != 3:
                    grid.__init__()
                    players_reset()
                    blocks_unclick()
                    game.now = True
            case "back":
                player_win_restart()
                button_init()
                grid.__init__()
                players_reset()
                blocks_unclick()
                game.now = False
                game.crown_dir = "none"
                game.mode = "ready"

def barrage_update(): # 彈幕更新
    fix = 0
    for bar_index in range(len(barrages)):
        bar_index+=fix
        bar_obj = barrages[bar_index]
        bar_obj.update()
        if bar_obj.x > width:
            del barrages[bar_index]
            fix-=1
    barrage_spawn()

def barrage_spawn(): # 彈幕生成
    if randint(0,100) > 98:
        barrages.append(Barrage())

def turn_next():
    global turn
    if turn == 0:
        turn += 1
    elif turn == 1:
        turn -= 1

def main_btn():
    if start.update(pos) == "start":
        start.clicked = True
        game.instructions = False
        game.now = True
        blocks_unclick()
        del start_btns[-1]
    
def face():
    if game.switcher.click_time == 10:
        screen.blit(pygame.transform.scale(pygame.image.load(path.join("ooxx","data","haha.jpg")),(width,height)),(0,0))
        pygame.display.set_caption("hahahahahahahahahahahahahahahahahahahahahahahahahahahahahahaha")

class Barrage: #* 彈幕
    def __init__(self):
        self.data = [
            # "GURU靈波（●´∀｀）ノ♡","來跟我ooxx吧!!","777777777777","666666666","太狂啦","吃JJ","主播甚麼時候抽gogoro","盤起來","笑死","878787878","?","安安","副班代好帥","暴龍好可愛","井字遊戲!!","########","點擊按鈕開始遊戲!"
            "讀書會會長"
            ]
        self.color = [
            (127,255,212),(255,215,0),(255,0,0),(153,51,250),(150,150,150),(0,0,0)
        ]
        self.text = choice(self.data)
        self.text_color = choice(self.color)
        self.size = randint(30,50)
        self.x = -width/2
        self.y = randint(height/2,height/2+145)
        self.speed = randint(5,8)
    
    def update(self):
        self.x+=self.speed
        draw_text(screen,self.text,self.size,self.x,self.y,self.text_color,True,False)

class Button: #主畫面按鈕
    def __init__(self,name,img,x,y,scale=0.5):
        self.isalive = False
        self.name = name
        self.img = img
        self.img = pygame.transform.scale(self.img,(self.img.get_width()*scale,self.img.get_height()*scale))
        self.rect = self.img.get_rect( center = (x,y) )
        self.clicked = False

    def alive(self):
        if pygame.mouse.get_pressed()[0] != 1 :
            self.isalive = True

    def click(self):
        if self.clicked == False:
            self.clicked = True

    def update(self,pos):
        self.alive()
        screen.blit(self.img,(self.rect))
        if self.isalive == True:
            if self.rect.collidepoint(pos):
                if pygame.mouse.get_pressed() [0] == 1:
                    self.click()
                    return self.name

class Player: # 玩家
    def __init__(self,name,color,win,dir):
        self.name = name
        self.big = 2
        self.mid = 3
        self.small = 3
        self.color = color
        
        if self.color == (255,0,0):
            self.style = "red"
        else:
            self.style = "blue"

        self.win = win
        self.dir = dir
        self.surface = {
            "big":pygame.transform.scale(pygame.image.load(path.join("ooxx","data",f"circle_{self.style}.png")).convert_alpha(),(150,150)),
            "mid":pygame.transform.scale(pygame.image.load(path.join("ooxx","data",f"circle_{self.style}.png")).convert_alpha(),(100,100)),
            "small":pygame.transform.scale(pygame.image.load(path.join("ooxx","data",f"circle_{self.style}.png")).convert_alpha(),(50,50))
        }
        self.list = {
            "big":pygame.transform.scale(pygame.image.load(path.join("ooxx","data",f"circle_{self.style}.png")).convert_alpha(),(70,70)),
            "mid":pygame.transform.scale(pygame.image.load(path.join("ooxx","data",f"circle_{self.style}.png")).convert_alpha(),(60,60)),
            "small":pygame.transform.scale(pygame.image.load(path.join("ooxx","data",f"circle_{self.style}.png")).convert_alpha(),(50,50))
        }
    
    def restart(self):
        self.big = 2
        self.mid = 3
        self.small = 3

    def call_color(self):
        return (self.color)

    def call_stock(self,size):
        if size == "big":
            return self.big
        elif size == "mid":
            return self.mid
        elif size == "small":
            return self.small

class Player_list:
    def __init__(self,player_obj,x,y):
        self.rect = draw_text(screen,player_obj.name,50,x,y,player_obj.color,True)
        self.open_y = 1
        self.surface = pygame.Surface((self.rect.width,self.open_y))
        self.speed = 0

        self.line_a = self.rect.bottomleft
        self.line_b = self.line_a
        self.line_speed = 0

        self.player_obj = player_obj
        if self.player_obj.color == (255,0,0):
            self.shadow = (139,0,0)
        else:
            self.shadow = (0,0,139)
        self.open = False

    def line_move(self):
        new_bx = self.line_b[0] + self.line_speed
        self.line_b = (new_bx,self.line_b[1]) 

    def linea(self,au):
        self.line_speed += 0.8
        if self.line_speed > 17 :
            self.speed = 17
        if self.line_speed < 0:
            self.line_speed = 0
        
        new_bx = self.line_b[0] + self.line_speed*au
        self.line_b = (new_bx,self.line_b[1]) 

    def a(self,au):
        self.speed += 0.3
        if self.speed > 15 :
            self.speed = 15
        if self.speed < 0:
            self.speed = 0
        self.open_y += self.speed*au

    def hover(self,pos):
        if self.rect.collidepoint(pos) or self.open:
            self.a(1)
            if self.open_y >200:
                self.open_y = 200
                self.speed = 0

            if self.line_b[0] < self.rect.right:
                self.linea(1)

        else:
            self.a(-1)
            if self.open_y < 0:
                self.open_y = 0
                self.speed = 0
            
            if self.line_b[0] > self.rect.left:
                self.linea(-1)

        if self.line_a[0] > self.line_b[0]:
            self.line_speed = 0
            self.line_b = self.line_a

    def update(self,pos):
        self.surface = pygame.Surface((self.rect.width,self.open_y))
        self.surface.fill((255,255,255))
        #inner text
        big_circle = self.surface.blit(self.player_obj.list["big"],(0,10))
        draw_text(self.player_obj.list["big"],"L",30,30,15,(255,255,255),bold=True)
        big = draw_text(self.surface,f"x{self.player_obj.big}",35,big_circle.midright[0],big_circle.topright[1]+17,(0,0,0),bold=True)
        

        center = self.player_obj.list["big"].get_rect()
        center.centerx = big_circle.centerx+5
        mid_circle = self.surface.blit(self.player_obj.list["mid"],(center.x,big_circle.bottom))
        draw_text(self.player_obj.list["mid"],"M",25,25,15,(255,255,255),bold=True)
        mid = draw_text(self.surface,f"x{self.player_obj.mid}",35,big_circle.midright[0],mid_circle.topright[1]+15,(0,0,0),bold=True)

        center = self.player_obj.list["mid"].get_rect()
        center.centerx = big_circle.centerx+5
        small_circle = self.surface.blit(self.player_obj.list["small"],(center.x,mid_circle.bottom))
        draw_text(self.player_obj.list["small"],"S",25,20,10,(255,255,255),bold=True)
        small = draw_text(self.surface,f"x{self.player_obj.small}",35,big_circle.midright[0],small_circle.topright[1]+13,(0,0,0),bold=True)

        draw_text(screen,self.player_obj.name,50,self.rect.x,self.rect.y,self.player_obj.color,True,shadow=True,showdow_color=self.shadow)
        screen.blit(self.surface,self.rect.bottomleft)
        if self.line_a != self.line_b:
            pygame.draw.line(screen,(0,0,0),self.line_a,self.line_b,3)
        self.hover(pos)



class TurnsMark:  # 輪轉
    def __init__(self):
        self.triangles = {
            #topy = 10  bottom = 60 
            "mid":pygame.transform.scale(pygame.image.load(path.join("ooxx","data","triangle.png")).convert_alpha(),(64,64)),
            "left":pygame.transform.scale(pygame.image.load(path.join("ooxx","data","triangle_left.png")).convert_alpha(),(64,64)),
            "right":pygame.transform.scale(pygame.image.load(path.join("ooxx","data","triangle_right.png")).convert_alpha(),(64,64))
        }
        self.turns = ["left","right"]

    def update(self):
        if len(start_btns) != 3:
            mid = self.triangles[self.turns[turn]].get_rect()
            if turn == 1:
                mid.midright = (interface.right_name.left-10,35)
            else:
                mid.midleft = (interface.left_name.right+10,35)
            screen.blit(self.triangles[self.turns[turn]],(mid[0],mid[1]))
        else:
            pass
            # mid = self.triangles["mid"].get_rect()
            # mid.centerx = width/2
            # screen.blit(self.triangles["mid"],(mid[0],0))

class Interface: # 遊戲介面
    def __init__(self):
        self.left_name = draw_text(screen,players[0].name,50,10,10,(255,0,0),bold=True)
        self.left_crown = Crown(self.left_name.right,self.left_name.y-20)
        self.right_name = draw_text(screen,players[1].name,50,width,10,(30,144,255),bold=True)
        self.right_crown = Crown(self.right_name.left-100,self.right_name.y-20)
        self.sizes = ["big","mid","small"]
        self.radiuses = {
            "big":30,"mid":20,"small":10
        }

        self.left_list = Player_list(players[0],10,10)
        self.right_list = Player_list(players[1],670,10)


    def set_up(self):
        if game.instructions == False:
            self.left_list.update(pos)
            self.right_list.update(pos)

        draw_text(screen,str(players[0].win),50,width/2-50,10,players[0].call_color(),bold=True)
        draw_text(screen,":",50,width/2-10,10,(0,0,0),bold=True)
        draw_text(screen,str(players[1].win),50,width/2+30,10,players[1].call_color(),bold=True)

    def updata(self):
        self.set_up()

class Grid: # 遊戲格子
    def __init__(self):
        #3x3
        self.data = [
            Vector2(0,0),Vector2(1,0),Vector2(2,0),
            Vector2(0,1),Vector2(1,1),Vector2(2,1),
            Vector2(0,2),Vector2(1,2),Vector2(2,2)]
        self.saved = [ # player,size,object
            [[],[],[]],
            [[],[],[]],
            [[],[],[]]
        ]
        
    def update(self):
        for y in range(len(self.saved)):
            for x in range(len(self.saved[y])):
                if self.saved[y][x] != []:
                    circle = self.saved[y][x][2].surface[self.saved[y][x][1]].get_rect()
                    circle.centerx = grid_x+x*grid_width+77
                    circle.centery = grid_y+y*grid_width+75
                    screen.blit(self.saved[y][x][2].surface[self.saved[y][x][1]],(circle.x,circle.y))


class Block: # 遊戲格子點擊
    def __init__(self,pos,x,y) :
        self.block_pos = pos
        self.rect = pygame.Rect(x,y,grid_width,grid_width)
        self.color = (255,255,255)
        self.clicked = True
        self.isalive = False

    def alive(self):
        if pygame.mouse.get_pressed()[0] != 1 :
            self.isalive = True

    def hover(self,pos):
        if self.rect.collidepoint(pos):
            self.color = (192,192,192)
            if pygame.mouse.get_pressed() [0] == 1 and self.clicked == False:
                self.click(pos)
        else:
            self.color = (255,255,255)

    def click(self,pos):
        chats.append(Chat(pos,self.block_pos))
        blocks_click()

    def update(self,pos):
        self.alive()
        pygame.draw.rect(screen,self.color,self.rect)
        if self.isalive == True:
            self.hover(pos)

chats = []
class Chat: # 對話框
    def __init__(self,pos,block_pos):
        self.block_pos = block_pos
        self.img = pygame.image.load(path.join("ooxx","data","chat.png")).convert_alpha()
        self.img = pygame.transform.scale(self.img,(300,150))
        self.rect = self.img.get_rect()
        self.rect.centerx = pos[0]
        self.rect.top = pos[1]
        if self.rect.bottom > height:
            self.rect.bottom = height

        self.chat_btns = [
            Chat_btn(self.rect.x+35+10,self.rect.y+45,"big",self.block_pos),
            Chat_btn(self.rect.x+35+75+10,self.rect.y+45,"mid",self.block_pos),
            Chat_btn(self.rect.x+35+75+75+10,self.rect.y+45,"small",self.block_pos)
        ]

    def chat_btn_update(self):
        for btn in self.chat_btns:
            btn.update(pos)

    def update(self):
        screen.blit(self.img,self.rect)
        self.chat_btn_update()
        
class Chat_btn: # 對話框的按鈕
    def __init__(self,x,y,size,block_pos):
        self.block_pos = block_pos
        self.rect = pygame.Rect(x,y,70,70)
        self.center = (x+35,y+35)
        self.color = (255,255,255)
        self.ori_color = self.color
        self.size_model = {
            "big":32,"mid":23,"small":15
        }
        self.name = {
            "big":"L","mid":"M","small":"S"
        }
        self.size = size
        self.alive = False
        self.clicked = False
        blocks_click()
        if players[turn].call_stock(self.size) <= 0:
            self.ori_color = (120,120,120)
            self.color = self.ori_color
            self.clicked = True
    

        if grid.saved[int(self.block_pos.y)][int(self.block_pos.x)] != []:
            if size_compare[grid.saved[int(self.block_pos.y)][int(self.block_pos.x)][1]] >= size_compare[self.size] :
                self.ori_color = (120,120,120)
                self.color = self.ori_color
                self.clicked = True
    
    def hover(self,pos):
        if self.rect.collidepoint(pos):
            self.color = (192,192,192)
            if self.alive == True:
                if pygame.mouse.get_pressed() [0] == 1 and self.clicked == False:
                    self.click()
                    chats.clear()
        else:
            if self.alive == True:
                self.color = self.ori_color
                if pygame.mouse.get_pressed() [0] == 1:
                    chats.clear()
                    blocks_kill()
                    blocks_unclick()

    def click(self):
        chat_btn_lock()
        grid.saved[int(self.block_pos.y)][int(self.block_pos.x)] = [players[turn].color,self.size,players[turn]]
        if self.size == "big":
            players[turn].big -= 1
        elif self.size == "mid":
            players[turn].mid -= 1
        else:
            players[turn].small -= 1
        turn_next()

    def update(self,pos):
        if pygame.mouse.get_pressed() [0] == False:
            self.alive = True
        pygame.draw.rect(screen,self.color,self.rect)
        rect = players[turn].list[self.size].get_rect()
        rect.center = self.center
        screen.blit(players[turn].list[self.size],rect)
        self.hover(pos)

class Crown:
    def __init__(self,x,y):
        self.images = [
            pygame.transform.scale(pygame.image.load(path.join("ooxx","data","crown0.png")).convert_alpha(),(92,67)),
            pygame.transform.scale(pygame.image.load(path.join("ooxx","data","crown1.png")).convert_alpha(),(92,67))]
        self.index= 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.time = 100

    def update(self):
        if (now_time-self.time) % 1000 <= 15:
            self.index += 1 
            self.time = now_time
            if self.index >= len(self.images):
                self.index = 0
            self.image = self.images[self.index]
        screen.blit(self.image,self.rect)

class Switching:
    def __init__(self,x,y):
        self.click_time = 0
        self.x = x
        self.y = y

        self.color = (255,255,255)
        self.hover_color = (192,192,192)

        self.background_width = 88
        self.background_height = 38
        self.background = pygame.Rect(x,y,self.background_width,self.background_height)

        self.color_change = 0
        self.inner_color = (255, 204, 0) #on
        self.inner_color = (0,52,112) #oFF
        self.on_off = {
            "on":(255, 204, 0),
            "off": (0,52,112)}
        self.inner_width = 82
        self.inner_height = 32
        self.inner = pygame.Rect(x+4,y+2,self.inner_width,self.inner_height)
        
        self.mode = "off"
        self.stick_pos = self.x+self.background_width,self.y+self.background_height/2
        self.clicked = False
        self.moving = False
        self.move_speed = 0

    def background_draw(self):
        pygame.draw.rect(screen,(0,0,0),self.background)
        pygame.draw.circle(screen,(0,0,0),(self.x,self.y+(self.background_height/2)),self.background_height/2)
        pygame.draw.circle(screen,(0,0,0),(self.x+self.background_width,self.y+(self.background_height/2)),self.background_height/2)

    def inner_draw(self):
        pygame.draw.rect(screen,self.inner_color,self.inner)
        pygame.draw.circle(screen,self.inner_color,(self.x+2,self.y+(self.inner_height/2)+2),self.inner_height/2)
        pygame.draw.circle(screen,self.inner_color,(self.x+4+self.inner_width,self.y+(self.inner_height/2)+2),self.inner_height/2)

    def a(self):
        if self.move_speed < 13:
            self.move_speed += 6

    def anim(self):
        if self.moving == True and self.mode == "off":
            if self.stick_pos[0] > self.x:
                self.stick_pos = (self.stick_pos[0]-self.move_speed,self.stick_pos[1])
                self.a()
            else:
                self.mode = "on"
                self.clicked = False
                self.moving = False
                self.move_speed = 0
                self.color_change = 0
        elif self.moving == True and self.mode == "on":
            if self.stick_pos[0] < self.x+self.background_width:
                self.stick_pos = (self.stick_pos[0]+self.move_speed,self.stick_pos[1])
                self.a()

            else:
                self.mode = "off"
                self.clicked = False
                self.moving = False
                self.move_speed = 0
                self.color_change = 0

    def stick(self):
        if self.moving != True:
            if self.mode == "on":
                draw_text(screen,"SHOW",25,self.x+30,self.y+5,(255,255,255),bold=True,outline=True,outline_color=(0,0,0),outline_width=2)
            else:
                draw_text(screen,"HIDE",25,self.x,self.y+5,(255,255,255),bold=True,outline=True,outline_color=(0,0,0),outline_width=2)
        pygame.draw.circle(screen,self.color,self.stick_pos,self.inner_height/2+4)
        swicher = pygame.draw.circle(screen,(0,0,0),self.stick_pos,self.inner_height/2+4,3)
        if swicher.collidepoint(pos):
            self.color = self.hover_color
            if (pygame.mouse.get_pressed() [0] == 1 and self.clicked == False) :
                self.click_time += 1
                if self.mode == "on":
                    self.inner_color = self.inner_color = self.on_off["off"]
                    interface.left_list.open =False
                    interface.right_list.open =False
                else:
                    self.inner_color = self.on_off["on"]
                    interface.left_list.open = True
                    interface.right_list.open = True
                self.moving = True    
                self.clicked = True
        else:
            self.color = (255,255,255)

    def update(self):
        self.background_draw()
        self.inner_draw()
        self.stick()
        self.anim()

size_compare = {
    "big":3,"mid":2,"small":0
}

#主畫面初始化
title = pygame.image.load(path.join("ooxx","data","title.png")).convert_alpha()
buttons = [
    Button("local",pygame.image.load(path.join("ooxx","data","local.png")).convert_alpha(),width*2/5-50+25,height/2+220,scale=0.3),
    Button("exit",pygame.image.load(path.join("ooxx","data","exit.png")).convert_alpha(),width*5/6-180+25,height/2+220,scale=0.3)
    ]
barrages = [
    Barrage()
]


#game start
players = [
    Player("DICK",(255,0,0),0,"left"),Player("FUCK",(30,144,255),0,"right")]
grid = Grid()
interface = Interface()
start_btns = [
    Button("back",pygame.image.load(path.join("ooxx","data","backbtn.png")).convert_alpha(),90,height-100,scale=0.35),
    Button("replay",pygame.image.load(path.join("ooxx","data","replaybtn.png")).convert_alpha(),width-90,height-100,scale=0.35),
    Button("start",pygame.image.load(path.join("ooxx","data","startbtn.png")).convert_alpha(),width-90,height-175,scale=0.35)
    ]
start = Button("start",pygame.image.load(path.join("ooxx","data","startbtn.png")).convert_alpha(),width-180,height-155,scale=0.65)
turns_mark = TurnsMark()
blocks = []
for blocks_pos in grid.data:
    blocks.append(Block(blocks_pos,grid_x+blocks_pos.x*grid_width,grid_y+blocks_pos.y*grid_width))
turn = 0

class GameManager:
    def __init__(self):
        self.mode = "ready"
        self.now = True
        self.switcher = Switching(width/2+270,height-60)
        self.crown_dir = "none"
        self.instructions = True 
        self.show = False

    def ready(self):
        screen.blit(title,(width/2-title.get_width()/2,-120))
        button_update(pos)
        barrage_update()

    def local(self):
        if self.show == False:
            turns_mark.update()
            if game.instructions == False:
                blocks_update(pos)  # 格子更新
            
            
            grid.update()
            interface.updata() 
            lines() 

            if game.instructions == True:
                main_btn()
            if game.instructions == False:
                start_btn_update(pos)
                chat_update()
                chat_fix()
                self.switcher.update()
            if self.now == True:
                self.game_over()
            else:
                if self.crown_dir == "none":
                    pass
                elif self.crown_dir == "right":
                    interface.right_crown.update()
                elif self.crown_dir == "left":
                    interface.left_crown.update()

        face()
    def game_over(self):
        try:
            if grid.saved[0][0][0] == grid.saved[0][1][0] == grid.saved[0][2][0]:
                self.isover(grid.saved[0][0][2])
        except:
            pass
        try:
            if grid.saved[1][0][0] == grid.saved[1][1][0] == grid.saved[1][2][0]:
                self.isover(grid.saved[1][0][2])
        except:
            pass
        try:
            if grid.saved[2][0][0] == grid.saved[2][1][0] == grid.saved[2][2][0]:
                self.isover(grid.saved[2][0][2])
        except:
            pass
        try:
            if grid.saved[0][0][0] == grid.saved[1][0][0] == grid.saved[2][0][0]:
                self.isover(grid.saved[0][0][2])
        except:
            pass
        try:
            if grid.saved[0][1][0] == grid.saved[1][1][0] == grid.saved[2][1][0]:
                self.isover(grid.saved[0][1][2])
        except:
            pass
        try:
            if grid.saved[0][2][0] == grid.saved[1][2][0] == grid.saved[2][2][0]:
                self.isover(grid.saved[0][2][2])
        except:
            pass
        try:
            if grid.saved[0][0][0] == grid.saved[1][1][0] == grid.saved[2][2][0]:
                self.isover(grid.saved[0][0][2])
        except:
            pass
        try:
            if grid.saved[2][0][0] == grid.saved[1][1][0] == grid.saved[0][2][0]:
                self.isover(grid.saved[2][0][2])
        except:
            pass

    def isover(self,who):
        blocks_click()
        who.win +=1
        if who.dir == "right":
            self.crown_dir = "right"
        if who.dir == "left":
            self.crown_dir = "left"
        self.now = False

game = GameManager()

while True:
    now_time = pygame.time.get_ticks()
    pos = pygame.mouse.get_pos()
    screen.fill((255,255,255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit
            exit()

    match game.mode:
        case "ready":
            game.ready()
        case "local":
            game.local()
            if game.instructions:
                screen.blit(pygame.image.load(path.join("ooxx","data","black.png")),(0,0))
                start.update(pos)

    pygame.display.update()
    clock.tick(60)
