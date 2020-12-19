import math
import matplotlib.pyplot as plt
from ypstruct import structure
import numpy as np
import ga

steiner_vert_num = 0
terminal_vert_num = 0
vertices_num = 0
edges_num = 0
steiner_vert = [] # Steiner Vertices
terminal_vert = [] # Terminal Vertices
vertices = []
graph = [] # Our graph
edges = []

ss = [] # subset with all indices of terminal vertices


#add a vertex to the graph
def add_vertex(v):
    global graph
    global vertices_num
    global vertices
    vertices_num += 1
    vertices.append(v)
    if vertices_num > 1:
        for vertex in graph:
            vertex.append(0)
    temp = []
    for i in range(vertices_num):
        temp.append(0)
    graph.append(temp)


# Add an edge between vertices v1 and v2 with a weight of e
def add_edge(v1_index, v2_index):
    global graph
    global vertices_num
    global vertices
    v1 = vertices[v1_index]
    v2 = vertices[v2_index]
    edge_cost = math.sqrt((v1.x - v2.x)**2 + (v1.y - v2.y)**2)
    graph[v1_index][v2_index] = edge_cost
    graph[v2_index][v1_index] = edge_cost


def build_graph(edges_arr):
    global vertices_num
    res_graph = [ [0] * vertices_num for _ in range(vertices_num)]
    for e in edges_arr:
        if e.deleted == False:
            res_graph[e.v1][e.v2] = res_graph[e.v2][e.v1] = e.cost
    return res_graph


def init(file_name):
    global steiner_vert_num, terminal_vert_num, edges_num, graph, ss
    with open(file_name, 'r') as reader:
        steiner_vert_num, terminal_vert_num, edges_num = [int(x) for x in next(reader).split()] # read first line
        for i in range(steiner_vert_num):
            x, y = [int(x) for x in next(reader).split()] # read steiner vertices coordinates
            v = structure()
            v.x = x
            v.y = y
            steiner_vert.append(v)
            add_vertex(v)

        for i in range(terminal_vert_num):
            x, y = [int(x) for x in next(reader).split()] # read terminal vertices coordinates
            v = structure()
            v.x = x
            v.y = y
            terminal_vert.append(v)
            add_vertex(v)
            ss.append(i+steiner_vert_num)

        graph = [[0 for x in range(vertices_num)] for y in range(vertices_num)] # Creating empty 2d vertex list

        for i in range(edges_num):
            v1_index, v2_index = [int(x) for x in next(reader).split()] # read vertices corresponding to each edge
            add_edge(v1_index, v2_index)
            edge = structure()
            edge.v1 = v1_index
            edge.v2 = v2_index
            edge.deleted = False
            v1 = vertices[v1_index]
            v2 = vertices[v2_index]
            edge.cost =  math.sqrt((v1.x - v2.x)**2 + (v1.y - v2.y)**2)
            edges.append(edge)

def calculate_cost(graph_in):
    cost = int(sum(map(sum, graph_in)) / 2)
    is_a_tree = is_tree(graph_in)
    return cost, is_a_tree

def calculate_cost2(edges_arr):
    cost = int(sum(e.cost for e in edges_arr if e.deleted == False))
    cor_graph = build_graph(edges_arr)
    # is_a_tree = is_tree(cor_graph)
    terminals_connected = are_terminals_connected(cor_graph) 
    return cost, terminals_connected[0], terminals_connected[1]

def calculate_cost3(edges_arr):
    cost, terminals_connected, cc = calculate_cost2(edges_arr)
    if terminals_connected == False:
        cost = cost + 10000 * len(cc)
    return cost

def calculate_cost4(edges_arr):
    cost, terminals_connected, cc = calculate_cost2(edges_arr)
    return cost


def plot_graph(graph_in):
    terminal_vertices_x = [vertex.x for vertex in terminal_vert]
    terminal_vertices_y = [vertex.y for vertex in terminal_vert]
    plt.scatter(terminal_vertices_x, terminal_vertices_y, label= "Data", color= "red", linewidths=5, s=30)

    steiner_vertices_x = [vertex.x for vertex in steiner_vert]
    steiner_vertices_y = [vertex.y for vertex in steiner_vert]
    plt.scatter(steiner_vertices_x, steiner_vertices_y, label= "Data", color= "blue", s=30)

    for i in range(len(graph_in)):
        for j in range(len(graph_in)):
            if graph_in[i][j] != 0:
                x_values = [vertices[i].x, vertices[j].x]
                y_values = [vertices[i].y, vertices[j].y]
                #print("({}, {}) -> ({}, {})".format(vertices[i][0], vertices[i][1], vertices[j][0], vertices[j][1]))
                plt.plot(x_values, y_values, color='blue', linewidth=1)
    plt.show()


