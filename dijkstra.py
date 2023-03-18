import matplotlib.pyplot as plt
import math

def planning(sx, sy, gx, gy, ox, oy, grid_size):
    motion = [[-1, 0],
             [0, -1],
             [1, 0],
             [0, 1]]

    cost = 1

    goal = False

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

    dist = 0
    nearest_nodes = [(dist, round(sx / grid_size), round(sy / grid_size))]
    connective = {}

    while len(nearest_nodes) != 0:
        nearest_nodes.sort(reverse=True)
        current_node = nearest_nodes.pop()

        if current_node[1] == round(gx / grid_size) and current_node[2] == round(gy / grid_size):
            print("Goal found!")
            goal = True
            break

        dist, x, y = current_node

        for move_x, move_y in motion:
            movement_x = x + move_x
            movement_y = y + move_y
            if 0 <= movement_x < x_width and 0 <= movement_y < y_width:
                if possible_nodes[movement_y][movement_x] == 0 and obstacle_map[movement_x][movement_y] == 0:
                    possible_nodes[movement_y][movement_x] = 3
                    possible_node = (dist + cost, movement_x, movement_y)
                    nearest_nodes.append(possible_node)
                    connective[possible_node] = current_node

                    plt.plot(movement_x * grid_size, movement_y * grid_size, "x", color='tab:gray')
                    plt.pause(0.001)

    if goal == True:
        route = []
        connecting = current_node
        route.append(connecting)
        while connecting in connective:
            route.append(connective[connecting])
            connecting = connective[connecting]
            route.sort()

    px = []
    py = []

    for i in range(0, len(route)):
        px.append(route[i][1] * grid_size)
        py.append(route[i][2] * grid_size)

    return px, py

def preprocess():
    sx = 5.0
    sy = 5.0
    gx = 50.0
    gy = 50.0
    grid_size = 4.0

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

    px, py = planning(sx, sy, gx, gy, ox, oy, grid_size)

    plt.plot(px, py, "sr")
    plt.pause(0.01)
    plt.show()

if __name__ == '__main__':
    preprocess()