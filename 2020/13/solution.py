with open("2020/13/input.txt") as f:
    arrival_time = int(f.readline())
    buses = [int(b) for b in f.readline().split(",") if b != "x"]
    
print(f"Estimated arrival time to the bus station: {arrival_time}")

earliest_possible_departure_time = -1
bus_id = 0
cur_time = arrival_time
while earliest_possible_departure_time == -1:
    for b in buses:
        if cur_time % b == 0:
            earliest_possible_departure_time = cur_time
            bus_id = b
            break
    cur_time += 1

wait_time = earliest_possible_departure_time - arrival_time
score = wait_time * bus_id
print(f"Earliest possible departure at {earliest_possible_departure_time} (waiting for {wait_time} min.) on bus {bus_id}, score: {score}")
        