def plot_graph_vertices():
    terminal_vertices_x = [vertex.x for vertex in terminal_vert]
    terminal_vertices_y = [vertex.y for vertex in terminal_vert]
    plt.scatter(terminal_vertices_x, terminal_vertices_y, label= "Data", color= "red", linewidths=5, s=30)

    steiner_vertices_x = [vertex.x for vertex in steiner_vert]
    steiner_vertices_y = [vertex.y for vertex in steiner_vert]
    plt.scatter(steiner_vertices_x, steiner_vertices_y, label= "Data", color= "blue", s=30)

    plt.show()
    return plt.plot([], [], color='blue', linewidth=1)


'''
def update_line(hl, graph_in):
    for i in range(len(graph_in)):
        for j in range(len(graph_in)):
            if graph_in[i][j] != 0:
                x_values = [vertices[i].x, vertices[j].x]
                y_values = [vertices[i].y, vertices[j].y]
                #print("({}, {}) -> ({}, {})".format(vertices[i][0], vertices[i][1], vertices[j][0], vertices[j][1]))
                plt.plot(x_values, y_values, color='blue', linewidth=1) '''


# Checks whether there is a cycle in graph or not
def is_cyclic(v, graph_in, visited, parent): 

    # Mark current node as visited 
    visited[v] = True

    # Recur for every vertex adjacent to this vertex 
    for i in range (len(vertices)): 
        # If an adjacent vertex is not visited, recur for it
        if graph_in[v][i] != 0:
            if visited[i] == False: 
                if is_cyclic(i, graph_in, visited, v) == True: 
                    return True

            # If the adjacent vertex is visited and is not the parent of this graph, then there is a cycle
            elif i != parent and v != i: 
                return True

    # Graph is not cyclic if we reach this point
    return False
  

# Checks whether there is a cycle in graph or not
def is_tree(graph_in): 
    # making a list for all nodes, showing their visit status
    visited = [False] * len(vertices)

    # checks if there is a cycle in the graph
    # starting the check from the first terminal node
    start_index = steiner_vert_num # first terminal node index
    if is_cyclic(start_index, graph_in, visited, -1) == True: 
        return False

    # If a terminal vertex is not reachable then we return false
    for i in range(len(vertices)): 
        if visited[i] == False and vertices[i] in terminal_vert:
            return False
    
    return True


def DFSUtil(temp, v, visited, graph_in):
    # current vertex is now visited
    visited[v] = True

    # Store the vertex to list
    temp.append(v)

    # Repeat for all adjacent vertices to this vertex
    for i in range (len(vertices)):
        if graph_in[v][i] != 0:

            if visited[i] == False:

                # Update the list
                temp = DFSUtil(temp, i, visited, graph_in)
    return temp
 

# Method to find connected components in an undirected graph
def connectedComponents(graph_in):
    global ss
    visited = []
    cc = []
    for i in range(vertices_num):
        visited.append(False)
    for v in range(vertices_num):
        if visited[v] == False and v >= steiner_vert_num:
            temp = []
            cc.append(DFSUtil(temp, v, visited, graph_in))
    return cc

def are_terminals_connected(graph_in):
    global ss
    cc = connectedComponents(graph_in)
    for i in range(len(cc)):
        if all(elem in cc[i] for elem in ss):
            return True, cc
    return False, cc
    


def print_debugging():
    print(steiner_vert_num, terminal_vert_num, edges_num)
    print("Vertices:", vertices)
    print("Graph:", graph)
    print("cost:", calculate_cost(graph))



    


def main():
    
    init("steiner_in.txt")
    #init("test.txt")
    #init("test2.txt")
    #init("test3.txt")
    #plot_graph(graph)

    #print(are_terminals_connected(graph))
    #print(connectedComponents(graph))
    #print(ss)

    ncost = calculate_cost(graph)
    wcost = calculate_cost2(edges)

    plot_graph(graph)

    print("Tree which contants all of the terminal nodes?", ncost, wcost)

    # Defining the problem
    problem = structure()
    problem.graph = graph
    problem.cost = calculate_cost3
    problem.nvar = int(len(vertices)/2) # number of variables
    problem.steiner_vert = steiner_vert
    problem.terminal_vert = terminal_vert
    problem.vertices = vertices
    problem.edges = edges
    problem.plot_graph = plot_graph
    problem.build_graph = build_graph
    problem.calculate_cost4 = calculate_cost4


    # Defining the parameters
    params = structure()
    params.npop = 25 # ancestors population number
    params.pc = 4 # children population is pc times the npop
    params.maxit = 200 # maximum number of iterations
    params.npoints = 2 # number of points for crossover
    params.mu = 0.2 # mutation probability
    params.beta = 1

    # running the GA algorithm
    ga.run(problem, params)









if __name__ == '__main__':
    main()