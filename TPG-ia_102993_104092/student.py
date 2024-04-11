import asyncio
import json
import math
import websockets
import os
import getpass

import asyncio
import json
import websockets
import os
import getpass
from abc import ABC, abstractmethod

# Define Search Classes
class SearchDomain(ABC):

    # construtor
    @abstractmethod
    def __init__(self):
        pass

    # lista de accoes possiveis num estado
    @abstractmethod
    def actions(self, state):
        pass

    # resultado de uma accao num estado, ou seja, o estado seguinte
    @abstractmethod
    def result(self, state, action):
        pass

    # custo de uma accao num estado
    @abstractmethod
    def cost(self, state, action):
        pass

    # custo estimado de chegar de um estado a outro
    @abstractmethod
    def heuristic(self, state, goal):
        pass

    # test if the given "goal" is satisfied in "state"
    @abstractmethod
    def satisfies(self, state, goal):
        pass


# Problemas concretos a resolver
# dentro de um determinado dominio
class SearchProblem:
    def __init__(self, domain, initial, goal):
        self.domain = domain
        self.initial = initial
        self.goal = goal
    def goal_test(self, state):
        return self.domain.satisfies(state,self.goal)

# Nos de uma arvore de pesquisa
class SearchNode:
    def __init__(self, state, parent, action = "", depth=0, cost=0, heuristic=0): #
        self.state = state
        self.action = action
        self.parent = parent
        self.depth = depth #ex2 adiciona a possibilidade de calcular a depth a que está eleminar?
        self.cost = cost #ex8 possibilita a habilidade de guardar o custo eleminar?
        self.heuristic = heuristic #ex12 possibilita a habilidade de guardar o valor da heuristica

    #previne ciclos na arvore de pequisa ex1 eleminar?
    def in_parent(self,newstate):
        if self.parent == None:
            return False
        if self.state == newstate:
            return True
        return self.parent.in_parent(newstate)
        
    def __str__(self):
        return "no(" + str(self.state) + "," + str(self.parent) + ")"
    def __repr__(self):
        return str(self)

# Arvores de pesquisa
class SearchTree:

    # construtor
    def __init__(self,problem, strategy='breadth'): 
        self.problem = problem
        root = SearchNode(problem.initial, None)
        self.open_nodes = [root]
        self.strategy = strategy
        self.solution = None
        self.non_terminals = 0 # ex5 definição da variavel que conta os nos n terminais eleminar?
        self.highest_cost_nodes = [root] #ex15 guarda a lista com os nós com maior custo acumulado eleminar?
        self._total_depth = 0 #ex16 guarda a depth total eleminar?
        self.average_depth = 0 #ex16 guarda a avg depth dos nós eleminar?

    @property #ex5 calcula o numero de nodes terminais eleminar?
    def terminals(self):
        return len(self.open_nodes)

    @property #ex3 eleminar?
    def length(self):
        return self.solution.depth
    @property #ex6 eleminar?
    def avg_branching(self):
        return (self.terminals + self.non_terminals -1
                #todos os nós com excepção da raiz da árvore
                ) / self.non_terminals
                # a dividir por tds os nós nao terminais
    #EX9   eleminar?
    @property
    def cost(self):
        return self.solution.cost

    # obter o caminho (sequencia de estados) da raiz ate um no, eleminar?
    def get_path(self,node):
        if node.parent == None:
            return [node.state]
        path = self.get_path(node.parent)
        path += [node.state]
        return(path)
    
    # obter o caminho (sequencia de açoes) da raiz ate um no
    def get_path_ac(self,node):
        if node.parent == None:
            return [node.action]
        path = self.get_path_ac(node.parent)
        path += [node.action]
        return(path)

    # procurar a solucao
    def search(self,limit=None):#ex4 funcionalidade de definir limite de profundidade na pesquisa
        while self.open_nodes != []:
            node = self.open_nodes.pop(0)
            if self.problem.goal_test(node.state):
                self.solution = node
                self.average_depth = self._total_depth / (self.terminals + self.non_terminals -1) #ex16 calcula a profundidade media dos nós eleminar?
                return self.get_path_ac(node), self.get_path(node)
            self.non_terminals += 1 #ex5 os nos nao terminais sao aqui adicionados
            lnewnodes = []
            #print("node presente: {}".format(node))
            for a in self.problem.domain.actions(node.state):
                newstate = self.problem.domain.result(node.state,a)
                #print("node novo: {}".format(newstate))
                if (not node.in_parent(newstate)) and (#se o node ja for pai nao faz isto eleminar?
                    limit == None or node.depth<limit): #ex4 funcionalidade de definir limite de profundidade na pesquisa
                    newnode = SearchNode(newstate,
                                         node,
                                         a,
                                         node.depth+1, #ex2 adiciona a possibilidade de calcular a depth a que está
                                         node.cost + self.problem.domain.cost(node.state,a,self.problem.goal), # ex8 armazena o cost
                                         self.problem.domain.heuristic(newstate,self.problem.goal) #ex12 armazena a heuristica
                                        ) 
                    lnewnodes.append(newnode)

            self.add_to_open(lnewnodes)
        return None

    # juntar novos nos a lista de nos abertos de acordo com a estrategia
    def add_to_open(self,lnewnodes):
        if self.strategy == 'breadth': #eleminar?
            self.open_nodes.extend(lnewnodes)
        elif self.strategy == 'depth': #eleminar?
            self.open_nodes[:0] = lnewnodes
        elif self.strategy == 'uniform': #ex10 #eleminar?
            self.open_nodes.extend(lnewnodes) #adiciona a lista dos nos novos
            self.open_nodes.sort(key=lambda node: node.cost) #ordena essa lista tendo em conta o custo 
        elif self.strategy == 'greedy':
            self.open_nodes.extend(lnewnodes) #adiciona a lista dos nos novos
            self.open_nodes.sort(key=lambda node: node.heuristic) #ordena essa lista tendo em conta a heuristica 
        elif self.strategy == 'a*':  # junta os metodos de pesquisa uniforme e greedy #eleminar?
            self.open_nodes.extend(lnewnodes)
            self.open_nodes.sort(key=lambda node: node.cost + node.heuristic)


