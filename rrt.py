import matplotlib.pyplot as plt
import math
import random
import sys

def near_node(nx, ny, nd_list):
    dist_list = []
    for i in range(len(nd_list)):
        dist = math.sqrt(((nx - nd_list[i][0])**2)+((ny - nd_list[i][1])**2))
        dist_list.append(dist)
    return dist_list.index(min(dist_list))

def planning(sx, sy, gx, gy, ox, oy, grid_size, max_iter):
    min_x = 0
    min_y = 0
    max_x = round(max(ox))
    max_y = round(max(oy))

    x_width = round((max_x - min_x) / grid_size)
    y_width = round((max_y - min_y) / grid_size)

    obstacle_map = [[False for _ in range(y_width)]
                    for _ in range(x_width)]
    for ix in range(x_width):
        x = ix * grid_size
        for iy in range(y_width):
            y = iy * grid_size
            for iox, ioy in zip(ox, oy):
                d = math.hypot(iox - x, ioy - y)
                if d <= 1.0:
                    obstacle_map[ix][iy] = True
                    break

    possible_nodes = [[0 for row in range(y_width)] for col in range(x_width)]
    possible_nodes[round(sy / grid_size)][round(sx / grid_size)] = 5

    nd_list = [(round(sx / grid_size), round(sy / grid_size))]
    connective = {}

    goal = False
    iterations = 0

    while iterations < max_iter:
        nx = random.randint(0, x_width)
        ny = random.randint(0, y_width)

        near_ind = near_node(nx, ny, nd_list)
        near_x = nd_list[near_ind][0]
        near_y = nd_list[near_ind][1]
        near_point = near_x, near_y

        delta_x = nx - near_x
        delta_y = ny - near_y

        if abs(delta_x) >= abs(delta_y):
            delta_x = 1 if delta_x > 0 else -1
            delta_y = 0
        else:
            delta_y = 1 if delta_y > 0 else -1
            delta_x = 0

        nd = near_x + delta_x, near_y + delta_y

        if 0 <= nd[0] < x_width and 0 <= nd[1] < y_width:
            if possible_nodes[nd[1]][nd[0]] == 0 and obstacle_map[nd[0]][nd[1]] == 0:
                possible_nodes[nd[1]][nd[0]] = 3
                nd_list.append(nd)
                connective[nd] = near_point
                if nd[0] == round(gx / grid_size) and nd[1] == round(gy / grid_size):
                    print("Goal found!")
                    goal = True
                    break
        iterations += 1

    if goal == True:
        route = []
        connecting = nd
        route.append(connecting)
        while connecting in connective:
            route.append(connective[connecting])
            connecting = connective[connecting]
            route.sort()

        px = []
        py = []

        for i in range(0, len(route)):
            px.append(route[i][0] * grid_size)
            py.append(route[i][1] * grid_size)

        return px, py

    else:
        print("Path not found")
        sys.exit(0)

def preprocess():
    sx = 5.0
    sy = 5.0
    gx = 50.0
    gy = 50.0
    grid_size = 4.0
    max_iter = 1000

    ox, oy = [], []
    for i in range(0, 60):
        ox.append(i)
        oy.append(0.0)
    for i in range(0, 60):
        ox.append(60.0)
        oy.append(i)
    for i in range(0, 61):
        ox.append(i)
        oy.append(60.0)
    for i in range(0, 61):
        ox.append(0.0)
        oy.append(i)
    for i in range(11):
        ox.append(i + 10)
        oy.append(20)
    for i in range(11):
        oy.append(i + 10)
        ox.append(20)
    for i in range(11):
        ox.append(i + 40)
        oy.append(40)
    for i in range(11):
        oy.append(i + 40)
        ox.append(40)
    for i in range(21):
        ox.append(i + 40)
        oy.append(20)
    for i in range(21):
        ox.append(i)
        oy.append(40)

    plt.plot(ox, oy, "sk")
    plt.plot(sx, sy, "xg")
    plt.plot(gx, gy, "xb")
    plt.grid(True)
    plt.axis("equal")

    px, py = planning(sx, sy, gx, gy, ox, oy, grid_size, max_iter)

    plt.plot(px, py, "sr")
    plt.pause(0.01)
    plt.show()

if __name__ == '__main__':
    preprocess()