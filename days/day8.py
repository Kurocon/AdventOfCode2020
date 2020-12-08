from days import AOCDay, day

class Instr:
    instruction = None
    arg = None
    run_count = None

    def __init__(self, instr, arg, runcount):
        self.instruction = instr
        self.arg = arg
        self.run_count = runcount


@day(8)
class Day8(AOCDay):
    print_debug = ""
    test_input = """nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6""".split("\n")

    instructions = []

    def common(self, input_data):
        # input_data = self.test_input

        self.instructions = []

        for line in input_data:
            instr, arg = line.split(" ")
            arg = int(arg)
            assert instr in ["acc", "jmp", "nop"]
            self.instructions.append(Instr(instr, arg, 0))

    def run_instrs(self):
        pc = 0
        acc = 0
        while True:
            inc_pc = True
            try:
                i = self.instructions[pc]
            except IndexError:
                assert pc == len(self.instructions), "IndexError but not after last instruction?"
                return acc, True
            self.debug(f"pc:{pc}, acc:{acc}, instr:{i.instruction}, arg:{i.arg}, rc:{i.run_count}")
            if i.run_count != 0:
                return acc, False
            if i.instruction == "nop":
                pass
            elif i.instruction == "jmp":
                pc += i.arg
                inc_pc = False
            elif i.instruction == "acc":
                acc += i.arg
            else:
                self.error(f"Invalid instr {i.instruction}")
            self.debug(f"npc:{pc}, nacc:{acc} nrc:{i.run_count}")
            i.run_count += 1
            if inc_pc:
                pc += 1

    def part1(self, input_data):
        yield self.run_instrs()[0]

    def part2(self, input_data):
        for i, instr in enumerate(self.instructions):
            if instr.instruction == "acc":
                continue

            # Change instruction to other one
            orig_instr = (instr.instruction)
            instr.instruction = "nop" if instr.instruction == "jmp" else "jmp"

            # Run program
            acc, success = self.run_instrs()

            # Check output
            if success:
                yield acc
                break

            # Change instruction back
            instr.instruction = orig_instr

            # Reset runcounts
            for p in self.instructions:
                p.run_count = 0
