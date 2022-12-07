from collections import Counter


def find_first_distinct_sequence(data: str, seq_len: int) -> int:
    counter = Counter(data[0:seq_len])
    distinct_seq_index = -1
    for i in range(seq_len, len(data)):
        if counter.most_common(1)[0][1] == 1:
            distinct_seq_index = i
            break
        
        counter.subtract({data[i-seq_len]: 1})
        counter.update(data[i])
    
    return distinct_seq_index
    
data = open("2022/06/input.txt").read()

# Part 1
first_packet_index = find_first_distinct_sequence(data, 4)
print(f"First packet starts at index: {first_packet_index}")

# Part 2
first_message_index = find_first_distinct_sequence(data, 14)
print(f"First message starts at index: {first_message_index}")