# Define DigDug Search Domain
class DigDugSearchDomain(SearchDomain):
    # Implement the required methods: actions, result, cost, heuristic, satisfies
    # ...
    def __init__(self,state,fygar_range):
        self.enemies = state["enemies"]
        self.rocks = state["rocks"]
        self.digdug = state["digdug"]
        self.fygar_range = fygar_range
 


    def actions(self, coords):
        actlist = ["a", "s", "w", "d"]

        if coords[0] == 0:
            actlist.remove("a")

        if coords[1] == 0:
            actlist.remove("w")

        if coords[1] == 23:
            actlist.remove("s")

        if coords[0] == 47:
            actlist.remove("d")

        for rocks in self.rocks:
            if rocks["pos"][0]  == coords[0]: # se a pedra ta na mm coluna
                if  rocks["pos"][1] - 1 == coords[1]: # pedra em cima do digdug
                    actlist.remove("w")

                elif rocks["pos"][1] + 1 == coords[1]: # pedra em baixo do digdug
                    actlist.remove("s")

            if rocks["pos"][1]  == coords[1]: # se a pedra ta na mm coluna
                if  rocks["pos"][0] - 1 == coords[0]: # pedra ta a direita do digdug
                    actlist.remove("d")

                elif rocks["pos"][0] + 1 == coords[0]: # pedra ta a esquerda do digdug
                    actlist.remove("a")
        # no caso de o dig dug estar atrás de um fygar           
        if self.fygar_range != []:
            for range_coords in self.fygar_range:
                if range_coords[0]  == coords[0]: # se o fygar ta na mm coluna
                    if  range_coords[1] - 1 == coords[1]: # fygar em cima do digdug
                        actlist.remove("w")

                    elif range_coords[1] + 1 == coords[1]: # pedra em baixo do digdug
                        actlist.remove("s")

                if range_coords[1]  == coords[1]: # se a pedra ta na mm coluna
                    if  range_coords[0] - 1 == coords[0]: # pedra ta a direita do digdug
                        actlist.remove("d")

                    elif range_coords[0] + 1 == coords[0]: # pedra ta a esquerda do digdug
                        actlist.remove("a")
        return actlist 
        

    def result(self,coords,action):
        (x,y) = coords
        if action == "w":
            y -= 1
        elif action == "s":
            y += 1
        elif action == "a":
            x -= 1
        elif action == "d":
            x += 1

        return (x,y)

    def cost(self,coords,action,closest_enemy): #eleminar?
        return 1
            
    def heuristic(self, coords, closest_enemy):
        #distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        distance = math.dist(coords, closest_enemy)
        return distance
            
    def satisfies(self, coords, closest_enemy):
        distance = math.dist(coords, closest_enemy)
        if distance == 0:
            return True
        return False
    
