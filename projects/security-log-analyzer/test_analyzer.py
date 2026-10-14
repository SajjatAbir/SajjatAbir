import unittest
from analyzer import analyze


def failure(address):
    return f"Oct 15 09:00:01 lab sshd[1]: Failed password for invalid user admin from {address} port 12345 ssh2"


class AnalyzerTests(unittest.TestCase):
    def test_threshold_and_address_separation(self):
        report = analyze([failure("192.0.2.1")] * 3 + [failure("192.0.2.2")] * 2)
        self.assertEqual(report["failed_passwords"], 5)
        self.assertEqual(report["alerts"], [{"source_ip": "192.0.2.1", "failed_passwords": 3}])

    def test_ignores_success_and_invalid_address(self):
        report = analyze(["Accepted password for root from 192.0.2.1 port 12345", failure("invalid")])
        self.assertEqual(report["ignored_lines"], 2)
        self.assertEqual(report["alerts"], [])

    def test_ipv6_normalization(self):
        report = analyze([failure("2001:db8::1"), failure("2001:0db8::1")], 2)
        self.assertEqual(report["alerts"], [{"source_ip": "2001:db8::1", "failed_passwords": 2}])

    def test_empty_input(self):
        self.assertEqual(analyze([])["lines_read"], 0)

    def test_invalid_threshold(self):
        with self.assertRaises(ValueError):
            analyze([], 0)


if __name__ == "__main__":
    unittest.main()
