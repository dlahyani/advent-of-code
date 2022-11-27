from sympy.ntheory.modular import crt



with open("2020/13/input.txt") as f:
    arrival_time = int(f.readline())
    buses = [int(b) if b != "x" else -1 for b in f.readline().split(",")]
    
print(f"Estimated arrival time to the bus station: {arrival_time}")

earliest_possible_departure_time = -1
bus_id = 0
cur_time = arrival_time
while earliest_possible_departure_time == -1:
    for b in buses:
        if b == -1:
            continue
        if cur_time % b == 0:
            earliest_possible_departure_time = cur_time
            bus_id = b
            break
    cur_time += 1

wait_time = earliest_possible_departure_time - arrival_time
score = wait_time * bus_id
print(f"Earliest possible departure at {earliest_possible_departure_time} (waiting for {wait_time} min.) on bus {bus_id}, score: {score}")

### Part 2:
# requires sympy package for Chinese Remainder Theorem implementation.
n = list(filter(lambda b: b != -1, buses))
b = list(map(lambda ni: (ni-buses.index(ni))%ni, n))

golden_time = crt(n, b)[0] 
print(f"Golden time is {golden_time}")
