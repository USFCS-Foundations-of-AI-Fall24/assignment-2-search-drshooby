## actions:
## pick up tool
## move_to_sample
## use_tool
## move_to_station
## drop_tool
## drop_sample
## move_to_battery
## charge

## locations: battery, sample, station
## holding_sample can be True or False
## holding_tool can be True or False
## Charged can be True or False

from copy import deepcopy


class RoverState :
    def __init__(self, loc="station", sample_extracted=False, holding_sample=False, holding_tool=False, sample_dropped_off=False, charged=False):
        self.loc = loc
        self.sample_extracted = sample_extracted
        self.holding_sample = holding_sample
        self.holding_tool = holding_tool
        self.charged = charged
        self.sample_dropped_off = sample_dropped_off
        self.prev = None

    ## you do this.
    def __eq__(self, other):
        return (
            self.loc == other.loc and
            self.sample_extracted == other.sample_extracted and
            self.holding_sample == other.holding_sample and
            self.holding_tool == other.holding_tool and
            self.charged == other.charged and
            self.sample_dropped_off == other.sample_dropped_off
        )

    def __repr__(self):
        return (f"Location: {self.loc}\n" +
                f"Sample Extracted?: {self.sample_extracted}\n"+
                f"Holding Sample?: {self.holding_sample}\n" +
                f"Charged? {self.charged}\n" +
                f"Sample Dropped Off?: {self.sample_dropped_off}\n") # added sample dropped off for goal func

    def __hash__(self):
        return self.__repr__().__hash__()

    def successors(self, list_of_actions, depth=0, limit=0):

        ## apply each function in the list of actions to the current state to get
        ## a new state.
        ## add the name of the function also
        if limit != 0: # check if we have a limit
            if depth <= limit: # make sure we are within the limit
                succ = [(item(self), item.__name__, depth) for item in list_of_actions]
                ## remove actions that have no effect
                succ = [item for item in succ if not item[0] == self]
            else:
                return []
        else:
            succ = [(item(self), item.__name__, depth) for item in list_of_actions]
            ## remove actions that have no effect
            succ = [item for item in succ if not item[0] == self]
        return succ

## our actions will be functions that return a new state.

def move_to_sample(state) :
    r2 = deepcopy(state)
    r2.loc = "sample"
    r2.prev=state
    return r2

def move_to_station(state) :
    r2 = deepcopy(state)
    r2.loc = "station"
    r2.prev = state
    return r2

def move_to_battery(state) :
    r2 = deepcopy(state)
    r2.loc = "battery"
    r2.prev = state
    return r2
# add tool functions here

def pick_up_tool(state):
    r2 = deepcopy(state)
    if not r2.holding_tool:
        r2.holding_tool = True
    r2.prev = state
    return r2

def drop_tool(state):
    r2 = deepcopy(state)
    if r2.holding_tool:
        r2.holding_tool = False
    r2.prev = state
    return r2

def use_tool(state):
    r2 = deepcopy(state)
    if r2.holding_tool:
        r2.sample_extracted = True
    r2.prev = state
    return r2

def pick_up_sample(state) :
    r2 = deepcopy(state)
    if state.sample_extracted and state.loc == "sample":
        r2.holding_sample = True
    r2.prev = state
    return r2

def drop_sample(state) :
    r2 = deepcopy(state)
    if state.sample_extracted and state.loc == "station":
        r2.holding_sample = False
        r2.sample_dropped_off = True
    r2.prev = state
    return r2

def charge(state) :
    r2 = deepcopy(state)
    if state.sample_extracted and state.loc == "sample":
        r2.charged = True
    r2.prev = state
    return r2


action_list = [charge, drop_sample, pick_up_sample,
               move_to_sample, move_to_battery, move_to_station,
               pick_up_tool, use_tool, drop_tool]

def battery_goal(state) :
    return state.loc == "battery"

def charge_goal(state) :
    return state.charged

def sample_goal(state) :
    return state.sample_dropped_off

def sub_problems(state) :
    # charger is at sample
    return sample_goal(state) and state.loc == "sample"

def mission_complete(state) :
    return battery_goal(state) and charge_goal(state) and sample_goal(state)



