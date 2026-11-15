import unittest
import os
import sys
import io
import csv
import json
from contextlib import redirect_stdout
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from csvq import read_csv, cmd_count, cmd_headers, cmd_pretty


class TestReadCsv(unittest.TestCase):
    def test_basic(self):
        p = os.path.join(os.path.dirname(__file__), "t.csv")
        with open(p, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["name", "age"])
            w.writerow(["alice", "30"])
        fields, rows = read_csv(p)
        self.assertEqual(fields, ["name", "age"])
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["name"], "alice")
        os.unlink(p)


class TestCount(unittest.TestCase):
    def test_count(self):
        p = os.path.join(os.path.dirname(__file__), "t2.csv")
        with open(p, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["a", "b"])
            w.writerow(["1", "2"])
            w.writerow(["3", "4"])
        buf = io.StringIO()
        with redirect_stdout(buf):
            cmd_count(type("A", (), {"file": p, "where": None})())
        self.assertEqual(buf.getvalue().strip(), "2")
        os.unlink(p)


class TestHeaders(unittest.TestCase):
    def test_headers(self):
        p = os.path.join(os.path.dirname(__file__), "t3.csv")
        with open(p, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["name", "age", "city"])
        buf = io.StringIO()
        with redirect_stdout(buf):
            cmd_headers(type("A", (), {"file": p})())
        self.assertEqual(buf.getvalue().strip().splitlines(), ["name", "age", "city"])
        os.unlink(p)


if __name__ == "__main__":
    unittest.main()
