class SearchNode:
    def __init__(self, state, parent, cost = 0.):
        self.state = state
        self.parent = parent
    def path(self):
        p = []
        node = self
        while node:
            p.append(node.state)
            node = node.parent
        p.reverse()
        return p


    def knight_successor(state):
        moves = [(1,2),(1,-2),(-1,2),(-1,-2),(2,1),(2,-1),(-2,1),(-2,-1)]
        board_x, board_y = (8,8)
        out = []
        x,y = state
        for dx,dy in moves:
            nx,ny = x+dx,y+dy
            if (-1<nx<board_x) and (-1<ny<board_y):
                out.append((nx,ny))
        return out

    def search(successors, start_state, goal_test, dfs=False):
    if dfs==False :
        if goal_test(start_state):
            return [start_state]
        startnode=SearchNode(start_state,None)
        agenda=[]
        agenda.append(startnode)
        visited={start_state}
        while len(agenda)!=0:
            parent=agenda.pop(0)
            newchildstates=[]
            print(successors(parent.state))
            for childstate in successors(parent.state):
                child=SearchNode(childstate,parent)
                if goal_test(childstate):
                    return child.path()
                elif childstate not in visited:
                    visited.add(childstate)
                    agenda.append(child)
        return None
    else:
        if goal_test(start_state):
            return [start_state]
        startnode=SearchNode(start_state,None)
        agenda=[]
        agenda.append(startnode)
        visited={start_state}
        while len(agenda)!=0:
            parent=agenda.pop(-1)
            newchildstates=[]
            for childstate in successors(parent.state):
                child=SearchNode(childstate,parent)
                if goal_test(childstate):
                    return child.path()
                    
                elif childstate not in visited:
                    visited.add(childstate)
                    agenda.append(child)
        return None
#Uses searches to evaluate the least cost path between two destinations

    def find_itinerary(start_city, start_time, end_city, deadline):
    start_state=(start_city,start_time)
    def goal_test(state):
        (current_city,current_time)=state
        if current_city==end_city and current_time<=deadline:
            return True
        
        else:
            return False
    return search(flight_successors,start_state,goal_test,False)

    class Flight:
    def __init__(self, start_city, start_time, end_city, end_time):
        self.start_city = start_city
        self.start_time = start_time
        self.end_city = end_city
        self.end_time = end_time

    def __str__(self):
        return str((self.start_city, self.start_time))+' -> '+ str((self.end_city, self.end_time))
    __repr__ = __str__

#A database of fights:

"flightDB = [Flight('Rome', 1, 'Paris', 4),
            Flight('Rome', 3, 'Madrid', 5),
            Flight('Rome', 5, 'Istanbul', 10),
            Flight('Paris', 2, 'London', 4),
            Flight('Paris', 5, 'Oslo', 7),
            Flight('Paris', 5, 'Istanbul', 9),
            Flight('Madrid', 7, 'Rabat', 10),
            Flight('Madrid', 8, 'London', 10),
            Flight('Istanbul', 10, 'Constantinople', 10)]"

class Flight:
    def __init__(self, start_city, start_time, end_city, end_time):
        self.start_city = start_city
        self.start_time = start_time
        self.end_city = end_city
        self.end_time = end_time

    def matches(self, city_time_pair):
        (city, time) = city_time_pair
        if city==self.start_city and time<self.start_time:
            return True
        else:
            return False

    def flight_successors(state):
    
    matchable_flights=[]
    for trip in flightDB:
        is_good_trip=(trip.matches(state))
        if is_good_trip==True:
            
            matchable_flights.append((trip.end_city,trip.end_time))
        
    return matchable_flights

    def find_shortest_itinerary(start_loc, end_loc):
    shortest_choice=[]
    deadline=0
    while True:
        travel_path=find_itinerary(start_loc ,start_time=1, end_city =end_loc, deadline=deadline)
        deadline+=1
        if travel_path is not None:
            return travel_path
        else:
            pass


        

    