#---------------------funçoes auxiliares---------------------------------
def ver_coords(dir, dig_dug, enemy,map): # verifica as coordenadas do dig_dug se td estiver como o esperado devolve True e a ação a praticar
    x,y = enemy
    if map[x][y] == 0: # aqui verifica se o inimigo está ou não em espaço aberto
        if dir == 0 or dir == 2: # verifica se o inimigo se está a movimentar no eixo vertical
            if dig_dug[0] == enemy[0]: 
                if dir == 0: 
                    if dig_dug[1] < enemy[1]:
                        return True,"d"
                    return True,"w"
                else:
                    if dig_dug[1] > enemy[1]:
                        return True,"a"
                    return True,"s"
            return False,""
        else:
            if dig_dug[1] == enemy[1]:
                if dir == 1:
                    if dig_dug[0] > enemy[0]:
                        return True, "w"
                    return True,"d"
                else:
                    if dig_dug[0] < enemy[0]:
                        return True, "s"
                    return True,"a"
            return False,""
    return False,""

def update_map(map, coord): # dá update ao mapa opós o dig dug se movimentar
    x,y = coord
    map[x][y] = 0

def calc_coords(dir, coord, dist): #«calcula as coordenadas desejadas tendo em conta a direção e a distancia pretendida
    goal_coord = [0,0]
    if dir == 0 : # dir cima 
        goal_coord[0] = coord[0]
        goal_coord[1] = abs(coord[1] + dist)
    elif dir == 2:# dir baixo 
        goal_coord[0] = coord[0]
        goal_coord[1] = abs(coord[1] - dist) 
    elif dir == 1:# dir direita
        goal_coord[1] = coord[1]
        goal_coord[0] = abs(coord[0] - dist) 
    else: # dir esq
        goal_coord[1] = coord[1]
        goal_coord[0] = abs(coord[0] + dist)
    
    #verifica se o goal_coord tem coordenadas aceitaveis
    if goal_coord[0] > 47:
        goal_coord[0] = 47
    if goal_coord[1] > 23:
        goal_coord[1] = 23
    
    return goal_coord

def ver_dir_dig_dug(action): # devolve a dir em q o dig_dug está tendo em conta a ação que tomou
    if action == "w":
        return 0
    if action == "a":
        return 3
    if action == "d":
        return 1
    if action == "s":
        return 2

def ver_rocks(rocks,dig_dug):
    coord_cima = calc_coords(0,dig_dug,-1)
    for rock in rocks:
        if coord_cima == rock["pos"]:
            return False
    return True

