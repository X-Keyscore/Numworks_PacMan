# V5 | By XKeyscore
from kandinsky import *
from ion import *
from time import *
from random import randrange,choice

# Color table / (name): color()
Color={
  "BG": color(0,0,0),
  "pacman": color(255,255,0),
  "wall": color(24,24,190),
  "point": color(255,255,0),
  "ghostR": color(255,0,0),# Red
  "ghostB": color(1,255,255),# Bleu
  "ghostP": color(255,184,255),# Pink
  "ghostY": color(255,184,81),# Yellow
  "title": color(255,191,0),
  "text": color(108,52,131)
}
# Map [[x,y,size,direction]] / hauteur 13*14 = 182, largeur 23*14= 322
Map = [
  [0,3,23,0],[0,4,11,1],[0,15,23,0],[22,4,11,1],
  [18,4,1,0],[2,5,3,0],[6,5,3,0],
  [10,5,3,0],[14,5,3,0],[20,5,1,0],
  [2,6,4,1],[8,6,2,1],[14,6,4,1],
  [18,6,4,1],[4,7,3,0],[10,7,3,0],
  [16,7,2,0],[19,7,1,0],[21,7,1,0],
  [6,8,2,1],[10,8,4,1],[12,8,4,1],
  [4,9,4,1],[8,9,5,1],[16,9,3,1],
  [20,9,5,1],[1,11,1,0],[3,11,1,0],
  [5,11,2,0],[11,11,1,0],[14,11,3,1],
  [17,11,2,0],[0,11,0,0],[2,13,1,0],
  [6,13,2,0],[10,13,3,0],[15,13,2,0],
  [18,13,2,0],[4,14,1,0]
]

# Icon [[x,y,size]] / !Ordre des positions importants pour l'animation!
Icon = {
  "pacman": [
    [5,0,4],[3,1,8],[2,2,10],
    [1,3,12],[1,4,9],[0,5,7],
    [0,6,4],[0,7,4],[0,8,7],
    [1,9,9],[1,10,12],[2,11,10],
    [3,12,8],[5,13,4]
  ],
  "ghost": [
    [5,0,4],[3,1,8],[2,2,10],
    [1,3,12],[1,4,12],[1,5,12],
    [0,6,14],[0,7,14],[0,8,14],
    [0,9,14],[0,10,14],[0,11,14],
    [12,12,2],[13,13,1],[8,12,3],
    [8,13,2],[3,12,3],[4,13,2],
    [0,12,2],[0,13,1]
  ]
}

# [ FUNCTIONS ]

# Conversion
def c(a):
  return a*14

# Affichage icon / f (Number,Number,Icon,Color)
def dspIcon(x,y,ico,col): # Display Heart
  for i in ico:
      fill_rect(c(x)+i[0],c(y)+i[1],i[2],1,col)

# Affichage point de vie / f (Number)
def dspHeart(v):
  x=0;y=1;i=0
  fill_rect(c(x),c(y),c(3),c(1),Color['BG'])
  while (i < v):
    for I in Icon['pacman']:
      fill_rect(c(x+i)+I[0],21+I[1],I[2],1,Color['pacman'])
    i += 1

# Affichage score / f (Number)
def dspScore(v):
  draw_string("Score:" + str(v),c(0),c(0),Color['point'],Color['BG'])
  #draw_string(str(v),c(0),c(1),Color['point'],Color['BG'])

def convertWHB(WHB):
  conv = []
  for i,value in enumerate(WHB):
    if value:
      conv.append(i)
  return conv

# Donne une list des positions d'une couleur dans la zone de jeu (15/15)
def ColorPos(col):
  T=[];i=0
  while (i < 23):# x
    j=0
    while (j < 13):# y
      if get_pixel(c(i)+6,c(j+3)+6) == col:
        T.append([i,j+3])
      j += 1
    i += 1
  return T

# [ CLASS ]

# Stockage des données joueur
class player():
  def __init__(s,x,y,d,icon,color,heart,score):
    s.x = x
    s.y = y
    s.d = d
    s.t = monotonic()
    s.i = icon
    s.c = color
    s._heart = heart;dspHeart(heart)
    s._score = score;dspScore(score)

  def updPos(s): # Update position
    x = s.x
    y = s.y
    pos = [[x+1,y],[x,y+1],[x-1,y],[x,y-1]][s.d]
    s.x = pos[0]
    s.y = pos[1]
  def FrameTemps(s):
    if (s.t + 1) < monotonic():
      s.t = monotonic()
      return True
    return False
  def heart(s,v):
    s._heart += v
    dspHeart(s._heart)
  def score(s,v):
    s._score += v
    dspScore(s._score)

# Stockage des données des fantomes
class ghost():
  def __init__(s,x,y,d,icon,color,status):
    s.x = x
    s.y = y
    s.d = d
    s.t = monotonic() # Frame temps
    s.WHB = []
    s.oldWHB = []
    s.i = icon
    s.c = color
    s.f = 0
    s._status = status # (0)nasty (1)victim (2)dead

  # Update position
  def updPos(s): 
    pos = [[s.x+1,s.y],[s.x,s.y+1],[s.x-1,s.y],[s.x,s.y-1]][s.d]
    s.x = pos[0]
    s.y = pos[1]
  # Change direction
  def ChgDir(s): 
    if s.oldWHB != s.WHB:
      s.oldWHB = s.WHB
      s.d = choice(s.WHB)
  def FrameTemps(s):
    if (s.t + 1) < monotonic():
      s.t = monotonic()
      return True
    return False
  def Frame(s):
    if s.f > 14:
      s.f = 0
      return s.f
    actu = s.f
    s.f += 1
    return actu
  def ChgWHB(s,WHB):
    s.WHB = convertWHB(WHB)
    s.OldWHB = s.WHB
  def ChgStatus(s,v):
    s._status = v

