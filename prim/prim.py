import networkx as nx
import matplotlib.pyplot as plt
import sys
import getopt
from random import randint


def create_graph(nodes_cnt):
    max_edges = int((nodes_cnt * (nodes_cnt - 1)) / 2)
    graph = nx.gnm_random_graph(nodes_cnt,
                                randint(nodes_cnt, max_edges))
    for n1, n2, prop in graph.edges(data=True):
        prop['weight'] = randint(1, 1000)
    return graph


def color_graph_element(path, elements, color_1, color_2):
    colors = []

    for element in elements:
        if element in path:
            colors.append(color_1)
        else:
            colors.append(color_2)
    return colors


def draw_graph(graph, path_edges):
    pos = nx.spring_layout(graph)

    sorted_graph_edges = list(map(
        lambda edge: sorted(edge), graph.edges()))

    path_edges = list(map(
        lambda edge: sorted((edge[0], edge[1])), path_edges))
    path = []
    for n1, n2 in path_edges:
        path.append(n1)
        path.append(n2)

    edge_colors = color_graph_element(path_edges,
                                      sorted_graph_edges, 'red', 'blue')
    node_colors = color_graph_element(set(path), graph,
                                      'red', 'blue')

    plt.figure(1)
    nx.draw_networkx(graph, node_color=node_colors,
                     edge_color=edge_colors, with_labels=True, pos=pos)
    nx.draw_networkx_edge_labels(graph, pos=pos)
    plt.show()


def solve_problem(nodes_cnt):
    graph = create_graph(nodes_cnt)

    spanning_tree_edges = list(nx.minimum_spanning_edges(
        graph, algorithm='prim'))

    print('Path: ' + str(spanning_tree_edges))

    draw_graph(graph, spanning_tree_edges)


def input_validation(nodes_cnt):
    if nodes_cnt < 1:
        print('Liczba wezlow musi byc wieksza niz 1')
        sys.exit(2)


def main(argv):
    nodes_cnt = 0

    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["nodes_number="])
        if len(opts) == 0:
            print 'prim.py -nn <nodes_number>'
            sys.exit(2)
    except getopt.GetoptError:
        print 'prim.py -nn <nodes_number>'
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print 'prim.py -nn <nodes_number>'
            sys.exit()
        elif opt in ("-nn", "--nodes_number"):
            nodes_cnt = int(arg)
    input_validation(nodes_cnt)
    solve_problem(nodes_cnt)


if __name__ == "__main__":
    main(sys.argv[1:])
