import time
import os
import numpy
basic_operations = 0

def main():
    prompt = int(input("Which world you want to use? 1 or 2?"))
    if prompt == 1:
        input_name = "world1"
    elif prompt == 2:
        input_name = "world2"

    i = 0
    for file in os.listdir():
        if file.startswith(input_name) and file.endswith(".dat"):
            i += 1
            print(input_name)
            maze = worldGenerator(input_name)
            #maze = readMazeFromFile(file)
            start = findStart(maze)
            end = findEnd(maze)

            startTime = time.time()
            path = WavefrontPlanner(maze, start, end)
            endTime = time.time()

            if path == None:
                printMaze(maze)
                print("No path to destination.")
            else:
                printPath(maze, path)
                print("Shortest path: ")
                print(path)

            print("Time taken:", endTime-startTime, "secs")
            print("Basic operations: ", basic_operations)
            print("\n")


def worldGenerator(input_nm):
    removespaces(input_nm)
    i = 0
    for file in os.listdir():
        if file.startswith(input_nm) and file.endswith(".dat"):
            myworld = readWorldFromFile(file)
            myworld = worldTransformation(myworld)
            myworld = worldPadding(myworld)
            return myworld

def removespaces(input_n):
    if input_n == "world1":
        with open('world1.dat', 'r') as f:
            lines = f.readlines()
    elif input_n == "world2":
        with open('world2.dat', 'r') as f:
            lines = f.readlines()
    # remove spaces
    lines = [line.replace(' ', '') for line in lines]

    # finally, write lines in the file
    if input_n == "world1":
        with open('world1.dat', 'w') as f:
            f.writelines(lines)

    if input_n == "world2":
        with open('world2.dat', 'w') as f:
            f.writelines(lines)


def readWorldFromFile(f):
    world = list()
    with open(f) as file:
        for line in file:
            world.append(list(line.rstrip()))
    return world

def worldTransformation(world):
    for i in range(len(world)):
        for j in range(len(world[0])):
            if world[i][j] == '0':
                world[i][j] = '.'
            elif world[i][j] == '1':
                world[i][j] = '*'
    return world

def worldPadding(world):
    rows = len(world)
    cols = len(world[0])
    #print(rows,cols)
    reference = numpy.zeros((rows+2,cols+2))
    reference = reference.tolist()

    for i in range(len(reference)):
        for j in range(len(reference[0])):
            reference[i][j] = '*'

    reference = numpy.array(reference)
    world = numpy.array(world)

    reference[1:rows+1,:][:,1:cols+1] = world
    reference = reference.tolist()
    return reference


def WavefrontPlanner(maze, start, end):
    queue = [start]
    visited = set()
    while len(queue) != 0:
        if queue[0] == start:
            path = [queue.pop(0)]
        else:
            path = queue.pop(0)
        front = path[-1]
        if front == end:
            return path
        elif front not in visited:
            for adjacentSpace in getAdjacentSpaces(maze, front, visited):
                newPath = list(path)
                newPath.append(adjacentSpace)
                queue.append(newPath)
                global basic_operations
                basic_operations += 1
            visited.add(front)
    return None

def getAdjacentSpaces(maze, space, visited):
    spaces = list()
    spaces.append((space[0]-1, space[1]))  # Up
    spaces.append((space[0]+1, space[1]))  # Down
    spaces.append((space[0], space[1]-1))  # Left
    spaces.append((space[0], space[1]+1))  # Right
    final = list()
    for i in spaces:
        if maze[i[0]][i[1]] != '*' and i not in visited:
            final.append(i)
    return final

def findStart(maze):
    x = int(input("Enter x coordinate of starting point -> "))
    y = int(input("Enter y coordinate of starting point -> "))
    maze[x][y] = 's'
    return tuple([x, y])

def findEnd(maze):
    x = int(input("Enter x coordinate of destination -> "))
    y = int(input("Enter y coordinate of destination -> "))
    maze[x][y] = 'e'
    return tuple([x, y])

def readMazeFromFile(f):
    maze = list()
    with open(f) as file:
        for line in file:
            maze.append(list(line.rstrip()))
    return maze

def printMaze(maze):
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            print(maze[i][j], end="")
        print()

def printPath(maze, path):
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if tuple([i, j]) in path and maze[i][j] != 's' and maze[i][j] != 'e':
                print("x", end="")
            else:
                print(maze[i][j], end="")
        print()

if __name__ == "__main__":
    main()
