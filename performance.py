"""Compute the assignment's -O0/-O1 performance model from WSL execution profiles."""

import argparse
from collections import Counter, OrderedDict
import json
from pathlib import Path

from cache_sim import ADDRESS_MASK, load_trace, simulate, stats

CPI = {"ALU": 1, "Çarpma": 3, "Load": 1, "Store": 1, "Branch / jump": 2}
FREQ_GHZ = 1.9
MEMORY_CYCLES = 25
CORES = 3


def instruction_class(instruction):
    opcode = instruction["asm"].split()[0]
    if opcode in ("call", "ret") or opcode.startswith("j"):
        return "Branch / jump"
    if opcode in ("imul", "mul"):
        return "Çarpma"
    modes = {event[0] for event in instruction["accesses"]}
    if "W" in modes:
        return "Store"
    if "R" in modes:
        return "Load"
    return "ALU"


def counts(instructions):
    classes = Counter(map(instruction_class, instructions))
    refs = sum(len(insn["accesses"]) for insn in instructions)
    cycles = sum(CPI[name] * number for name, number in classes.items())
    return classes, refs, cycles


def profile_stats(profile, trace):
    instructions = profile["instructions"]
    classes, refs, cycles = counts(instructions)
    assert refs == len(trace)
    cache_results, _, _ = simulate(trace)
    summary = stats(cache_results, trace)
    ic = len(instructions)
    cpi = cycles / ic
    return {
        "classes": {name: classes[name] for name in CPI},
        "Ic": ic,
        "data_references": refs,
        "core_cycles": cycles,
        "CPI": cpi,
        "m": refs / ic,
        "MIPS": FREQ_GHZ * 1000 / cpi,
        "no_memory_ns": cycles / FREQ_GHZ,
        "uncached_ns": (cycles + refs * MEMORY_CYCLES) / FREQ_GHZ,
        "cached_ns": (cycles + refs * summary["Ts"]) / FREQ_GHZ,
        "cache": summary,
        "outputs": profile["outputs"],
    }


def replay_cache(profile, capacity, line_size, ways):
    """Check read values and architectural output with a write-through data cache."""
    memory = {}
    sets = [OrderedDict() for _ in range(capacity // (line_size * ways))]
    hits = misses = 0
    for insn in profile["instructions"]:
        for mode, address, width, value in insn["accesses"]:
            data = value.to_bytes(width, "little")
            blocks = {}
            for offset in range(width):
                byte_address = address + offset
                block = (byte_address & ADDRESS_MASK) // line_size
                blocks.setdefault(block, []).append((byte_address, data[offset]))
            for block, byte_values in blocks.items():
                lines = sets[block % len(sets)]
                if block in lines:
                    hits += 1
                    lines.move_to_end(block)
                else:
                    misses += 1
                    if len(lines) == ways:
                        lines.popitem(last=False)
                    lines[block] = {}
                cached_bytes = lines[block]
                for byte_address, byte in byte_values:
                    if mode == "W":
                        memory[byte_address] = byte
                        cached_bytes[byte_address] = byte
                    else:
                        from_memory = memory.setdefault(byte_address, byte)
                        from_cache = cached_bytes.setdefault(byte_address, from_memory)
                        assert from_memory == from_cache == byte, (insn["pc"], byte_address)
    outputs = {}
    for name, expected in profile["outputs"].items():
        address = profile["symbols"][name]
        value = int.from_bytes(bytes(memory[address + offset] for offset in range(4)), "little")
        assert value == expected
        outputs[name] = value
    return {"hits": hits, "misses": misses, "outputs": outputs}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("profile_o0")
    parser.add_argument("trace_o0")
    parser.add_argument("profile_o1")
    parser.add_argument("trace_o1")
    parser.add_argument("--output", default="performance_summary.json")
    args = parser.parse_args()
    original = json.loads(Path(args.profile_o0).read_text(encoding="utf-8"))
    optimized = json.loads(Path(args.profile_o1).read_text(encoding="utf-8"))
    trace_o0 = load_trace(args.trace_o0)
    trace_o1 = load_trace(args.trace_o1)
    opt0 = profile_stats(original, trace_o0)
    opt1 = profile_stats(optimized, trace_o1)
    assert opt0["outputs"] == opt1["outputs"]
    assert opt0["Ic"] == 3513 and opt0["data_references"] == 1777
    archive = json.loads(Path("cache_summary.json").read_text(encoding="utf-8"))
    assert opt0["cache"] == archive["base"]

    # Include complete loop control for the two independent XOR loops in -O0.
    independent = [insn for insn in original["instructions"]
                   if (0x401223 <= insn["pc"] <= 0x401275
                       or 0x4012DE <= insn["pc"] <= 0x401330)]
    _, parallel_refs, parallel_cycles = counts(independent)
    parallel_time = (parallel_cycles + parallel_refs * opt0["cache"]["Ts"]) / FREQ_GHZ
    fraction = parallel_time / opt0["cached_ns"]
    audited = {}
    for line, ways in [(16, 1), (16, 2), (16, 4), (16, 8), (8, 4), (32, 4)]:
        key = f"{line}B/{ways}-way"
        result = replay_cache(original, 128, line, ways)
        expected, _, _ = simulate(trace_o0, line_bytes=line, ways=ways)
        summary = stats(expected, trace_o0)
        assert (result["hits"], result["misses"]) == (summary["hits"], summary["misses"])
        audited[key] = dict(result, Ts=summary["Ts"])

    result = {
        "model": {"GHz": FREQ_GHZ, "tau_ns": 1 / FREQ_GHZ,
                  "cores": CORES, "memory_cycles": MEMORY_CYCLES},
        "O0": opt0,
        "O1": opt1,
        "optimization_speedup": opt0["cached_ns"] / opt1["cached_ns"],
        "cache_speedup_O0": opt0["uncached_ns"] / opt0["cached_ns"],
        "amdahl": {"instructions": len(independent), "core_cycles": parallel_cycles,
                   "references": parallel_refs, "time_ns": parallel_time,
                   "fraction": fraction,
                   "speedup": 1 / (1 - fraction + fraction / CORES),
                   "limit": 1 / (1 - fraction)},
        "cache_value_replay": audited,
    }
    Path(args.output).write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n",
                                 encoding="utf-8")


if __name__ == "__main__":
    main()
