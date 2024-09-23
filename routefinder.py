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
    state_count = 0
    search_queue = PriorityQueue()
    closed_list = {}
    search_queue.put(start_state)

    while search_queue:
        curr_state = search_queue.get()
        state_count += 1

        if goal_test(curr_state):
            return curr_state, state_count

        if use_closed_list:
            closed_list[curr_state] = True

        for edge in curr_state.mars_graph.get_edges(curr_state.location):
            neighbor = edge.dest
            new_g = curr_state.g + 1 + edge.val # graph is unweighted, edge val should be 0
            new_h = heuristic_fn(neighbor)

            neighbor_state = map_state(
                neighbor,
                curr_state.mars_graph,
                curr_state,
                new_g,
                new_h
            )

            if use_closed_list and neighbor_state in closed_list:
                continue

            search_queue.put(neighbor_state)

    return None, state_count

## default heuristic - we can use this to implement uniform cost search
def h1(state) :
    return 0

## you do this - return the straight-line distance between the state and (1,1)
def sld(state) :
    if isinstance(state, map_state):
        state = state.location
    x, y = state.split(',')
    return math.sqrt(
        ((int(x) - 1) ** 2) + ((int(y) - 1) ** 2)
    )

## manhattan just to test
def manhattan(state) :
    x, y = state.split(',')
    return abs(int(x) - 1) + abs(int(y) - 1)

## you implement this. Open the file filename, read in each line,
## construct a Graph object and assign it to self.mars_graph().
def read_mars_graph(filename):
    try:
        with open(filename, 'r') as f:
            # 1,1: 2,1 1,2... src: edge1 edge2 etc
            edges = {src: neighbors.split(" ")[1:] for (src, neighbors) in [line.strip().split(":") for line in f.readlines()]}
            g = Graph()
            for src, neighbors in edges.items():
                g.add_node(src)
                for neighbor in neighbors:
                    e = Edge(src, neighbor)
                    g.add_edge(e)
            return g
    except IOError:
        print("Boom")

def goal(s):
    return s.location == "1,1"

def main():
    # from sample (8,8) to charger (1,1)
    state = map_state(location='8,8', mars_graph=read_mars_graph("marsmapvalues.txt"))
    print("\nTESTING A*\n")
    print("SLD HEURISTIC\n")
    end_state, state_count = a_star(state, sld, goal)
    print("states generated =", state_count)
    print("end state =", end_state if end_state else "Something went wrong, end state doesn't exist")

    print("\nH1 HEURISTIC\n")
    state2 = map_state(location='8,8', mars_graph=read_mars_graph("marsmapvalues.txt"))
    end_state2, state_count2 = a_star(state2, h1, goal)
    print("states generated =", state_count2)
    print("end state =", end_state2 if end_state2 else "Something went wrong, end state2 doesn't exist")

if __name__ == "__main__":
    main()

