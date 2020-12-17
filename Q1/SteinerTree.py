import math

X_INDEX = 0
Y_INDEX = 1

steiner_vert_num = 0
terminal_vert_num = 0
vertices_num = 0
edges_num = 0
steiner_vert = [] # Steiner Vertices
terminal_vert = [] # Terminal Vertices
vertices = []
graph = [] # Our graph

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
    edge_cost = math.sqrt((v1[X_INDEX] - v2[X_INDEX])**2 + (v1[Y_INDEX] - v2[Y_INDEX])**2)
    graph[v1_index][v2_index] = edge_cost
    graph[v2_index][v1_index] = edge_cost


def init(file_name):
    global steiner_vert_num, terminal_vert_num, edges_num, graph
    with open(file_name, 'r') as reader:
        steiner_vert_num, terminal_vert_num, edges_num = [int(x) for x in next(reader).split()] # read first line
        for i in range(steiner_vert_num):
            x, y = [int(x) for x in next(reader).split()] # read steiner vertices coordinates
            steiner_vert.append((x, y))
            add_vertex((x, y))

        for i in range(terminal_vert_num):
            x, y = [int(x) for x in next(reader).split()] # read terminal vertices coordinates
            terminal_vert.append((x, y))
            add_vertex((x, y))

        graph = [[0 for x in range(vertices_num)] for y in range(vertices_num)] # Creating empty 2d vertex list

        for i in range(edges_num):
            v1_index, v2_index = [int(x) for x in next(reader).split()] # read vertices corresponding to each edge
            add_edge(v1_index, v2_index)

def calculate_cost():
    cost = sum(map(sum, graph)) / 2
    return cost

def print_debugging():
    print(steiner_vert_num, terminal_vert_num, edges_num)
    print("Vertices:", vertices)
    print("Graph:", graph)
    print("cost:", calculate_cost())



    


def main():
    init("steiner_in.txt")





if __name__ == '__main__':
    main()