def find_positive_derivatives(seq, window_size):
    derivatives = [seq[i + window_size] - seq[i] for i in range(len(seq) - window_size)]
    return list(filter(lambda d: d > 0, derivatives))


with open("2021/01/input.txt") as f:
    measurements = [int(l) for l in f.readlines()]

# Part 1:
print("***** Part 1:")
print(f"Number of positives derivatives is {len(find_positive_derivatives(measurements, 1))}")

# Part 2:
print("***** Part 2:")
print(f"Number of positives derivatives is {len(find_positive_derivatives(measurements, 3))}")
