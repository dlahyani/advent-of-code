from typing import Optional, Tuple, Set

def sum_of_k(numbers: Set[int], d: int, k: int) -> Optional[Tuple[int]]:
    """
    Find and return a tuple of `k` elements from `numbers` that their sum equals to `d`. If no such
    tuple exists, `None` is returned.

    Note: Given that item search in `numbers` is performed in complexity `O(1)` the overall
    complexity of this function is `O(n^(k-1))` where `n = |numbers|`.

    @param numbers - A set of integers from which to chose the tuple.
    @param d - The desired target number that the tuple sum should match. Must be an integer.
    @param k - Number of elements in the desired tuple. Must be a positive integer.

    @returns A tuple of numbers `T` such that: `T ⊆ numbers`, `|T| = k` and `sum(T) = d`.
    """
    if k == 1:
        return (d,) if d in numbers else None
    
    for n in numbers:
        # Find `(k - 1)` numbers that their sum equals to `(d - n)`. If we found such tuple 
        # then together with `n` we get total of `k` number which their sum equals to `d`.
        n_comp = sum_of_k(numbers, d - n, k - 1) 
        if n_comp:
            return n_comp + (n,)


if __name__ == "__main__":
    numbers = {int(l) for l in open("2020/01/input.txt", "r").readlines()}

    # Part 1
    n1, n2 =  sum_of_k(numbers, 2020, 2)
    print(f"Part 1: N1 = {n1}, N2 = {n2}, product = {n1 * n2}")

    # Part 2
    n1, n2, n3 = sum_of_k(numbers, 2020, 3)
    print(f"Part 2: N1 = {n1}, N2 = {n2}, N3 = {n3} product = {n1 * n2 * n3}")
