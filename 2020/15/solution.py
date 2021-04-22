
def memory_game(init_sequence, t):
    assert len(init_sequence) > 0
    assert t >= len(init_sequence)

    # Each entry in this dictionary maps a number N that appeared in the game to a pair of two number
    # (i, D) such that i is the index of the last appearance of N and D is the difference between i
    # and the previous appearance of N or 0 if N first appeared at index i.
    # By consistently updating this dictionary, in order to calculate the (J+1)th element we just take
    # d[K][1] where K is the value of the Jth element. In other words in order to calculate the value
    # of element (J+1) we just need d (this dict) and the value of the Jth element.
    d = {}

    # initialize
    for i in range(len(init_sequence)):
        cur = init_sequence[i]
        is_new = cur not in d
        d[cur] = (i, 0 if is_new else (i - d[cur][0]))

    for i in range(len(init_sequence), t):
        cur = d[cur][1]
        is_new = cur not in d
        d[cur] = (i, 0 if is_new else i - d[cur][0])

    return cur


if __name__ == "__main__":
    numbers = [int(i) for i in open("2020/15/input.txt", "r").read().split(",")]
    print(f"Initial sequence: {numbers}")

    # Part 1
    n = memory_game(numbers, 2020)
    print(f"2020th number is: {n}")

    # Part 2
    n = memory_game(numbers, 30_000_000)
    print(f"30000000th number is: {n}")
