from collections import deque

from mars_planner import sub_problems


def format_state_count(state_count, goal_found):
    goal_str = "Yes" if goal_found else "No"
    return f"\nStates generated: {state_count}, goal found? {goal_str}\n"

## We will append tuples (state, "action") in the search queue
def breadth_first_search(startState, action_list, goal_test, use_closed_list=True) :
    search_queue = deque()
    closed_list = {}
    state_count = 0
    search_queue.append((startState,""))
    if use_closed_list :
        closed_list[startState] = True
    while len(search_queue) > 0 :
        ## this is a (state, "action") tuple
        next_state = search_queue.popleft()
        state_count += 1
        if goal_test(next_state[0]):
            print("Goal found")
            print(next_state)
            print("------------\n") # added for testing clarity
            ptr = next_state[0]
            while ptr is not None :
                ptr = ptr.prev
                print(ptr)
            print(format_state_count(state_count, True))
            return next_state
        else :
            successors = next_state[0].successors(action_list)
            if use_closed_list :
                successors = [item for item in successors
                                    if item[0] not in closed_list]
                for s in successors :
                    closed_list[s[0]] = True
            search_queue.extend(successors)
    print(format_state_count(state_count, False))

### Note the similarity to BFS - the only difference is the search queue

## use the limit parameter to implement depth-limited search
def depth_first_search(startState, action_list, goal_test, use_closed_list=True,limit=0) :
    search_queue = deque()
    closed_list = {}
    state_count = 0
    search_queue.append((startState,"", 0))
    if use_closed_list :
        closed_list[startState] = True
    while len(search_queue) > 0 :
        ## this is a (state, "action", depth) tuple
        next_state = search_queue.pop()
        state_count += 1
        if goal_test(next_state[0]):
            print("Goal found")
            print(next_state)
            print("------------\n")
            ptr = next_state[0]
            while ptr is not None :
                ptr = ptr.prev
                print(ptr)
            print(format_state_count(state_count, True))
            return next_state
        else :
            successors = next_state[0].successors(action_list, next_state[2] + 1, limit)
            if use_closed_list :
                successors = [item for item in successors
                                    if item[0] not in closed_list]
                for s in successors :
                    closed_list[s[0]] = True
            search_queue.extend(successors)
    print(format_state_count(state_count, False))

def main():
    from mars_planner import RoverState, action_list, mission_complete
    template = f'Function run done, starting next...\n_______________________'

    s = RoverState()
    breadth_first_search(s, action_list, mission_complete)
    print(template)

    s2 = RoverState()
    depth_first_search(s2, action_list, mission_complete)
    print(template)

    print("Running DLS, trying depth=5\n")
    s3 = RoverState()
    depth_first_search(s3, action_list, mission_complete, limit=5)

    print("Running DLS, trying depth=15\n")
    s4 = RoverState()
    depth_first_search(s4, action_list, mission_complete, limit=15)
    print(template)

    print("Running three sub-problems:\n")
    s5 = RoverState()
    s5.loc = "sample" # start sub-problem by modifying start state
    breadth_first_search(s5, action_list, sub_problems)
    print(template)

    s6 = RoverState()
    s6.loc = "sample"
    depth_first_search(s6, action_list, sub_problems)

    print("\nSEARCH_ALGORITHMS.PY COMPLETE\n")


if __name__ == '__main__':
    main()
