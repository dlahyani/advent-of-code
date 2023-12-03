from typing import List, Optional, Set, Tuple

PREAMBLE_LEN = 25


def sum_of_k(numbers: Set[int], d: int, k: int) -> Optional[Tuple[int]]:
    """
    Find and return a tuple of `k` elements from `numbers` that their sum equals to `d`. If no such
    tuple exists, `None` is returned.

    Note: Given that item search in `numbers` is performed in complexity `O(1)` the overall
    complexity of this function is `O(n^(k-1))` where `n = |numbers|`.

    Returns A tuple of numbers `T` such that: `T ⊆ numbers`, `|T| = k` and `sum(T) = d`.
    """
    if k == 1:
        return (d,) if d in numbers else None

    for n in numbers:
        n_comp = sum_of_k(numbers, d - n, k - 1)
        if n_comp:
            return n_comp + (n,)


def find_xmas_break(numbers: List[int], preamble_size: int) -> int:
    """
    Find the first number in the list (after the preamble of size `preamble_size`) which is not the
    sum of two of the `preamble_size` numbers before it.

    Run-time complexity of this functions is `O(n * preamble_size)` where `n  = len(numbers)`.

    Returns the index of the first element that breaks the XMAS cypher consistency, or `None` if no
    such element found.
    """
    preamble = set(numbers[:preamble_size])
    for i in range(preamble_size, len(numbers)):
        if not sum_of_k(preamble, numbers[i], 2):
            return i

        preamble.remove(numbers[i - preamble_size])
        preamble.add(numbers[i])


def find_seq_with_sum(numbers: List[int], target_sum: int) -> Optional[Tuple[int]]:
    """
    Finds a sequence of elements in `numbers` that their sum equals exactly to `target_sum`. The
    sequence can be of any length (greather than 1 of course).

    Run-time complexity of this function is `O(n)`.

    Returns the indexes of the first and the last elements of the sequence, or `None` if no such
    sequence found.
    """
    # Run with 2 pointers on the list which respectively mark the beginning and end of the sequence
    # to check. If the sum of that sequence matches `target_sum` we return the 2 pointers, if the
    # sum is too small we move froward the end marker (adding one more element to the sequence), and
    # if the sum is too high we move forward the start marker (removing one element from the
    # sequence). This way we scan the entire list until we find a matching sequence or both markers
    # reach the end of the list.
    seq_start = 0
    seq_end = 0
    seq_sum = numbers[0]

    while seq_start < len(numbers) - 2:
        if seq_sum == target_sum:
            return seq_start, seq_end
        elif seq_sum < target_sum:
            seq_end += 1
            seq_sum += numbers[seq_end]
        else:
            seq_sum -= numbers[seq_start]
            seq_start += 1

        if seq_start > seq_end:
            seq_end = seq_start
            seq_sum = numbers[seq_start]


if __name__ == "__main__":
    numbers = [int(line) for line in open("2020/09/input.txt", "r").readlines()]

    # Part 1
    xmas_break_index = find_xmas_break(numbers, PREAMBLE_LEN)
    xmas_break_value = numbers[xmas_break_index]
    print(f"XMAS is broken at index {xmas_break_index}, {xmas_break_value}")

    # Part 2
    seq_range = find_seq_with_sum(numbers, xmas_break_value)
    seq = numbers[seq_range[0] : seq_range[1] + 1]
    xmas_weakness = min(seq) + max(seq)
    print(f"XMAS encryption weakness value is: {xmas_weakness}")
