
from functools import reduce
from math import ceil

def get_common_bit(bits):
    return 1 if sum(bits) >= ceil(len(bits) / 2) else 0

def stringify_bits(bits):
    return "".join([str(b) for b in bits])

def bits_array_to_int(bits):
    return int(stringify_bits(bits), base=2)

def get_common_bit_at_index(reads, i):
    return get_common_bit(list(zip(*reads))[i])

def get_reads_matching_bit_at_index(reads, value, i):
    return list(filter(lambda c: c[i] == value, reads))

def get_reads_matching_rule_at_index(reads, rule, i):
    if len(reads) == 1:
        return reads
    
    bit = get_common_bit_at_index(reads, i) ^ int(rule == "lcb")
    return get_reads_matching_bit_at_index(reads, bit, i)
    
with open("2021/03/input.txt") as f:
    reads = [[int(b) for b in l.strip()] for l in f.readlines()]


bit_count = len(reads[0])
print(f"Total reads: {len(reads)}, read size: {bit_count}")
gamma = [get_common_bit(zr) for zr in zip(*reads)]
epsilon = [b ^ 1 for b in gamma]
pwc = bits_array_to_int(gamma) * bits_array_to_int(epsilon)
print(f"The Submarine power consumption is: {pwc} (gamma={gamma}, epsilon={epsilon})")


ox_gen_rating_bits = reduce(
    lambda r, i: get_reads_matching_rule_at_index(r, "mcb", i), range(bit_count), reads
)[0]
co2_scrub_rating_bits = reduce(
    lambda r, i: get_reads_matching_rule_at_index(r, "lcb", i), range(bit_count), reads
)[0]

print(f"Oxygen generator rating value: {''.join([str(i) for i in ox_gen_rating_bits])}")
print(f"CO2 scrubber rating value: {''.join([str(i) for i in co2_scrub_rating_bits])}")


ox_gen_rating = bits_array_to_int(ox_gen_rating_bits)
co2_scrub_rating = bits_array_to_int(co2_scrub_rating_bits)
print(f"Oxygen generator rating value: {ox_gen_rating} {ox_gen_rating_bits}")
print(f"CO2 scrubber rating value: {co2_scrub_rating} {co2_scrub_rating_bits}")

life_support_rating = ox_gen_rating * co2_scrub_rating
print(f"Life support rating in the submarine is: {life_support_rating}")