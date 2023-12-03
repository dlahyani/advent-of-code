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
    def from_str(instruction: str) -> "Instruction":
        operation, operand = instruction.split()
        return Instruction(operation=Operation(operation), operand=int(operand))


#########################################
## Logic


def execute_instruction(instruction: Instruction, context: ExecutionContext) -> ExecutionContext:
    return ExecutionContext(
        ip=context.ip + instruction.instruction_pointer_effect,
        acc=context.acc + instruction.accumulator_effect,
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
    program: List[Instruction],
    initial_context: ExecutionContext,
    trap_gate: Optional[TrapGate] = None,
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
        return (trap_gate and trap_gate(instruction, context)) or execute_instruction(instruction, context)

    context = initial_context
    while True:
        instruction = program[context.ip]
        try:
            context = _trap_or_execute_instruction(instruction, context, trap_gate)
        except StopIteration:
            break

        if context.ip >= len(program):
            break

    return context


def get_tracing_trap(trace: List[int]) -> TrapGate:
    def _trap(_: Instruction, context: ExecutionContext):
        trace.append(context.ip)

    return _trap


def get_loop_breaking_trap(trace: Optional[List[int]] = None) -> TrapGate:
    trace = trace if trace is not None else []
    tracer = get_tracing_trap(trace)

    def _trap(instruction: Instruction, context: ExecutionContext):
        if context.ip in trace:
            raise StopIteration(f"Instruction @ {context.ip} was already executed")

        tracer(instruction, context)

    return _trap


def get_instruction_patching_trap(target_address: int) -> TrapGate:
    loop_break_trap = get_loop_breaking_trap()

    def _trap(instruction: Instruction, context: ExecutionContext):
        if context.ip == target_address:
            modified_instruction = get_patched_instruction(instruction)
            loop_break_trap(modified_instruction, context)
            return execute_instruction(modified_instruction, context)

        return loop_break_trap(instruction, context)

    return _trap


def patch_loop_and_execute_program(program: List[Instruction], loop_offsets: List[int]) -> Optional[ExecutionContext]:
    potentially_loop_breaking_patches = [o for o in loop_offsets if may_patch_break_loop(program, o, loop_offsets)]

    initial_context = ExecutionContext(loop_offsets[0], 0)
    for offset in potentially_loop_breaking_patches:
        trap = get_instruction_patching_trap(offset)
        exit_context = execute_program(program, initial_context, trap)
        if exit_context.ip >= len(program):
            return exit_context


def may_patch_break_loop(program: List[Instruction], offset: int, loop_offsets: List[int]):
    patched_instruction = get_patched_instruction(program[offset])
    return get_next_instruction_offset(patched_instruction, offset) not in loop_offsets


def get_next_instruction_offset(instruction: Instruction, offset: int):
    return offset + instruction.instruction_pointer_effect


def get_patched_instruction(instruction: Instruction) -> Instruction:
    if instruction.operation == Operation.ACC:
        return instruction

    return Instruction(
        Operation.JMP if instruction.operation == Operation.NOP else Operation.NOP,
        instruction.operand,
    )


######################################
## Solution

if __name__ == "__main__":
    program = [Instruction.from_str(line) for line in open("2020/08/input.txt", "r").readlines()]

    # Part 1
    loop_offsets = []
    loop_break_trap = get_loop_breaking_trap(loop_offsets)
    context = execute_program(program, ExecutionContext(), trap_gate=loop_break_trap)
    print(f"Loop identified at address {context.ip}, Accumulator={context.acc}")

    # Part  2
    context = patch_loop_and_execute_program(program, loop_offsets)
    print(f"Program finished successfully at address {context.ip}, Accumulator={context.acc}")
