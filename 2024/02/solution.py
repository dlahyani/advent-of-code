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


# Part 1
safe_reports_1 = [r for r in reports if is_report_safe(r)]
print("Part 1: Number of safe report lines: ", len(safe_reports_1))


# Part 1
safe_reports_2 = [r for r in reports if is_report_safe(r, allowed_errors=1)]
print("Part 2: Number of safe report lines: ", len(safe_reports_2))
