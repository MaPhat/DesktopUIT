import pygame as pg
import random as rd

#const#
speed = 200
dis = 8
height = 320
height_scr = height + 2 * dis
#-----#


Sn_h = pg.image.load(r'.\Picture\Sn_h.png')
Sn_b = pg.image.load(r'.\Picture\Sn_b.png')
Point = pg.image.load(r'.\Picture\Point.png')
Start = pg.image.load(r'.\Picture\Start.png')
step_x = 0
step_y = 0
p_x = 0
p_y = 0

maps = []
mp_index = 2
with open('./map.txt','r') as file:
    map = file.read()
for item in map.split('\n'):
    maps.append(item)

def strtomap(map):
    walls = []
    map = list(map.split(' '))
    index = 0
    while index < len(map):
        walls.append([int(map[index]),int(map[index + 1]),int(map[index + 2]),int(map[index + 3]),int(map[index + 4])])
        index += 5
    return walls

for i in range(len(maps)):
    maps[i] = strtomap(maps[i])

class snake:
    def __init__(self,Role,x,y):
        self.Role = Role
        self.x = x
        self.y = y
    def move(self,x,y):
        self.x = x
        self.y = y
    def local(self):
        return self.Role,self.x,self.y
    
def moveSn(Sns,step_x,step_y):
    Role,x,y = Sns[0].local()
    Sns[0].move(x + step_x,y + step_y)
    l = len(Sns)
    for index in range(1,l):
        Role,x_2,y_2 = Sns[index].local()
        Sns[index].move(x,y)
        x = x_2
        y = y_2
    return Sns

def addBody(Sns,Role,step_x,step_y):
    R,x,y = Sns[-1].local()
    Sn_b = snake(Role,x - step_x,y - step_y)
    Sns.append(Sn_b)
    return Sns

def check(Sns,mp_code):
    r,x,y = Sns[0].local()
    if x >= height_scr - dis or x <= 0 or y <= 0 or y >= height_scr - dis:
        return False
    if mp_code[(int(x/8 - 1) // 4)][(int(y/8 - 1) // 4)] == 1:
        return False
    l = len(Sns)
    for index in range(1,l):
        r,x_2,y_2 = Sns[index].local()
        if(x == x_2 and y == y_2):
            return False
    return True

def ranPoint(mp_code):
    p_x = rd.choice(range(1,41))
    p_y = rd.choice(range(1,41))
    while mp_code[((p_x - 1) // 4)][((p_y - 1) // 4)] == 1:
        p_x = rd.choice(range(1,41))
        p_y = rd.choice(range(1,41))
    return p_x * dis, p_y * dis

def checkPoint(Sns,p_x,p_y):
    r,x,y = Sns.local()
    conf = False
    if x == p_x and y == p_y:
        conf = True
    return conf

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_t:
                mp_index = rd.choice(range(5))
                Token = 0
                mp_code = [[0 for _ in range(10)] for _ in range(10)]
                for wall in maps[mp_index]:
                    for i in range(wall[1],wall[1] + wall[3]):
                        for j in range(wall[2],wall[2] + wall[4]):
                            mp_code[i][j] = int(wall[0])

                p_x,p_y = ranPoint(mp_code)
                x,y = ranPoint(mp_code)
                Snk_h = snake(Sn_h,x,y)
                Sns = [Snk_h]
    screen.fill((0, 0, 0))
    pg.draw.rect(screen,((255, 0, 0)),[0,0,height_scr,height_scr],dis)

    if play:
        for item in maps[mp_index]:
            cl = (0,0,0)
            if item[0] == 1:
                cl = (0,255,0)
            w_x = item[1]
            w_y = item[2]
            d_x = item[3]
            d_y = item[4]
            pg.draw.rect(screen,cl,(w_x * 32 + dis,w_y * 32 + dis,d_x * 32,d_y * 32))

        if game_time == speed:
            Sns = moveSn(Sns,step_x,step_y)
            game_time = 0

        l = len(Sns)
        for index in range(0,l):
            Role,x,y = Sns[index].local()
            screen.blit(Role,(x,y))

        conf = checkPoint(Sns[0],p_x,p_y)
        if conf:
            addBody(Sns,Sn_b,step_x,step_y)
            p_x,p_y = ranPoint(mp_code)
            Token += 1
            if Token == 5:
                play = False
                continue
        screen.blit(Point,(p_x,p_y))

        play = check(Sns,mp_code)
        game_time += 1
    else:
        screen.blit(Start,((height_scr / 2 - 71),(height_scr / 2) - 62))

    pg.display.update()
