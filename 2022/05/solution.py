from functools import reduce
from typing import Callable, Optional
import parse

Instruction = tuple[int, int, int]
CraneProgram = list[Instruction]
CrateStack = list[Optional[str]]
CrateStacks = list[CrateStack]
InstructionExecutor = Callable[[CrateStacks, Instruction], CrateStacks]

INSTRUCTION_FORMAT = parse.compile("move {:d} from {:d} to {:d}")

def parse_input(raw_input: str) -> tuple[CrateStacks, CraneProgram]:
    stacks, instructions = raw_input.split("\n\n")
    stack_levels = [[l[i+1] if len(l[i:i+3].strip()) > 0 else None for i in range(0, len(l), 4)] for l in stacks.split("\n")[-2::-1]]
    stacks = [list(filter(lambda c: c is not None, s)) for s in zip(*stack_levels)]
    instructions = [tuple(INSTRUCTION_FORMAT.parse(i.strip()).fixed) for i in instructions.split("\n")]
    return stacks, instructions

def execute_crane_program(path: str, executor: InstructionExecutor) -> tuple[CrateStacks, str]:
    stacks, instructions = parse_input(open(path).read())
    reduce(executor, instructions, stacks)
    return stacks, "".join([s[-1] for s in stacks])

    
### Part 1
def execute_crane_instruction_fofi(stacks: CrateStacks, instruction: Instruction) -> CrateStacks:
    count, src, dst = instruction
    stacks[dst-1].extend(stacks[src-1][-1:-count-1:-1])
    stacks[src-1] = stacks[src-1][:-count]
    return stacks
    
stacks, tops = execute_crane_program("2022/05/input.txt", execute_crane_instruction_fofi)
print("Crates at the top of the stacks: ", tops)

### Part 2
def execute_crane_instruction_foli(stacks: CrateStacks, instruction: Instruction) -> CrateStacks:
    count, src, dst = instruction
    stacks[src-1], crates_to_move = stacks[src-1][:-count], stacks[src-1][-count:]
    stacks[dst-1].extend(crates_to_move)
    return stacks

stacks, tops = execute_crane_program("2022/05/input.txt", execute_crane_instruction_foli)
print("Crates at the top of the stacks: ", tops)
