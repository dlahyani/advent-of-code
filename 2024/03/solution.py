from gc import disable
import re

from tenacity import DoSleep

# Common
with open("2024/03/input.txt", "r") as f:
    data = "".join(f.readlines())


# Part 1
mul_pattern = re.compile("(mul\((\d{1,3}),(\d{1,3})\))")
s = sum(int(f1) * int(f2) for _, f1, f2 in mul_pattern.findall(data))
print("Sum of all mul instructions is: ", s)

# Part 2
enable_marker = "do()"
disable_marker = "don't()"
mul_pattern = re.compile("mul\((\d{1,3}),(\d{1,3})\)")

s = 0 
i = 0
while i < len(data):
    if data[i:i+len(disable_marker)] == disable_marker:
        next_enable_marker_index = data.find(enable_marker, i + len(disable_marker))
        if next_enable_marker_index == -1:
            break
        i = next_enable_marker_index + len(enable_marker)
        continue
    
    if not data[i:i+4] == "mul(":
        i += 1
        continue
        
    m = mul_pattern.match(data, pos=i, endpos=i+12)
    if m is not None:
        s += int(m.group(1)) * int(m.group(2))
        i = m.end()
        continue
    else:
        i += 4
        
print("Sum of all enabled mul instructions is: ", s)