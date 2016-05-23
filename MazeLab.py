class Maze:
    def __init__(self, maze_text):
        self.maze_text=maze_text
        self.height=len(self.maze_text)
        self.width=len(self.maze_text[0])
        count_1=0
        a=0
        for search in maze_text:
            a=0
            for count_2 in search:
                if count_2=='S':
                    self.start=(count_1,a)
                if count_2=='G':
                    self.goal=(count_1,a)
                a+=1
            count_1+=1
            
        
    def is_passable(self, loc):
        x_1,x_2=loc
        try:
            if loc==self.goal:
                return True
            if loc==self.start:
                return True
            if self.maze_text[x_1][x_2]=='.':
                return True
            elif self.maze_text[x_1][x_2]=='#':
                return False
        except IndexError:
            return False



    def make_maze_successors(maze):
        def checker_func(given):
            routes=[]
            if maze.is_passable((given[0]+1,given[1])):
                routes.append((given[0]+1,given[1]))
            if maze.is_passable((given[0]-1,given[1])):
                routes.append((given[0]-1,given[1]))
            if maze.is_passable((given[0],given[1]+1)):
                routes.append((given[0],given[1]+1))
            if maze.is_passable((given[0],given[1]-1)):
                routes.append((given[0],given[1]-1))
                
            return routes
        return checker_func
