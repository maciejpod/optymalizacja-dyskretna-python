from random import Random
from time import time
import inspyred
import sys
import getopt
from random import randint
import networkx as nx
import matplotlib.pyplot as plt


def create_graph(nodes_cnt):
    graph = nx.complete_graph(nodes_cnt)
    for n1, n2, prop in graph.edges(data=True):
        prop['weight'] = randint(1, 1000)
    return graph


def calculate_distances(graph):
    distances = [[0 for _ in range(len(graph.nodes()))]
                 for _ in range(len(graph.nodes()))]
    for a, b in graph.edges():
        distances[a][b] = graph.get_edge_data(a, b)['weight']
        distances[b][a] = graph.get_edge_data(a, b)['weight']
    return distances


def color_graph_element(path, elements, color_1, color_2):
    colors = []

    for element in elements:
        if element in path:
            colors.append(color_1)
        else:
            colors.append(color_2)
    return colors


def calculate_path(distances):
    problem = inspyred.benchmarks.TSP(distances)
    prng = Random()
    prng.seed(time())
    ac = inspyred.swarm.ACS(prng, problem.components)
    ac.terminator = inspyred.ec.terminators.generation_termination
    ac.evolve(generator=problem.constructor,
              evaluator=problem.evaluator,
              bounder=problem.bounder,
              maximize=problem.maximize,
              pop_size=20,
              max_generations=100)
    best = max(ac.archive)
    path = []
    for b in best.candidate:
        path.append(b.element[0])
    path.append(best.candidate[-1].element[1])
    return path


def draw_graph(graph, path):
    path_edges = [sorted((path[i], path[i + 1]))
                  for i in range(len(path) - 1)]

    sorted_graph_edges = list(map(
        lambda edge: sorted(edge), graph.edges()))

    edge_colors = color_graph_element(path_edges,
                                      sorted_graph_edges, 'red', 'blue')
    color_map = color_graph_element(path, graph,
                                    'red', 'blue')

    pos = nx.spring_layout(graph)
    plt.figure(1)
    nx.draw_networkx(graph, node_color=color_map,
                     edge_color=edge_colors,
                     with_labels=True, pos=pos)
    nx.draw_networkx_edge_labels(graph, pos=pos)
    plt.show()


def solve_problem(nodes_cnt):
    graph = create_graph(nodes_cnt)

    distances = calculate_distances(graph)
    path = calculate_path(distances)

    print('Path: ' + path)

    draw_graph(graph, path)


def input_validation(nodes_cnt):
    if nodes_cnt < 1:
        print('Liczba wezlow musi byc wieksza niz 1')
        sys.exit(2)


def main(argv):
    nodes_cnt = 0

    try:
        opts, args = getopt.getopt(argv, "hi:o:",
                                   ["nodes_number="])
        if len(opts) == 0:
            print 'ant_colony.py -nn <nodes_number>'
            sys.exit(2)
    except getopt.GetoptError:
        print 'ant_colony.py -nn <nodes_number>'
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print 'ant_colony.py -nn <nodes_number>'
            sys.exit()
        elif opt in ("-nn", "--nodes_number"):
            nodes_cnt = int(arg)
    input_validation(nodes_cnt)
    solve_problem(nodes_cnt)


if __name__ == "__main__":
    main(sys.argv[1:])
