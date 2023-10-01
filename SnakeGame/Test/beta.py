import pygame
import math
import random
import tkinter as tk
from tkinter import messagebox

import os # highscore issaugojimui
import pygame.mixer

pygame.init()
pygame.mixer.init()

class cube(object):
    rows = 20
    w = 500
    highscore = 0
    def __init__(self, start, dirnx=0, dirny=0, color=(74, 185, 14)):
        self.pos = start
        self.dirnx = 0
        self.dirny = 0
        self.color = color

    
    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, (89, 89, 89), (i * dis, j * dis, dis, dis))

        pygame.draw.rect(surface, self.color, (i*dis+1, j*dis+1, dis-2, dis-2))
        if eyes: # nupiesiam akis
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis + centre - radius,j*dis + 8)
            circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)


class snake(object):
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos) #nustatom gyvates galvos pozicija
        self.body.append(self.head)
        self.dirnx = 0 #direction to x
        self.driny = 1 #direction for y

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()
            
            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.driny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.driny]   #[:] - kopijuoja pozicija, kad nekeistu pagrindines

                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.driny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.driny]

                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.driny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.driny]

                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.driny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.driny]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)
            else: # tikrinam ar gyavte uzeina uz ribu, jei uzeina, tai atspawnina tam tikroje vietoje
                if c.dirnx == -1 and c.pos[0] <= 0: c.pos = (c.rows-1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows-1: c.pos = (0,c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows-1: c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0: c.pos = (c.pos[0],c.rows-1)
                else: c.move(c.dirnx,c.dirny) # jei gyvate neuzeina uz ribu, tai tiesiog juda normaliai


    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0],tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0],tail.pos[1]+1)))
 
        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True) # jei yra pirmas gyvates blokelis, tai uzdedam jam akis (nupiesiam mazas akis)
            else:
                c.draw(surface)

def drawGrid(w, rows, surface):
    sizeBtwn = w // rows
    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn

        pygame.draw.line(surface, (153, 86, 10), (x,0), (x,w))
        pygame.draw.line(surface, (153, 86, 10), (0,y), (w,y))


def redrawWindow(surface, current_score = 0, highscore = 0):
    global rows, width, s, snack
    surface.fill((115, 67, 12))

    #pygame.draw.rect(surface, (0, 0, 0), (0, 0, width, 50))      #   !TAISYTI!
    

    s.draw(surface)
    snack.draw(surface)
    drawGrid(width, rows, surface)

    pygame.font.init()  # Initialize the font module
    font = pygame.font.Font(None, 26)  # Use Pygame's font module

    current_score_text = font.render(f'Score: {current_score}', True, (255, 255, 255))
    surface.blit(current_score_text, (width - 100, 10))
    text = font.render(f'Highscore: {highscore}', True, (255, 255, 255))
    surface.blit(text, (10, 10))
    text1 = font.render("Press any arroe key to start!", True, (255, 255, 255))
    surface.blit(text1, (width - 360, 10))
    
    pygame.display.update()

def randomSnack(rows, item): 
    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            continue
        else:
            break
    
    return (x,y)

def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

def save_highscore(highscore):
    with open('highscore.txt', 'w') as file:
        file.write(str(highscore))

def load_highscore():
    if os.path.isfile('highscore.txt'):
        with open('highscore.txt', 'r') as file:
            highscore = file.read().strip()  
            if highscore.isdigit():  
                return int(highscore)
    return 0  


def main():
    global width, rows, s, snack, highscore
    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    s = snake((74, 185, 14), (10, 10))
    snack = cube(randomSnack(rows, s), color=(185, 57, 14))

    cube.highscore = load_highscore()

    flag = True

    clock = pygame.time.Clock()
    current_score = 0

    pygame.mixer.music.load("SnakeMusic1.mp3") 
    pygame.mixer.music.play(-1)
    while flag:
        pygame.time.delay(50) #nustatom gyvates greiti
        clock.tick(10) #nustatom gyvates greiti
        s.move()
        if s.body[0].pos == snack.pos: # jei gyvate suvalgo snacks (uzeina ant snack pozicijos, gyvate pailgeja vienu bloku)
            s.addCube()
            snack = cube(randomSnack(rows, s), color=(185, 57, 14))
            current_score += 1

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])):
                if current_score > cube.highscore:
                    cube.highscore = current_score
                    save_highscore(cube.highscore)
                message_box('Game Over', "Press OK To Play Again!")
                s.reset((10,10))
                current_score = 0
                pygame.mixer.music.play(-1)
                break

        redrawWindow(win, current_score, cube.highscore)


    pass



main()