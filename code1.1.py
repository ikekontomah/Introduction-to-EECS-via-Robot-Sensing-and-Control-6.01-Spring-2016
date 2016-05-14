##function overshoot, which takes the following two inputs:
##
##distances: a list of distances, same as the output from simulate_wall_finder
##goal_distance: the original desired distance
##the function returns True if a robot overshot its goal (that is, if it ever got closer than goal_distance), and False otherwise.
def overshoot(distances,goal_distance):
    for i in range(len(distances)):
        if distances[i] < goal_distance:
            return True
        else:
            return False
