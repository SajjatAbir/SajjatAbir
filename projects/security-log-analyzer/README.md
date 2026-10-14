# Security log analyzer

A small, dependency-free Python CLI for practicing defensive log analysis. It reads an offline OpenSSH log and reports source addresses with repeated failed passwords as JSON.

## Run

Requires Python 3.10 or newer. From this directory:

```bash
python3 analyzer.py sample.log --threshold 3
python3 -m unittest discover -v
```

The synthetic sample uses reserved documentation addresses. It produces five lines read, four failed passwords, one ignored line, and one alert for `192.0.2.10` with three failures. To analyze your own authorized log export, pass its path instead of `sample.log`.

## Detection logic

1. Match OpenSSH `Failed password for ... from ADDRESS port NUMBER` messages, including invalid users.
2. Validate and normalize IPv4 and IPv6 source addresses.
3. Count failures per address over the entire file.
4. Return addresses whose count meets or exceeds the chosen positive threshold.

An empty alert list means no address met this rule. Exit code 0 means analysis completed, including when alerts exist; exit code 2 indicates an input or command error.

## Limits

This is an educational starter project, not a production intrusion detector. It has no time window, deduplication, live collection, or correlation with successful logins. Shared addresses, mistyped passwords, and duplicated logs can produce false positives; distributed attempts or other authentication formats can be missed. Ignored lines include unrelated events and invalid addresses. Do not infer that an address is malicious from this report alone.

Only synthetic data is included. Keep real logs, account names, and sensitive investigation details out of public commits.

## Possible next steps

- Add a timestamp-aware sliding window with boundary tests.
- Support additional authentication formats using sanitized fixtures.
- Add CSV output and investigation guidance.
