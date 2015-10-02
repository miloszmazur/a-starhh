from math import sqrt

__author__ = 'yuafan'

import random
import numpy as np
import matplotlib.pyplot as plt


sizeOfMap2D = [100, 50]
percentOfObstacle = 0.9  # 30% - 60%, random



# Generate 2D matrix of size x * y
# starting Point and Ending Point

def generateMap2d(size_):
# Generates a random 2d map of size size_. You can choose your desired size but whatever solution you come up with has
# to work independently of map size

    size_x, size_y = size_[0], size_[1]

    map2d = np.random.rand(size_y, size_x)
    perObstacles_ = percentOfObstacle
    map2d[map2d <= perObstacles_] = 0
    map2d[map2d > perObstacles_] = -1


    yloc, xloc = [np.random.random_integers(0, size_x-1, 2), np.random.random_integers(0, size_y-1, 2)]
    while (yloc[0] == yloc[1]) and (xloc[0] == xloc[1]):
        yloc, xloc = [np.random.random_integers(0, size_x-1,2), np.random.random_integers(0, size_y-1, 2)]


    map2d[xloc[0]][yloc[0]] = -2
    map2d[xloc[1]][yloc[1]] = -3

    return map2d

# Generate specific map
def generateMap2d_case1(size_):
# Generates a special map with the middle blocked and passing from left to right being possible at the top or bottom
# part of the map. If for some reason the map fails to generate like that rerun it as it is not foolproof
    size_x, size_y = size_[0], size_[1]
    map2d = generateMap2d(size_)

    map2d[map2d==-2] = 0
    map2d[map2d==-3] = 0

    # add special obstacle
    xtop = [np.random.random_integers(5, 3*size_x//10-2), np.random.random_integers(7*size_x//10+3, size_x-5)]
    ytop = np.random.random_integers(7*size_y//10 + 3, size_y - 5)
    xbot = np.random.random_integers(3, 3*size_x//10-5), np.random.random_integers(7*size_x//10+3, size_x-5)
    ybot = np.random.random_integers(5, size_y//5 - 3)

    map2d[ybot, xbot[0]:xbot[1]+1] = -1
    map2d[ytop, xtop[0]:xtop[1]+1] = -1
    minx = (xbot[0]+xbot[1])//2
    maxx = (xtop[0]+xtop[1])//2
    if minx > maxx:
        tempx = minx
        minx = maxx
        maxx = tempx
    if maxx == minx:
        maxx = maxx+1
    map2d[ybot:ytop, minx:maxx] = -1
    startp = [np.random.random_integers(0, size_x//2 - 4), np.random.random_integers(ybot+1, ytop-1)]

    map2d[startp[1], startp[0]] = -2
    goalp = [np.random.random_integers(size_x//2 + 4, size_x - 3), np.random.random_integers(ybot+1, ytop-1)]

    map2d[goalp[1],goalp[0]] = -3
    return map2d, ybot, ytop

def plotMap(map2d_, path_):
# Plots a map as described in lab2 description containing integer numbers. Each number has a specific meaning. You can check
# the example provided at the end of the file for more information

    import matplotlib.cm as cm

    greennumber = map2d_.max()
    colors = cm.winter(np.linspace(0, 1, greennumber))

    colorsMap2d = [[[] for x in xrange(map2d_.shape[1])] for y in range(map2d_.shape[0])]
    # Assign RGB Val for starting point and ending point
    locStart, locEnd = np.where(map2d_ == -2), np.where(map2d_ == -3)
    colorsMap2d[locStart[0]][locStart[1]] = [.0, .0, .0, 1.0]  # black
    colorsMap2d[locEnd[0]][locEnd[1]] = [.0, 0.0, 0.0, 0.5]  # grey

    # Assign RGB Val for obstacle
    locObstacle = np.where(map2d_ == -1)
    for iposObstacle in range(len(locObstacle[0])):
        colorsMap2d[locObstacle[0][iposObstacle]][locObstacle[1][iposObstacle]] = [1.0, .0, .0, 1.0]
    # Assign 0
    locZero = np.where(map2d_ == 0)

    for iposZero in range(len(locZero[0])):
        colorsMap2d[locZero[0][iposZero]][locZero[1][iposZero]] = [1.0, 1.0, 1.0, 1.0]

    # Assign Expanded nodes
    locExpand = np.where(map2d_>0)

    for iposExpand in range(len(locExpand[0])):
        colorsMap2d[locExpand[0][iposExpand]][locExpand[1][iposExpand]] = colors[map2d_[locExpand[0][iposExpand]][locExpand[1][iposExpand]]-1]

    if path_:
        for point in path:
            # colorsMap2d[point[0]][point[1]] = [.0, .0, .0, 0.5]  # black
            plt.plot(path_[:][0],path_[:][1], color='magenta',linewidth=2.5)
    plt.imshow(colorsMap2d, interpolation='nearest')
    # plot the path
    plt.ylim(0,map2d_.shape[0])
    plt.xlim(0,map2d_.shape[1])
    plt.show()


def get_surrounding_nodes(mmap, node):
    cells = []
    dims = mmap.shape
    if node[0] < dims[0] -1 and mmap[node[0]+1, node[1]] not in [-1, -2]:
        cells.append((node[0]+1, node[1]))
    if node[1] < dims[1] -1 and mmap[node[0], node[1]+1] not in [-1, -2]:
        cells.append((node[0], node[1]+1))
    if node[0] > 0 and mmap[node[0]-1, node[1]] not in [-1, -2]:
        cells.append((node[0] -1, node[1]))
    if node[1] > 0 and mmap[node[0], node[1]-1] not in [-1, -2]:
        cells.append((node[0], node[1] -1))
    return cells


def get_heur_val(_from, _to, top, bot):
    # euclidean
    return sqrt((_from[0] - _to[0]) * (_from[0] - _to[0]) + (_from[1] - _to[1]) * (_from[1] - _to[1]))

    # manhattan
    # return abs(_from[0] - _to[0]) + abs(_from[1] - _to[1])

    # specialized
    # euc = sqrt((_from[0] - _to[0]) * (_from[0] - _to[0]) + (_from[1] - _to[1]) * (_from[1] - _to[1]))
    # return (abs(_from[1] - top) + abs(_to[1] / top)) / (abs(_from[1] - bot) + abs(_to[1] - bot)) * euc



def get_minimum_node(node_list, goal, top_border, bottom_border):
    # returns (node, step, parent)
    const = 0.3
    res = node_list[0]
    min_val = get_heur_val(res[0], goal, top_border, bottom_border) + node_list[0][1] * const
    for entry in node_list:
        node = entry[0]
        step = entry[1]
        if get_heur_val(node, goal, top_border, bottom_border) + step * const < min_val:
            min_val = get_heur_val(node, goal, top_border, bottom_border)
            res = entry
    return res


def node_is_in_checked(node, checked):
    # srsly.
    res = False
    for n in checked:
        if int(node[0][0]) == int(n[0][0]) and int(node[0][1]) == int(n[0][1]):   # srsly
            res = True
    return res

def find_node_in_list(node, node_list):
    result = None
    if node == None:
        return None
    for n in node_list:
        if int(node[0]) == int(n[0][0]) and int(node[1]) == int(n[0][1]):
            result = n
    return result

def remove_node(node, node_list):
    for n in node_list:
        if int(node[0][0]) == int(n[0][0]) and int(node[0][1]) == int(n[0][1]):
            node_list.remove(n)
            break
    return node_list


def astar(mmap, top = None, bot = None):
    path = []
    start = np.where(mmap == -2)
    goal = np.where(mmap == -3)
    step = 1
    opened = [(start, 0, None)]
    checked = []
    while len(opened) > 0:
        curr = get_minimum_node(opened, goal, top, bot)
        curr_coordinates = (curr[0][0], curr[0][1])
        opened = remove_node(curr, opened)
        if not node_is_in_list(curr, checked):
            if curr_coordinates == goal:
                path.append(curr_coordinates) # goal
                path.append(curr[2]) # parent of goal
                pparent = find_node_in_list(curr[2], checked) # parent of parent of goal
                while pparent != None:
                    path.append(pparent[2]) # every other parent
                    pparent = find_node_in_list(pparent[2], checked)
                path.pop() # get rid of the None at the end
                return 'goal reached', list(reversed(path))
            else:
                checked.append(curr)
                if mmap[curr_coordinates] != -2: # start
                    mmap[curr_coordinates] = step # + get_heur_val(curr, goal, top,bot)
                neighbours = get_surrounding_nodes(mmap, curr_coordinates)
                for neighbour in neighbours:
                    opened.append((neighbour, step, curr_coordinates))
        step+=1
    return 'no solution', None



## Example
## Map description
##   0 - Free cell
##   -1 - Obstacle
##   -2 - Start point
##   -3 - Goal point
##
# res, path = astar(mymap, top, bot)
## Solve using your implemented A* algorithm
##solved_map description
##   0 - unexpanded cell
##   -1 - obstacle
##   -2 - start point
##   -3 - goal point
##   positive_number - one of the values described in lab2 description (heuristic cost, travel cost, cell total cost,...)
mymap, top, bot = generateMap2d_case1([40,40])
# mymap = generateMap2d([40,40])
# print mymap
res, path = astar(mymap, None)
print res
print path
print '---------'
print path
plotMap(mymap, path)
