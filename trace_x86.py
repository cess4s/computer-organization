"""Trace this project's non-PIE Linux x86-64 ELF in WSL using objdump and ptrace."""

import argparse
import csv
import ctypes
import json
import os
import re
import signal
import subprocess

FIELDS = ("sira", "RW", "adres_hex", "boyut", "c_satiri", "stack_mi")
REGISTERS = ("r15", "r14", "r13", "r12", "rbp", "rbx", "r11", "r10", "r9",
             "r8", "rax", "rcx", "rdx", "rsi", "rdi", "orig_rax", "rip", "cs",
             "eflags", "rsp", "ss", "fs_base", "gs_base", "ds", "es", "fs", "gs")
MASK64 = (1 << 64) - 1
MEMORY = re.compile(r"(BYTE|WORD|DWORD|QWORD) PTR (\[[^]]+\]|fs:0x[0-9a-f]+)")
SIZES = {"BYTE": 1, "WORD": 2, "DWORD": 4, "QWORD": 8}


def command(*args):
    return subprocess.check_output(args, text=True)


def disassemble(binary):
    instructions = {}
    for name in ("main", "rotl"):
        output = command("objdump", "-d", "-Mintel", "--insn-width=16",
                         f"--disassemble={name}", binary)
        for line in output.splitlines():
            columns = line.split("\t")
            if len(columns) < 3 or not columns[0].strip().endswith(":"):
                continue
            address = int(columns[0].strip()[:-1], 16)
            size = len(columns[1].split())
            instructions[address] = (name, size, columns[2].split("#", 1)[0].strip())
    addresses = [hex(address) for address in instructions]
    lines = command("addr2line", "-e", binary, *addresses).splitlines()
    return {address: (*insn, int(re.search(r":(\d+)", line)[1]))
            for (address, insn), line in zip(instructions.items(), lines, strict=True)}


def memory_operands(text, regs, next_pc):
    opcode, _, operands = text.partition(" ")
    if re.search(r"\bnop\b", text):
        return
    if opcode in ("call", "push"):
        yield "W", regs["rsp"] - 8, 8, True
    if opcode in ("pop", "ret", "leave"):
        yield "R", regs["rbp" if opcode == "leave" else "rsp"], 8, True
    for index, operand in enumerate(operands.split(",")):
        match = MEMORY.search(operand)
        if match is None:
            if ("[" in operand and opcode not in ("lea", "nop")) or "fs:" in operand:
                raise ValueError(f"Unrecognized memory operand: {text}")
            continue
        size_name, expr = match.groups()
        if expr.startswith("fs:"):
            address = regs["fs_base"] + int(expr[3:], 16)
        else:
            values = dict(regs, rip=next_pc)
            address = 0
            for term in re.findall(r"[+-]?[^+-]+", expr[1:-1]):
                sign = -1 if term.startswith("-") else 1
                name, _, scale = term.lstrip("+-").partition("*")
                value = values[name] if name in values else int(name, 0)
                address += sign * value * (int(scale) if scale else 1)
        stack = bool(re.search(r"\br(?:bp|sp)\b", expr))
        if opcode == "mov":
            modes = "W" if index == 0 else "R"
        elif opcode in ("cmp", "test") or index != 0:
            modes = "R"
        elif opcode in ("add", "sub", "xor", "and", "or", "inc", "dec"):
            modes = "RW"
        else:
            raise ValueError(f"Unmodeled instruction: {text}")
        for mode in modes:
            yield mode, address & MASK64, SIZES[size_name], stack


