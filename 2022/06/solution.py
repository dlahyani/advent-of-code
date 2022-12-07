from collections import Counter

def find_first_distinct_sequence(data: str, k: int) -> int:
    # Scan data using a sliding window of size k and identify if the window contains distinct chars.
    # Use a Counter to track the exact number of occurrences of all chars within the window. As we
    # slide the window right we decrement the counter of left-most char in the window and increment
    # the counter for the new char on the right.
    # By removing items from the Counter when they reach count of 0 we promise that len(counter)
    # is the number of unique chars in the window, thus being able to test uniqueness in O(1)
    # complexity (assuming len(Counter) is an O(1) operation).
    
    window_counter = Counter(data[0:k])
    for i in range(k, len(data)):
        if len(window_counter) == k:
            return i
        
        w0, wk = data[i-k], data[i]
        window_counter.subtract(w0)
        if window_counter[w0] == 0:
            del window_counter[w0]
        window_counter.update(wk)
    
    return -1
    
data = open("2022/06/input.txt").read()

# Part 1
first_packet_index = find_first_distinct_sequence(data, 4)
print(f"First packet starts at index: {first_packet_index}")

# Part 2
first_message_index = find_first_distinct_sequence(data, 14)
print(f"First message starts at index: {first_message_index}")