# Calculs et stockage de l'environment de jeu
class environment():
  def __init__(s,walls,points):
    s.walls = walls
    s.points = points

  # Wall hitbox
  def wall(s,x,y):
    T=[True,True,True,True]
    # Je boucle les données des murs
    for wl in s.walls:
      wX=wl[0];wY=wl[1];wS=wl[2];
      if (wl[3] == 1):# y / Droit Gauche Haut Bas
        if x+1 == wX and wY <= y <= wY+wS-1: T[0]=False
        elif x-1 == wX and wY <= y <= wY+wS-1: T[2]=False
        elif x == wX and y == wY+wS: T[3]=False
        elif x == wX and y == wY-1: T[1]=False
      else:# x / Haut Bas Droit Gauche
        if y-1 == wY and wX <= x <= wX+wS-1: T[3]=False
        elif y+1 == wY and wX <= x <= wX+wS-1: T[1]=False
        elif y == wY and x == wX+wS: T[2]=False
        elif y == wY and x == wX-1: T[0]=False
    return T

  def point(s,x,y):
    for i, pt in enumerate(s.points):
      if pt[0] == x and pt[1] == y:
        del s.points[i]
        return True
    return False

# [ GRAPHIC ]

# Entity Render
def entityRender(x,y,D,Ico,C,i):
  B=Color['BG'];Ic=Icon[Ico];cX=x*14;cY=y*14
  if (D == 0):
    cX += i
    for I in Ic:
      fill_rect(cX+I[0]-1,cY+I[1],1,1,B)# Reset
      fill_rect(cX+I[0],cY+I[1],I[2],1,C)# Draw
  elif (D == 1):
    cY += i
    for I in Ic:
      fill_rect(cX+I[1],cY+I[0]-1,1,1,B)
      fill_rect(cX+I[1],cY+I[0],1,I[2],C)
  elif (D == 2):
    cX -= i
    for I in Ic:
      a=14-(I[2]+I[0])
      fill_rect(cX+a+I[2],cY+I[1],1,1,B)
      fill_rect(cX+a,cY+I[1],I[2],1,C)
  elif (D == 3):
    cY -= i
    for I in Ic:
      a=14-(I[2]+I[0])
      fill_rect(cX+I[1],cY+a+I[2],1,1,B)
      fill_rect(cX+I[1],cY+a,1,I[2],C)

# Entity Render Fixe
def entityRenderFixe(x,y,D,Ico,C,i):
  B=Color['BG'];Ic=Icon[Ico];cX=c(x);cY=c(y)
  pos = [[cX-1+i,cY,cX+i,cY],[cX,cY-1+i,cX,cY+i],[cX+1-i,cY,cX-i,cY],[cX,cY+1-i,cX,cY-i]][D]
  fill_rect(pos[0],pos[1],14,14,B)# Reset
  for I in Ic:
    fill_rect(pos[2]+I[0],pos[3]+I[1],I[2],1,C)# Draw

# [ Pre init. affichage ]
def preInit():
  # -Background-
  fill_rect(0, 0, 320, 222, Color['BG'])
  # -Borders and Walls-
  for wl in Map:
    # axe
    if (wl[3] == 0):# x
      fill_rect(c(wl[0]),c(wl[1]),c(wl[2]),14,Color['wall'])
    else:# y
      fill_rect(c(wl[0]),c(wl[1]),14,c(wl[2]),Color['wall'])
preInit()

# [ CALL CLASS ]

# Init. des données de map
env = environment(Map,ColorPos(Color['BG']))

# Init. player
p = player(11,12,0,'pacman',Color['pacman'],3,0)
env.point(p.x,p.y)

# Init. ghost
gR = ghost(11,6,2,'ghost',Color['ghostR'],0)

# Init. des possibilités de direction
p.WHB = env.wall(p.x,p.y)
gR.ChgWHB(env.wall(gR.x,gR.y))

# [ Init. affichage ]
def Init():
  # -Points-
  for pt in env.points:
    fill_rect(c(pt[0])+6,c(pt[1])+6,2,2,Color['point'])
Init()

# [ LOOP ]
loop = True
Frame = 0
while (loop):

  # Player
  if p.FrameTemps():
    if p.WHB[p.d]:
      entityRender(p.x,p.y,p.d,p.i,p.c, Frame)
      p.updPos()
      p.WHB = env.wall(p.x,p.y)
      if env.point(p.x,p.y):
        p.score(10)
        if len(env.points) == 0: loop = False

  #if gR.FrameTemps():
  #  frame = gR.Frame()
   # if frame == 0:
  #    gR.updPos()
  #    Init()
  #  #if gR.d in gR.WHB:
  #  entityRenderFixe(gR.x,gR.y,gR.d,gR.i,gR.c,frame)
  #  gR.ChgWHB(env.wall(gR.x,gR.y))
  #  gR.ChgDir()
   # Frame += 1

  #Action for player
  if keydown(KEY_RIGHT) and p.WHB[0]:
    # Reset icon pour le changement de direction
    fill_rect(c(p.x),c(p.y),14,14,Color['BG'])
    # Changement de la direction
    p.d=0
  elif keydown(KEY_DOWN) and p.WHB[1]:
    fill_rect(c(p.x),c(p.y),14,14,Color['BG'])
    p.d=1
  elif keydown(KEY_LEFT) and p.WHB[2]:
    fill_rect(c(p.x),c(p.y),14,14,Color['BG'])
    p.d=2
  elif keydown(KEY_UP) and p.WHB[3]:
    fill_rect(c(p.x),c(p.y),14,14,Color['BG'])
    p.d=3
