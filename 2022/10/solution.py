from typing import Iterable


instructions = [l.strip() for l in open("2022/10/input.txt")]

def sample_cycle_if_needed(c, X, samples):
    if c == 20 or (c-20) % 40 == 0:
        samples[c] = X

def crt_draw(c, X, CRT):
    row, col = (c-1)//40, (c-1) % 40
    if col in [X-1, X, X+1]:
        CRT[row][col] = "#"
    

def execute_instructions(instructions: Iterable[str], samples, CRT):
    X = 1
    V = None
    ip = 0
    
    c = 1
    while ip < len(instructions):
        sample_cycle_if_needed(c, X, samples)
        crt_draw(c, X, CRT)
        
        if instructions[ip] == "noop":
            ip += 1
        else:
            if V is not None:
                X += V
                V = None
                ip += 1
            else: 
                V = int(instructions[ip].split()[1])        
        c += 1


samples = {}
CRT = [list("." * 40) for _ in range(6)]
execute_instructions(instructions, samples, CRT)

### Part 1
print("Sum of signal strengths: ", sum(map(lambda sample: sample[0]*sample[1], samples.items())))

### Part 2
print("\n".join(["".join(row) for row in CRT]))