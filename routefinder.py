import math
from queue import PriorityQueue
from Graph import Graph, Edge

class map_state() :
    ## f = total estimated cost
    ## g = cost so far
    ## h = estimated cost to goal
    def __init__(self, location="", mars_graph=None,
                 prev_state=None, g=0,h=0):
        self.location = location
        self.mars_graph = mars_graph
        self.prev_state = prev_state
        self.g = g
        self.h = h
        self.f = self.g + self.h

    def __eq__(self, other):
        return self.location == other.location

    def __hash__(self):
        return hash(self.location)

    def __repr__(self):
        return "(%s)" % (self.location)

    def __lt__(self, other):
        return self.f < other.f

    def __le__(self, other):
        return self.f <= other.f

    def is_goal(self):
        return self.location == '1,1'


def a_star(start_state, heuristic_fn, goal_test, use_closed_list=True) :
    search_queue = PriorityQueue()
    closed_list = {}
    search_queue.put(start_state)



    ## you do the rest.


## default heuristic - we can use this to implement uniform cost search
def h1(state) :
    return 0

## you do this - return the straight-line distance between the state and (1,1)
def sld(state) :
    x, y = state.location.split(',')
    return math.sqrt(
        (int(x) - 1) ** 2 + (int(y) - 1) ** 2
    )

## you implement this. Open the file filename, read in each line,
## construct a Graph object and assign it to self.mars_graph().
def read_mars_graph(filename):
    # 1,1: 2,1 1,2... src: edge1 edge2 etc
    try:
        with open(filename, 'r') as f:
            lines = [line.strip().split(":") for line in f.readlines()]
            edges = {line[0]: line[1].split(" ")[1:] for line in lines}

            g = Graph()

            for src, neighbors in edges.items():
                g.add_node(src)
                for neighbor in neighbors:
                    e = Edge(src, neighbor)
                    g.add_edge(e)
            return g
    except IOError:
        print("Boom")

map = map_state(mars_graph=read_mars_graph("marsmapvalues.txt"))