def trace_run(binary, instructions, symbols, stack_residue, profile=False):
    libc = ctypes.CDLL(None, use_errno=True)
    ptrace = libc.ptrace
    ptrace.restype = ctypes.c_long
    ptrace.argtypes = [ctypes.c_uint, ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p]
    pid = os.fork()

    def ptr(request, address=0, data=0):
        ctypes.set_errno(0)
        result = ptrace(request, pid, address, data)
        error = ctypes.get_errno()
        if error:
            raise OSError(error, os.strerror(error))
        return result

    def wait_trap():
        _, status = os.waitpid(pid, 0)
        if not os.WIFSTOPPED(status) or os.WSTOPSIG(status) != signal.SIGTRAP:
            raise RuntimeError(f"Expected ptrace stop, got {status:#x}")

    if pid == 0:
        ptr(0)
        os.execv(binary, [binary])

    raw = (ctypes.c_ulonglong * len(REGISTERS))()
    reaped = False

    def get_registers():
        ptr(12, 0, ctypes.addressof(raw))
        return dict(zip(REGISTERS, raw))

    rows, kernel_rows, executed = [], [], []
    try:
        wait_trap()
        start = symbols["main"]
        original = ptr(1, start)
        ptr(4, start, (original & ~0xff) | 0xcc)
        ptr(7)
        wait_trap()
        regs = get_registers()
        assert regs["rip"] == start + 1
        # main pushes the caller's RBP before establishing its own frame.
        main_rbp = regs["rsp"] - 8
        if stack_residue is not None and main_rbp % 128 != stack_residue:
            return None
        raw[REGISTERS.index("rip")] = start
        ptr(4, start, original)
        ptr(13, 0, ctypes.addressof(raw))
        dynamic = 0
        while True:
            regs = get_registers()
            pc = regs["rip"]
            name, length, asm, line = instructions[pc]
            dynamic += 1
            ref_ids = []
            accesses = list(memory_operands(asm, regs, pc + length))
            events = []
            for mode, address, width, stack in accesses:
                rows.append((len(rows) + 1, mode, hex(address), width, line, int(stack)))
                ref_ids.append(len(rows))
                if profile and mode == "R":
                    value = ptr(2, address) & ((1 << (8 * width)) - 1)
                    events.append([mode, address, width, value])
            if pc == 0x4012C9 and "cmp" in asm and not kernel_rows:
                kernel_rows.append((pc, ref_ids, dynamic))
            elif kernel_rows and len(kernel_rows) < 18:
                kernel_rows.append((pc, ref_ids, dynamic))
            final = name == "main" and asm == "ret"
            ptr(9)
            wait_trap()
            if profile:
                for mode, address, width, _ in accesses:
                    if mode == "W":
                        value = ptr(2, address) & ((1 << (8 * width)) - 1)
                        events.append([mode, address, width, value])
                executed.append({"pc": pc, "asm": asm, "line": line, "accesses": events})
            if final:
                break
        outputs = {name: ptr(2, symbols[name]) & 0xffffffff
                   for name in ("checksum", "decrypt_ok")}
        ptr(7)
        _, status = os.waitpid(pid, 0)
        reaped = os.WIFEXITED(status) or os.WIFSIGNALED(status)
        if not os.WIFEXITED(status) or os.WEXITSTATUS(status):
            raise RuntimeError(f"Program did not return successfully: {status:#x}")
        print(f"main_rbp={main_rbp:#x} TLS={regs['fs_base']:#x} Ic={dynamic} "
              f"v={symbols['v']:#x} checksum={outputs['checksum']:#010x} "
              f"decrypt_ok={outputs['decrypt_ok']}")
        if kernel_rows and kernel_rows[-1][0] == 0x4013E1:
            for pc, ids, _ in kernel_rows:
                print(f"{pc:#x} refs={','.join(map(str, ids)) or '-'}")
        report = {"instructions": executed, "outputs": outputs, "symbols": symbols}
        return rows, report
    finally:
        if not reaped:
            try:
                os.kill(pid, signal.SIGKILL)
                os.waitpid(pid, 0)
            except ProcessLookupError:
                pass


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("elf")
    parser.add_argument("csv")
    parser.add_argument("--stack-residue", type=int, choices=range(0, 128, 16))
    parser.add_argument("--profile", help="Temporary JSON with executed instructions and data values")
    args = parser.parse_args()
    binary = os.path.abspath(args.elf)
    instructions = disassemble(binary)
    names = {"main", "v", "checksum", "decrypt_ok"}
    symbols = {name: int(address, 16) for address, _, name in
               (line.split() for line in command("nm", "--defined-only", binary).splitlines()
                if len(line.split()) == 3) if name in names}
    for _ in range(128):
        result = trace_run(binary, instructions, symbols, args.stack_residue, bool(args.profile))
        if result is not None:
            rows, report = result
            with open(args.csv, "w", encoding="utf-8", newline="") as output:
                writer = csv.writer(output)
                writer.writerow(FIELDS)
                writer.writerows(rows)
            if args.profile:
                with open(args.profile, "w", encoding="utf-8") as output:
                    json.dump(report, output)
            return
    raise RuntimeError("No run matched the requested stack alignment")


if __name__ == "__main__":
    main()
