BOARDING_TRANS = str.maketrans({"F": "0", "B": "1", "L": "0", "R": "1"})

def boarding_pass_to_seat_id(boarding_pass: str) -> int:
    return int(boarding_pass.translate(BOARDING_TRANS), 2)

def find_hole_in_list(numbers: list) -> int:
    expected_sum = 0.5 * (len(numbers) + 1) * (min(numbers) + max(numbers))
    return int(expected_sum - sum(numbers))

if __name__ == "__main__":
    seat_ids = [boarding_pass_to_seat_id(l) for l in open("2020/05/input.txt", "r").readlines()]

    # Part 1
    print(f"Highest taken seat ID {max(seat_ids)}")

    # Part 2
    print(f"Your seat ID is: {find_hole_in_list(seat_ids)}")
