# Common
with open("2024/02/input.txt", "r") as f:
    reports = [tuple(int(r) for r in l.strip().split(" ")) for l in f]

def is_report_safe(report: tuple[int, ...], allowed_errors = 0):
    direction = 0
    is_safe = True
    for i in range(1, len(report)):
        gap = report[i] - report[i-1]
        if gap * direction < 0 or abs(gap) < 1 or abs(gap) > 3:
            is_safe = False
            break
        
        direction = gap
    
    if not is_safe and allowed_errors > 0:    
        is_safe = any(
            is_report_safe(
                report[:i] + report[i+1:], 
                allowed_errors - 1,
            ) for i in range(len(report))
        )
            
    return is_safe

def sign(x: int) -> int:
    return (x > 0) - (x < 0)

def derive_report(report: tuple[int, ...]):
    return tuple(report[i] - report[i-1] for i in range(1, len(report)))

def is_report_derivative_safe(derivative: tuple[int, ...], min_slope: int = 1, max_slope: int = 3) -> tuple[bool, int | None]:
    direction = sign(derivative[0])
    for i, d in enumerate(derivative):
        if sign(d) != direction or abs(d) < min_slope or abs(d) > max_slope:
            return False, i

    return True, None

# Part 1
safe_reports_1 = [r for r in reports if is_report_safe(r, allowed_errors=0)]
print("Part 1: Number of safe report lines: ", len(safe_reports_1))


# Part 1
safe_reports_2 = [r for r in reports if is_report_safe(r, allowed_errors=1)]
print("Part 2: Number of safe report lines: ", len(safe_reports_2))
