from random import Random
from time import time
import math
import sys
import getopt
from random import randint
import inspyred


def print_result(result):
    print('Result: {0}: {1}'.format(str(result.candidate),
                                    result.fitness))


def create_items():
    items = [(randint(1, 20), randint(100, 500)) for i in range(100)]
    print(items)
    return items


def calculate(items, limit):
    prng = Random()
    prng.seed(time())
    problem = inspyred.benchmarks.Knapsack(limit, items, duplicates=False)
    ac = inspyred.swarm.ACS(prng, problem.components)
    ac.terminator = inspyred.ec.terminators.generation_termination
    final_pop = ac.evolve(problem.constructor, problem.evaluator,
                          maximize=problem.maximize, pop_size=50,
                          max_generations=50)
    return max(ac.archive)


def input_validation(nodes_cnt):
    if nodes_cnt < 1:
        print('Liczba wezlow musi byc wieksza niz 1')
        sys.exit(2)


def main(argv):
    limit = 0

    try:
        opts, args = getopt.getopt(argv, "hl:", ["help", "limit="])
        if len(opts) == 0:
            print 'knapsack-ant-colony.py -l <limit>'
    except getopt.GetoptError:
        print(str(getopt.GetoptError))
        print 'knapsack-ant-colony.py -l <limit>'
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print 'knapsack-ant-colony.py -l <limit>'
            sys.exit()
        elif opt in ("-l", "--limit"):
            limit = int(arg)

    items = create_items()

    result = calculate(items, 30)

    print_result(result)


if __name__ == "__main__":
    main(sys.argv[1:])
