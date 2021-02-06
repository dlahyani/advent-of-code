from dataclasses import dataclass
from enum import Enum
from typing import Callable, List, Optional

#####################################
## Models


@dataclass
class ExecutionContext:
    ip: int = 0
    acc: int = 0


class Operation(Enum):
    NOP = "nop"
    JMP = "jmp"
    ACC = "acc"


@dataclass
class Instruction:
    operation: Operation
    operand: int

    @property
    def instruction_pointer_effect(self) -> int:
        return self.operand if self.operation == Operation.JMP else 1

    @property
    def accumulator_effect(self) -> int:
        return self.operand if self.operation == Operation.ACC else 0

    @staticmethod
    def from_str(instruction: str) -> 'Instruction':
        operation, operand = instruction.split()
        return Instruction(operation=Operation(operation), operand=int(operand))


class Program:
    def __init__(self, program: List[Instruction]):
        self.instructions = {i: program[i] for i in range(len(program))}

        self._instruction_termination_value = [-1] * len(self.instructions)
        for i in self.instructions:
            self._fill_termination_value_for_instruction(i)

    def _fill_termination_value_for_instruction(self, instruction_index: int):
        if self._instruction_termination_value[instruction_index] != -1:
            return
        
        next_instruction_index = self.next_instruction_index(instruction_index)
        if next_instruction_index >= len(self.instructions):
            self._instruction_termination_value[instruction_index] = 1
            return
        
        self._instruction_termination_value[instruction_index] = 0
        self._fill_termination_value_for_instruction(next_instruction_index)
        self._instruction_termination_value[instruction_index] = (
            2 if self._instruction_termination_value[next_instruction_index] > 0 else 0
        )

    def next_instruction_index(self, instruction_index: int):
        return (instruction_index + self.instructions[instruction_index].instruction_pointer_effect)
    
    def is_instruction_on_terminating_path(self, instruction_index: int):
        return self._instruction_termination_value[instruction_index] > 0


#########################################
## Logic

def execute_instruction(instruction: Instruction, context: ExecutionContext) -> ExecutionContext:
    return ExecutionContext(
        ip=context.ip + instruction.instruction_pointer_effect, 
        acc=context.acc + instruction.accumulator_effect
    )

# A TrapGate is a function that if provided will be invoked by `execute_program` before the
# execution of every instruction. This gives the trap  opportunity to trace and affect the execution
# flow of the program. If the trap gate returns `None` the execution of the instruction is performed
# normally and execution of the program continues. If the trap gate returns an `ExecutionContext`
# then the instruction will not be executed and instead the execution will continue based on the
# returned execution context (i.e. the next instruction to be executed is the instruction pointed by
# the `ip` of the returned context and the returned context will be used as the
# execution context). Finally if the trap gate raises a `StopIteration` exception the program halts
# and the current context is returned. 
TrapGate = Callable[[Instruction, ExecutionContext], Optional[ExecutionContext]]

def execute_program(
    program: Program,
    initial_context: ExecutionContext,
    trap_gate: Optional[TrapGate] = None
) -> ExecutionContext:
    """
    Executes a program (a sequence of instructions) one by one, starting from the address pointed by
    `initial_context.ip` and updating the execution context based on the executed
    instruction (i.e. creating a new execution context after every instruction which holds the CPU
    state to be used on the  execution of the next instruction). In addition a `TrapGate` can be
    provided to track and affect the execution flow, see `TrapGate` documentation.
    The execution halts in 2 scenarios:
    1. The trap gate raises a `StopIteration` exception.
    2. The execution reaches an instruction which is beyond `program` memory bounds.

    Returns an `ExecutionContext` holding the CPU state after the execution of the last instruction.
    """
    def _trap_or_execute_instruction(instruction, context, trap_gate):
        return ((trap_gate and trap_gate(instruction, context)) or
            execute_instruction(instruction, context))

    context  = initial_context
    while True:
        instruction = program.instructions[context.ip]
        try:
            context = _trap_or_execute_instruction(instruction, context, trap_gate)
        except StopIteration:
            break
        
        if  context.ip >= len(program.instructions):
                break
        
    return context

def get_tracing_trap(trace: List[int]) -> TrapGate:
    def _trap(_: Instruction, context: ExecutionContext):
        trace.append(context.ip)

    return _trap

def get_loop_breaking_trap(trace: Optional[List[int]] = None) -> TrapGate:
    visited_offsets = set()
    tracer = get_tracing_trap(trace) if trace is not None else (lambda i, c: None)

    def _trap(instruction: Instruction, context: ExecutionContext):
        if context.ip in visited_offsets:
            raise StopIteration(f"Instruction @ {context.ip} was already executed")
        
        visited_offsets.add(context.ip)
        tracer(instruction, context)
    
    return _trap

def get_instruction_patching_trap(graph: Program) -> TrapGate:
    patched = False
    visited = set()

    def _trap(instruction: Instruction, context: ExecutionContext) -> ExecutionContext:
        nonlocal patched

        if context.ip in visited:
            raise StopIteration()

        visited.add(context.ip)
        patched_instruction = get_patched_instruction(instruction)
        if patched or not patched_instruction:
            return None

        if not graph.is_instruction_on_terminating_path(
            context.ip + patched_instruction.instruction_pointer_effect):
            return None
        
        patched = True
        return execute_instruction(patched_instruction, context)
    
    return _trap

def get_patched_instruction(instruction: Instruction) -> Instruction:
    if instruction.operation == Operation.ACC:
        return None
    
    return Instruction(
        Operation.JMP if instruction.operation == Operation.NOP else Operation.NOP, 
        instruction.operand
    )


if __name__ == "__main__":
    program = Program(
        [Instruction.from_str(line) for line in open("2020/08/input.txt", "r").readlines()]
    )
    
    # Part 1
    context = execute_program(program, ExecutionContext(), get_loop_breaking_trap())
    print(f"Loop identified at address {context.ip}, Accumulator={context.acc}")

    # Part 2
    context = execute_program(program, ExecutionContext(), get_instruction_patching_trap(program))
    print(f"Program finished successfully at address {context.ip}, Accumulator={context.acc}")
