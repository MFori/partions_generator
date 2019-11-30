# Set partitions generator
# Author: Martin Forejt
# Version: 1.0
# Email: forejt.martin97@gmail.com

import sys
import random

# generate all partitions for given N
MODE_ALL = 1
# generate one random partition for given N
MODE_RANDOM = 2
# generate the next partition for given current partition
MODE_NEXT = 3

SUPPORTED_MODES = [MODE_ALL, MODE_RANDOM, MODE_NEXT]


def print_partition(partition):
    # print formatted partition
    parts = max(partition)
    print("{", end="")

    for p in reversed(range(1, parts + 1)):
        part = [(i + 1) for i in range(len(partition)) if partition[i] == p]
        if len(part) == 0:
            break
        print("{", end="")
        print(*part, sep=",", end="")
        if p > 1:
            print("},", end="")
        else:
            print("}", end="")

    print("}")


def next_partition(prev, m, n):
    # return next partition for prev partition
    i = 0
    prev[i] += 1
    while (i < n - 1) and (prev[i] > m[i + 1] + 1):
        prev[i] = 1
        i += 1
        prev[i] += 1

    if i == n - 1:
        return -1

    if prev[i] > m[i]:
        m[i] = prev[i]
    for j in range(0, i - 1):
        m[j] = m[i]

    return prev


def random_partition(n):
    # generate random partition
    items = [0] * n
    groups = random.randint(1, n)

    # first i items add to i group
    for i in range(0, groups):
        items[i] = i + 1

    # next items add to random group
    for i in range(groups, n):
        items[i] = random.randint(1, groups)

    random.shuffle(items)
    return items


def all_partitions(n):
    # generate all partitions
    count = 0
    partition = [1] * n
    m = [1] * n

    while partition != -1:
        print_partition(partition)
        print("m: ", end="")
        print(m)
        print("s: ", end="")
        print(partition)
        partition = next_partition(partition, m, n)
        count += 1

    print("Total partitions: " + str(count))
    return


def print_help():
    # print help
    print("MODES: 1 => ALL, 2 => RANDOM, 3 => NEXT")
    print("set 'mode' 'arg'")
    print("set 1/2 'N' (integer 1 5)")
    print("set 3 'partition mask' (integer 3 1,2,2,3,1,4,1) represents: {{1,5},{2,3,7},{4},{6}}")


def parse_args(argv):
    # parse cmd args
    if len(argv) < 2:
        return -1

    try:
        mode = int(argv[0])
        if mode not in SUPPORTED_MODES:
            return -1
    except ValueError:
        return -1

    if mode == MODE_NEXT:
        partition = [int(i) for i in argv[1].split(',')]
        return [mode, partition]
    else:
        try:
            n = int(argv[1])
        except ValueError:
            return -1
        return [mode, n]


def main(argv):
    conf = parse_args(argv)
    if conf == -1:
        print_help()
        return

    # print("configuration: ", end="")
    # print(conf)

    if conf[0] == MODE_ALL:
        all_partitions(conf[1])
    elif conf[0] == MODE_RANDOM:
        partition = random_partition(conf[1])
        print("Random partition: ", end="")
        print_partition(partition)
    else:
        m = [1] * len(conf[1])
        partition = next_partition(conf[1], m, len(conf[1]))
        print("Next partition is: ", end="")
        print_partition(partition)
    return


if __name__ == '__main__':
    main(sys.argv[1:])
