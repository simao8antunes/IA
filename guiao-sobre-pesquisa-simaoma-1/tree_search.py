from abc import ABC, abstractmethod

class SearchDomain(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def actions(self, state):
        pass

    @abstractmethod
    def result(self, state, action):
        pass

    @abstractmethod
    def cost(self, state, action):
        pass

    @abstractmethod
    def heuristic(self, state, goal):
        pass

    @abstractmethod
    def satisfies(self, state, goal):
        pass

class SearchProblem:
    def __init__(self, domain, initial, goal):
        self.domain = domain
        self.initial = initial
        self.goal = goal

    def goal_test(self, state):
        return self.domain.satisfies(state, self.goal)

class SearchNode:
    def __init__(self, state, parent, depth, cost, heuristic, action=None):
        self.state = state
        self.parent = parent
        self.depth = depth
        self.cost = cost
        self.heuristic = heuristic
        self.action = action #ex2
        self.plan = [] #ex2

    def in_parent(self, newstate):
        if self.state == newstate:
            return True
        elif self.parent is None:
            return False
        else:
            return self.parent.in_parent(newstate)

    def __str__(self):
        return f"no({self.state}, {self.parent})"

    def __repr__(self):
        return str(self)

class SearchTree:
    def __init__(self, problem, strategy='breadth'):
        self.problem = problem
        root = SearchNode(problem.initial, None, 0, 0, 0)
        self.open_nodes = [root]
        self.strategy = strategy
        self.solution = None
        self._length = 0
        self.terminals = 0
        self.non_terminals = 0
        self._avg_branching = 0
        self._cost = 0
        self.highest_cost_nodes = [root]
        self.average_depth = 0
        self.explored_states = set()  #EX3 Adicionar este atributo

    def contains_state(self, state): #ex3
        return state in self.explored_states

    @property
    def length(self):
        if self.solution:
            return self.solution.depth
        return 0

    @property
    def cost(self):
        if self.solution:
            return self.solution.cost
        return 0

    @property
    def avg_branching(self):
        if self.non_terminals > 0:
            ratio = (self.non_terminals + self.terminals - 1) / self.non_terminals
            return round(ratio, 2)
        return 0

    def get_path(self, node):
        if node.parent is None:
            return [node.state]
        path = self.get_path(node.parent)
        path.append(node.state)
        return path

    def search(self, limit=None):
        all_nodes_depth = 0

        while self.open_nodes:
            node = self.open_nodes.pop(0)

            if self.problem.goal_test(node.state):
                self.solution = node
                self.terminals = len(self.open_nodes) + 1
                self.average_depth = all_nodes_depth / (self.non_terminals + self.terminals)

                return self.get_path(node)

            lnewnodes = []

            for a in self.problem.domain.actions(node.state):
                newstate = self.problem.domain.result(node.state, a)
                depth = node.depth + 1
                cost = node.cost + self.problem.domain.cost(node.state, a)

                if newstate is not None and not self.contains_state(newstate): #ex3 (if)
                    newnode = SearchNode(newstate, node, depth, cost, self.problem.domain.heuristic(newstate, self.problem.goal))
                    newnode.plan = node.plan + [a] #ex2

                    if not self.highest_cost_nodes or newnode.cost > self.highest_cost_nodes[0].cost:
                        self.highest_cost_nodes = [newnode] * 5
                    elif newnode.cost == self.highest_cost_nodes[0].cost and newnode not in self.highest_cost_nodes:
                        self.highest_cost_nodes.pop(0)
                        self.highest_cost_nodes.append(newnode)

                if not node.in_parent(newstate) and (limit is None or newnode.depth <= limit):
                    lnewnodes.append(newnode)
                    self.explored_states.add(newstate)
                    all_nodes_depth += newnode.depth

            self.non_terminals += 1
            self.add_to_open(lnewnodes)

        return None

    def add_to_open(self, lnewnodes):
        if self.strategy == 'breadth':
            self.open_nodes.extend(lnewnodes)
        elif self.strategy == 'depth':
            self.open_nodes[:0] = lnewnodes
        elif self.strategy == 'uniform':
            self.open_nodes.extend(lnewnodes)
            self.open_nodes.sort(key=lambda node: node.cost)
        elif self.strategy == 'greedy':
            self.open_nodes.extend(lnewnodes)
            self.open_nodes.sort(key=lambda node: node.heuristic)
        elif self.strategy == 'a*':
            self.open_nodes.extend(lnewnodes)
            self.open_nodes.sort(key=lambda node: node.heuristic + node.cost)