# Modify agent_loop
async def agent_loop(server_address="localhost:8000", agent_name="student"):
    # Create an instance of DigDugSearchDomain
    async with websockets.connect(f"ws://{server_address}/player") as websocket:
        await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))
        count = 0
        while True:
            try:
                state = json.loads(await websocket.recv())
                print("Received state:", state)

                if "map" in state:
                    map = state["map"] # guarda o novo mapa quando o jogador primeiro se connecta ou qd muda de nivel
                    dir_dig = 1
                    enemy = {'name':"",'pos': [0,0], 'dir':0}
                    a_b_shoot = ""
                    #print("mapa: {}".format(map))

                if "digdug" in state and "enemies" in state:
                    digdug_pos = state["digdug"]
                    enemies = state["enemies"]
                    rocks = state["rocks"]
                    

                    if enemies:
                        closest_enemy = min(enemies, key=lambda enemy: abs(digdug_pos[0] - enemy["pos"][0]) + abs(digdug_pos[1] - enemy["pos"][1]))
                        # Define initial and goal states for the search problem
                        initial_state = digdug_pos
                        fygar_range = []
                        if enemy["name"] == closest_enemy["name"]:
                            if enemy["pos"] != closest_enemy["pos"]:
                                if enemy["pos"][0] == closest_enemy["pos"][0]:
                                    if enemy["pos"][1] > closest_enemy["pos"][1]:
                                        enemy["dir"] = 0
                                    else:
                                        enemy["dir"] = 2
                                else:
                                    if enemy["pos"][0] > closest_enemy["pos"][0]:
                                        enemy["dir"] = 3
                                    else:
                                        enemy["dir"] = 1
                        else:
                            enemy["name"] = closest_enemy["name"]
                            enemy["dir"] = closest_enemy["dir"]
                        
                        enemy["pos"] = closest_enemy["pos"]

                        if enemy["name"] == "Fygar":
                            for dist in [-1,-2,-3]:
                                fygar_range.append(calc_coords(enemy["dir"],enemy["pos"],dist))

                        s = DigDugSearchDomain(state,fygar_range)
                        #goalstate modificado para o digdug aparecer atrás do inim com dist 3
                        goal_state = calc_coords(enemy["dir"],enemy["pos"],3)
                        
                        #dá print as coords do objetivo, do dig dug do inimigo mais proximo e da direção do inimigo
                        print("goal_mod: {}".format(goal_state))
                        print("dig dug: {}, inimigo: {}, dir: {}".format(initial_state,enemy["pos"],enemy["dir"]))
                        
                        #verifica se o inimigo mais proximo está a uma distancia menor ao igual a 2 ou 3
                        dist = math.dist(initial_state, enemy["pos"])
                        if dist <= 3:
                            print("tou pa matar")
                            #esta função está descrita em cima, verifica se o dig dug está numa possição aceitavel para atacar
                            ver,a = ver_coords(enemy["dir"],initial_state,enemy["pos"],map)
                            if ver and not kill:
                                print("a")
                                print("action: {}".format(a))
                                dir_dig = ver_dir_dig_dug(a)
                                kill = True
                                a_b_shoot = a
                                await websocket.send(
                                        json.dumps({"cmd": "key", "key": a})
                                    )
                            else:
                                x,y = calc_coords(dir_dig,initial_state,-1)
                                if map[x][y] == 0:
                                    print("b") 
                                    if ver_rocks(rocks,initial_state): 
                                        await websocket.send(
                                                json.dumps({"cmd": "key", "key": "AB"})
                                            )
                                    else:
                                        if dir_dig == 1:
                                            action = "a"
                                        elif dir_dig == 2:
                                            action = "a" # contruir função que valide a ação
                                        elif dir_dig == 3:
                                            action = "d"
                                        else:
                                            action = "d"
                                        
                                        await websocket.send(
                                                json.dumps({"cmd": "key", "key": action})
                                            )
                                else:
                                    print("c")
                                    kill = False
                        else:
                            # aqui é aplicada a search tree para calcular o mlhr caminho para o objetivo definido em cima
                            kill = False
                            print("tou para caminhar")
                            problem = SearchProblem(s, initial_state, goal_state)
                            tree = SearchTree(problem, strategy='greedy')
                            path,coord = tree.search()
                            
                            if path: 
                                if len(path) != 1: 
                                    print("tenho action")
                                    update_map(map,coord[1]) # dá update do mapa para saber que espaços é que estão vazios ou ainda com terreno
                                    #print("mapa: {}".format(map)) 
                                    dir_dig = ver_dir_dig_dug(path[1])                     
                                    await websocket.send(
                                        json.dumps({"cmd": "key", "key": path[1]})
                                    )
                            else:
                                print("path ta nulo")                       
                    
            except websockets.exceptions.ConnectionClosedOK:
                print("Server has cleanly disconnected us")
                return
            


#DO NOT CHANGE THE LINES BELOW
loop = asyncio.get_event_loop()
SERVER = os.environ.get("SERVER", "localhost")
PORT = os.environ.get("PORT", "8000")
NAME = os.environ.get("NAME", getpass.getuser())
loop.run_until_complete(agent_loop(f"{SERVER}:{PORT}", NAME))
