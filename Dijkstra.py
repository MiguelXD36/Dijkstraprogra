import pygame
import sys


pasos=[]
grid = []
queue = []
path = []
boxfpasos=[]


v_width = 700
v_height = 700

col = 50
filas = 50

box_width = v_width // col
box_height = v_height// filas

window = pygame.display.set_mode((v_width, v_height))

class Box:
    def __init__(self, i, j):
        self.x = i
        self.y = j
        self.start = False
        self.target = False
        self.vecinos = []
        self.anterior = None
        self.queued = False
        self.visited = False
        self.wall = False

    def set_vecinos(self):
        if self.x > 0:
            self.vecinos.append(grid[self.x - 1][self.y])
        if self.x < col - 1:
            self.vecinos.append(grid[self.x + 1][self.y])
        if self.y > 0:
            self.vecinos.append(grid[self.x][self.y - 1])
        if self.y < filas - 1:
            self.vecinos.append(grid[self.x][self.y + 1])

    def draw(self, window, color):
        pygame.draw.rect(window, color, (self.x *box_width, self.y * box_height, box_width-1, box_height-1))

    def color_box(self):
        if self.queued and not self.start and not self.target:
            self.draw(window, (5, 84, 188))
        if self.visited and not self.start and not self.target:
            self.draw(window, (145, 187, 243))
        if self in path and not self.target:
            self.draw(window, (253, 233, 49))

def IniciarPasos(iterador,pasolist):
    i = pasolist[iterador]
    for box in i: 
        box.color_box()  
        
for i in range(col):
    arr = []
    for j in range(filas):
        arr.append(Box(i, j))
    grid.append(arr)

for i in range(col):
    for j in range(filas):
        grid[i][j].set_vecinos()
        
def main():
    
    target_box_set = False
    start_box_set = False
    searching = False
    target_box = None
    Avanzar= False
    iterador = 0
    First=True
    Iniciado=False

    while True:
        boxpasos=[]
        boxfpasos=[]

        for event in pygame.event.get():

            if event.type == pygame.MOUSEMOTION:
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                
                if event.buttons[0] and not start_box_set:
                    
                    i = x // box_width
                    j = y // box_height
                    start_box = grid[i][j]
                    start_box.start = True
                    start_box.visited = True 
                    start_box_set = True
                    queue.append(start_box)
                    
                if event.buttons[1]  :
                    i = x // box_width
                    j = y // box_height
                    grid[i][j].wall = True
                
                if event.buttons[2] and not target_box_set:
                    i = x // box_width
                    j = y // box_height
                    target_box = grid[i][j]
                    target_box.target = True
                    target_box_set = True
            elif event.type == pygame.QUIT:
                 pygame.quit()
                 sys.exit()
          
            if event.type == pygame.KEYDOWN and target_box_set and start_box_set:
                if event.key == pygame.K_RETURN:
    
                  Iniciado=True
                  searching=True

                if event.key == pygame.K_RIGHT and Iniciado:
                    Avanzar=True
                    if iterador<len(pasos)-1:
                     iterador+=1
                if event.key == pygame.K_LEFT and Iniciado:
                    if iterador>0:
                     iterador-=1
                                    
                           
        if Iniciado:
                
            if len(queue) > 0 and searching:
                    box_act = queue.pop(0)
                    if box_act == target_box:
                        searching = False
                        while box_act.prior != start_box:
                         path.append(box_act.prior)
                         box_act = box_act.prior
                    else:
                        for neighbour in box_act.vecinos:      
                            if not neighbour.queued and not neighbour.wall:
                             neighbour.queued = True
                             neighbour.prior = box_act
                             queue.append(neighbour)
                    box_act.visited = True                                                                         
       
        for i in range(col):
            for j in range(filas):
                 box = grid[i][j]
                 box.draw(window, (86, 90, 95))
                 if box.queued or box.visited or (box in path) :
                      boxpasos.append(box)  
                 if box.start:
                     box.draw(window, (124,252,0))
                 if box.target:
                     box.draw(window, (255, 0, 0))
                 if box.wall:
                     box.draw(window, (10, 10, 10))
                
                           
        if searching: 
            if First:
                pasos.append(boxfpasos)
                First=False
            pasos.append(boxpasos)
         
        if Avanzar:
          IniciarPasos(iterador,pasos)
            
        pygame.display.flip()
        
main()
