import networkx as nx
import matplotlib.pyplot as plt
import sys, getopt
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


def draw_graph(graph, path):
    path_edges = [sorted((path[i], path[i + 1]))
                  for i in range(len(path) - 1)]
    pos = nx.spring_layout(graph)

    sorted_graph_edges = list(map(
        lambda edge: sorted(edge), graph.edges()))

    edge_colors = color_graph_element(path_edges,
                                      sorted_graph_edges, 'red', 'blue')
    node_colors = color_graph_element(path, graph,
                                      'red', 'blue')

    plt.figure(1)
    nx.draw_networkx(graph, node_color=node_colors,
                     edge_color=edge_colors, with_labels=True, pos=pos)
    nx.draw_networkx_edge_labels(graph, pos=pos)
    plt.show()


def main(argv):
    nodes_cnt = 0
    start_node = 0
    end_node = 0
    hint = 'a_star.py -n <nodes_number> ' \
           '-s <start_node> -e <end_node>'

    try:
        opts, args = getopt.getopt(argv, "h:n:s:e:",
                                   ["nodes_number=", "start_node=",
                                    "end_node="])
        if len(opts) == 0:
            print(hint)
            sys.exit(2)
    except getopt.GetoptError:
        print(hint)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print(hint)
            sys.exit()
        elif opt in ("-n", "--nodes_number"):
            print(arg)
            nodes_cnt = int(arg)
        elif opt in ("-s", "--start_node"):
            print(arg)
            start_node = int(arg)
        elif opt in ("-e", "--end_node"):
            print(arg)
            end_node = int(arg)
    input_validation(nodes_cnt, start_node, end_node)
    solve_problem(nodes_cnt, start_node, end_node)


def input_validation(nodes_cnt, start_node, end_node):
    if start_node > nodes_cnt - 1 \
            or end_node > nodes_cnt - 1:
        print('Wybrany wezel poczatkowy lub koncowny nie istnieje.'
              ' Dostepne wezly: 0, 1, ...' + nodes_cnt - 1)
        sys.exit(2)
    elif nodes_cnt < 1:
        print('Liczba wezlow musi byc wieksza niz 1')
        sys.exit(2)


def solve_problem(nodes_cnt, start_node, end_node):
    graph = create_graph(nodes_cnt)

    try:
        path = nx.astar_path(graph, start_node, end_node)
        length = nx.astar_path_length(graph, start_node, end_node)
        print('Path: ' + str(path))
        print('Length: ' + str(length))
        draw_graph(graph, path)
    except nx.exception.NetworkXNoPath:
        print('Node {0} is not reachable from {1}'
              .format(str(end_node), str(start_node)))


if __name__ == "__main__":
    main(sys.argv[1:])
