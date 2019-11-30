# Integer partitions generator
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
    print("{", end="")
    print(*[i for i in partition if i != 0], sep=",", end="")
    print("}")


def get_sum(partition, end):
    # sum partition from begin to 'end'
    return sum(partition[0:end])


def next_partition(prev, n):
    # return next partition for prev partition
    for i in range(len(prev), n):
        prev.append(0)
    pos = len(prev) - 1

    while pos >= 0:
        if prev[pos] > 1:
            break
        pos -= 1

    if pos < 0:
        return -1

    prev[pos] -= 1
    val = prev[pos]
    pos += 1
    c_sum = get_sum(prev, pos)
    add = n - c_sum

    while add > 0:
        if val > add:
            val -= 1
        else:
            prev[pos] = val
            add -= val
            pos += 1

    return [i for i in prev if i != 0]


def random_partition(n):
    # generate random partition
    c_sum = n
    partition = []

    while c_sum != 0:
        i = random.randint(1, c_sum)
        c_sum -= i
        partition.append(i)

    return sorted(partition, reverse=True)


def all_partitions(n):
    # generate all partitions
    count = 0
    partition = [n]

    while partition != -1:
        print_partition(partition)
        partition = next_partition(partition, n)
        count += 1

    print("Total partitions: " + str(count))
    return


def print_help():
    # print help
    print("MODES: 1 => ALL, 2 => RANDOM, 3 => NEXT")
    print("integer 'mode' 'arg'")
    print("integer 1/2 'N' (integer 1 5)")
    print("integer 3 'partition' (integer 3 4,1,1)")


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
        partition = next_partition(conf[1], get_sum(conf[1], len(conf[1])))
        print("Next partition is: ", end="")
        print_partition(partition)
    return


if __name__ == '__main__':
    main(sys.argv[1:])
