from typing import Optional
import parse

Instruction = tuple[int, int, int]
CraneProgram = list[Instruction]
CrateStack = list[Optional[str]]
CrateStacks = list[CrateStack]

INSTRUCTION_FORMAT = parse.compile("move {:d} from {:d} to {:d}")

def parse_input(raw_input: str) -> tuple[CrateStacks, CraneProgram]:
    stacks, instructions = raw_input.split("\n\n")
    stack_levels = [[l[i+1] if len(l[i:i+3].strip()) > 0 else None for i in range(0, len(l), 4)] for l in stacks.split("\n")[-2::-1]]
    stacks = [list(filter(lambda c: c is not None, s)) for s in zip(*stack_levels)]
    instructions = [tuple(INSTRUCTION_FORMAT.parse(i.strip()).fixed) for i in instructions.split("\n")]
    return stacks, instructions

raw_input = open("2022/05/input.txt").read()
    
### Part 1
def execute_crane_instruction_fofi(count: int, src: int, dst: int, stacks: CrateStacks):
    stacks[src-1], crates_to_move = stacks[src-1][:-count], stacks[src-1][-1:-count-1:-1]
    stacks[dst-1].extend(crates_to_move)
    
stacks, instructions = parse_input(raw_input)
for count, src, dst in instructions:
    execute_crane_instruction_fofi(count, src, dst, stacks)
    
stack_tops = "".join([s[-1] for s in stacks])
print(stack_tops)

### Part 2
def execute_crane_instruction_foli(count: int, src: int, dst: int, stacks: CrateStacks):
    stacks[src-1], crates_to_move = stacks[src-1][:-count], stacks[src-1][-count:]
    stacks[dst-1].extend(crates_to_move)

stacks, instructions = parse_input(raw_input)
for count, src, dst in instructions:
    execute_crane_instruction_foli(count, src, dst, stacks)
stack_tops = "".join([s[-1] for s in stacks])
print(stack_tops)
