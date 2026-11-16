"""Simulate the project's write-through, write-allocate data cache with LRU."""

import argparse
from collections import Counter, OrderedDict
import csv
import json
from pathlib import Path

ADDRESS_MASK = (1 << 32) - 1


def load_trace(path):
    with open(path, encoding="utf-8", newline="") as source:
        return [
            dict(row, sira=int(row["sira"]), address=int(row["adres_hex"], 16),
                 boyut=int(row["boyut"]), stack_mi=int(row["stack_mi"]))
            for row in csv.DictReader(source)
        ]


def simulate(trace, capacity=128, line_bytes=16, ways=4, snapshot_at=30):
    if line_bytes < 1 or ways < 1 or capacity % (line_bytes * ways):
        raise ValueError("The cache must contain an integer number of sets")
    set_count = capacity // (line_bytes * ways)
    sets = [OrderedDict() for _ in range(set_count)]
    seen = set()
    results = []
    snapshot = []
    evictions = Counter()

    def cache_state():
        lines = []
        for set_index, entries in enumerate(sets):
            by_way = {way: (block // set_count, rank)
                      for rank, (block, way) in enumerate(entries.items(), 1)}
            for way in range(ways):
                tag, rank = by_way.get(way, (None, None))
                lines.append({"line": set_index * ways + way, "set": set_index,
                              "valid": int(way in by_way), "tag": tag, "lru": rank})
        return lines

    for ref in trace:
        addr = ref["address"] & ADDRESS_MASK
        first = addr // line_bytes
        last = (addr + ref["boyut"] - 1) // line_bytes
        for block in range(first, last + 1):
            set_index = block % set_count
            entries = sets[set_index]
            hit = block in entries
            victim = None
            if hit:
                entries.move_to_end(block)
            else:
                if len(entries) == ways:
                    victim, way = entries.popitem(last=False)
                    evictions[(victim * line_bytes, block * line_bytes)] += 1
                else:
                    used = set(entries.values())
                    way = next(slot for slot in range(ways) if slot not in used)
                entries[block] = way
            results.append({
                "sira": ref["sira"], "RW": ref["RW"], "adres_hex": ref["adres_hex"],
                "adres32": f"0x{addr:08x}", "tag": hex(block // set_count),
                "set": set_index, "word": addr % line_bytes if block == first else 0,
                "sonuc": "Hit" if hit else "Miss",
                "cikan_blok": hex(victim * line_bytes) if victim is not None else "",
                "once_geldi": int(block in seen),
            })
            seen.add(block)
        if ref["sira"] == snapshot_at:
            snapshot = cache_state()
    return results, snapshot, evictions


def stats(results, trace):
    hits = sum(row["sonuc"] == "Hit" for row in results)
    references = len(results)
    h = hits / references
    return {"refs": references, "hits": hits, "misses": references - hits,
            "H": h, "writes": sum(ref["RW"] == "W" for ref in trace),
            "Ts": 1 + (1 - h) * 25}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("trace", type=Path)
    parser.add_argument("trace_v2", type=Path)
    args = parser.parse_args()
    trace = load_trace(args.trace)
    trace_v2 = load_trace(args.trace_v2)
    base, snapshot, _ = simulate(trace)
    updated, _, _ = simulate(trace_v2)
    # Independent first-30 hand calculation for the archived trace.
    expected_misses = [1, 2, 3, 4, 6, 13]
    observed_misses = [row["sira"] for row in base[:30] if row["sonuc"] == "Miss"]
    expected_lines = {
        (0, 0x6ece93b, 1), (0, 0x32b204c, 2), (0, 0x20202, 3),
        (1, 0x32b204c, 1), (1, 0x32b2047, 2), (1, 0x32b2046, 3),
    }
    observed_lines = {(row["set"], row["tag"], row["lru"])
                      for row in snapshot if row["valid"]}
    if trace[0]["adres_hex"] == "0x7ffe65640990":
        assert observed_misses == expected_misses
        assert observed_lines == expected_lines, observed_lines
        assert stats(base[:30], trace[:30])["writes"] == 13

    mapping = {}
    direct_evictions = None
    for name, ways in [("Direct", 1), ("2-way", 2), ("4-way", 4), ("Fully associative", 8)]:
        values, _, evictions = simulate(trace, ways=ways)
        mapping[name] = stats(values, trace)
        if ways == 1:
            direct_evictions = evictions
    sizes = {}
    for size in (8, 16, 32, 64):
        if 128 % (size * 4):
            sizes[size] = None
        else:
            values, _, _ = simulate(trace, line_bytes=size)
            sizes[size] = stats(values, trace)
    summary = {
        "base": stats(base, trace), "v2": stats(updated, trace_v2),
        "first30": stats(base[:30], trace[:30]), "snapshot": snapshot,
        "mapping": mapping, "line_sizes": sizes,
        "direct_top_evictions": direct_evictions.most_common(6),
        "trace_counts": {
            "reads": sum(ref["RW"] == "R" for ref in trace),
            "stores": sum(ref["RW"] == "W" for ref in trace),
            "stack": sum(ref["stack_mi"] for ref in trace),
            "array": sum(0x404040 <= ref["address"] < 0x4040c4 for ref in trace),
        },
    }
    with open("cache_results.csv", "w", encoding="utf-8", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=list(base[0]))
        writer.writeheader()
        writer.writerows(base)
    Path("cache_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
