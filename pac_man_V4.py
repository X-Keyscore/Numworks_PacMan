# V4 | By XKeyscore
from math import *
import kandinsky as kand
from ion import *
from time import *
# color Table
colorT={
  "background": kand.color(0,0,0),
  "title": kand.color(255,191,0),
  "text": kand.color(108,52,131),
  "pacman": kand.color(255,255,0),
  "enemy": kand.color(255,87,34),
  "wall": kand.color(24,24,190),
  "coin": kand.color(255,255,0),
  "shieldb": kand.color(0,0,255),
  "shieldp": kand.color(127,0,255),
  "shieldr": kand.color(255,0,0)
}
# Maps | wall [x,y,size,direction]
maps = {
  "name": "Pac-Man",
  "wall": [
    [0,0,15,0],[10,1,1,0],[14,1,13,1],
    [0,1,14,1],[2,2,3,0],[6,2,3,0],
    [12,2,1,0],[2,3,2,1],[10,3,4,1],
    [4,4,3,0],[8,4,4,0],[13,4,1,0],
    [4,5,2,1],[2,6,3,1],[6,6,3,0],
    [12,6,3,1],[6,7,3,0],[4,8,4,1],
    [6,8,3,0],[10,8,3,1],[1,10,1,0],
    [3,10,4,0],[8,10,3,0],[12,10,3,1],
    [2,12,1,0],[6,12,3,0],[10,12,3,0],
    [4,13,1,0],[0,14,15,0]
  ]
}
# Icons | pacman [x,y,size]
icons = {
  "pacman": [
    [6,0,3],[4,1,7],[3,2,9],
    [2,3,11],[1,4,13],[1,5,12],
    [0,6,11],[0,7,8],[0,8,11],
    [1,9,12],[1,10,13],[2,11,11],
    [3,12,9],[4,13,7],[6,14,3]
  ],
  "shield": [
    [4,1,2],[11,1,2],[2,2,5],
    [10,2,5],[1,3,6],[10,3,6],
    [1,4,15],[1,5,15],[2,6,13],
    [2,7,13],[3,8,11],[3,9,11],
    [3,10,11],[3,11,11],[3,12,11],
    [3,13,11],[4,14,9],[5,15,7]
  ]
}

# =[ FUNCTIONS ]=

# Conversion
def c(a):
  return a*15

# Attente
def waiting():
  sleep(0.10)

# Display icon
def displayicon(x,y,iconname,colorname):
  for icon in icons[iconname]:
      kand.fill_rect(icon[0]+(x*15),(icon[1]-1)+(y*15),icon[2],1,colorT[colorname])

# Reset pixel
def resetpixel(x,y,w,h):
  kand.fill_rect(x*15,y*15,w*15,y*15,colorT['background'])

# Initialisation
def init():
  # -Background-
  kand.fill_rect(0, 0, 320, 222, colorT['background'])
  # -Borders and Walls-
  for wall in maps['wall']:
    if (wall[3] == 0):
      kand.fill_rect(wall[0]*15,wall[1]*15,wall[2]*15,15,colorT['wall'])
    else:
      kand.fill_rect(wall[0]*15,wall[1]*15,15,wall[2]*15,colorT['wall'])
  # -Level-
  kand.draw_string("Level:",c(15),c(0),colorT['title'],colorT['background'])
  kand.draw_string("0",c(19),c(0),colorT['title'],colorT['background'])
  # -Life point pacman-
  def lfp():
    lfpPos = [[15,1],[16,1],[17,1]];i = 0
    # Je boucle pour afficher tout mes lfp grace au tableau
    while (i < len(lfpPos)):
      # Récupération de la position
      x=lfpPos[i][0];y=lfpPos[i][1]
      # Fonction pour afficher l'icon
      displayicon(x,y,'pacman','pacman')
      i=i+1
  lfp()
  # -Shield-
  def shield():
    # Fonction pour afficher l'icon
    displayicon(15,2,'shield','shieldb')
    displayicon(16,2,'shield','shieldp')
    displayicon(17,2,'shield','shieldr')
    sleep(0.15)
    #resetpixel(15,2,4,1)
    #shieldPos = [[15,2],[16,2],[17,2]];i = 0
  shield()
  #displayicon(1,1,'pacman','pacman')
  #Fin init

# =[ GRAPHIC ENGINE ]=

# Move player
def playerMove(x1,y1,D):
  # Display
  def displayentity(x,y,iconname,colorname,Com):

    icon = icons[iconname][0]
    calX=0;calY=0
    if (Com['e'][0] == 'x'):
      calX=x*15+Com['x']
      calY=y+Com['y']
    elif (Com['e'][0] == 'y'):
      calX=x+Com['x']
      calY=y*15+Com['y']
    # voir les *15 et resetpixel
    #resetpixel(x,y,2,1)
  
    for icon in icons[iconname]:
      xx=icon[0]+(calX)
      yy=(icon[1]-1)+(calY)
      print(xx, yy)
      kand.fill_rect(xx,yy,icon[2],1,colorT[colorname])
    sleep(0.02)

  # Compass | [{x,y,edit}]
  Com = [{"x":15,"y":0,"e":['y',-1]},{"x":0,"y":14,"e":['x',1]},{"x":15,"y":0,"e":['y',1]},{"x":0,"y":15,"e":['x',-1]}]
  Com=Com[D]

  i=0
  while (i < 15):
    displayentity(x1,y1,'pacman','pacman',Com)
    i=i+1
    Com[Com['e'][0]]=Com[Com['e'][0]]+Com['e'][1]

  if (Com['e'][0] == 'x'):
    end={"x":x1+Com['e'][1],"y":y1}
  elif (Com['e'][0] == 'y'):
    end={"x":x1,"y":y1+Com['e'][1]}
  print(end)
  return end




# =[ PROCESS ]=
init()

# [ CACHE ] | P = Position | D1 = Direction actuelle | D2 = Direction a venir
C={
  "level":0,
  "P":{"x":1,"y":1},
  "DTable":[0,1,2,3],
  "D1":1,
  "D2":0
}

# =[ LOOP ]=
loop = True
#Player
kand.fill_rect(15,15,1,1,kand.color(0,150,152))
while (loop == True):
  C['P']=playerMove(C['P']['x'],C['P']['y'],C['D1'])
  loop=False
  #Ghost
  #Action
  if keydown(KEY_UP):
    C['D1']=0
  elif keydown(KEY_RIGHT):
    C['D1']=1
  elif keydown(KEY_DOWN):
    C['D1']=2
  elif keydown(KEY_LEFT):
    C['D1']=3

  kand.draw_string(str(C['P']['x']),c(15),c(6),colorT['title'],colorT['background'])
  kand.draw_string(str(C['P']['y']),c(15),c(7),colorT['title'],colorT['background'])
  kand.draw_string("Dir:"+str(C['D1']),c(15),c(8),colorT['title'],colorT['background'])