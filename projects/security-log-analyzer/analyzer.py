"""Summarize failed OpenSSH passwords in offline logs. Python 3.10+, no dependencies."""
import argparse
from collections import Counter
import ipaddress
import json
from pathlib import Path
import re

FAILED = re.compile(r"\bFailed password for (?:invalid user )?\S+ from (\S+) port \d+\b")


def analyze(lines, threshold=3):
    """Flag addresses at or above the failure threshold across the entire input."""
    if threshold < 1:
        raise ValueError("threshold must be at least 1")
    failures = Counter()
    total = 0
    ignored = 0
    for line in lines:
        total += 1
        match = FAILED.search(line)
        if match:
            try:
                address = str(ipaddress.ip_address(match.group(1)))
            except ValueError:
                ignored += 1
                continue
            failures[address] += 1
        else:
            ignored += 1
    return {
        "lines_read": total,
        "ignored_lines": ignored,
        "failed_passwords": sum(failures.values()),
        "threshold": threshold,
        "alerts": [
            {"source_ip": address, "failed_passwords": count}
            for address, count in sorted(failures.items())
            if count >= threshold
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("log", type=Path, help="UTF-8 OpenSSH log file")
    parser.add_argument("--threshold", type=int, default=3)
    args = parser.parse_args()
    try:
        with args.log.open(encoding="utf-8") as stream:
            report = analyze(stream, args.threshold)
    except (OSError, UnicodeError, ValueError) as error:
        parser.exit(2, f"Error: {error}\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
