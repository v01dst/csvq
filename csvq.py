#!/usr/bin/env python3
import argparse
import csv
import json
import sys
import os

def read_csv(path):
    if path == "-":
        f = sys.stdin
    else:
        f = open(path, newline="")
    reader = csv.DictReader(f)
    rows = list(reader)
    fieldnames = reader.fieldnames or []
    if path != "-":
        f.close()
    return fieldnames, rows

def cmd_query(args):
    fields, rows = read_csv(args.file)
    # filter
    if args.where:
        key, val = args.where.split("=", 1)
        rows = [r for r in rows if r.get(key) == val]
    # select columns
    if args.select:
        cols = args.select.split(",")
        rows = [{c: r.get(c) for c in cols} for r in rows]
        fields = cols
    # limit
    if args.limit:
        rows = rows[:args.limit]
    if args.json:
        print(json.dumps(rows, indent=2))
    else:
        writer = csv.DictWriter(sys.stdout, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

def cmd_count(args):
    fields, rows = read_csv(args.file)
    if args.where:
        key, val = args.where.split("=", 1)
        rows = [r for r in rows if r.get(key) == val]
    print(len(rows))

def cmd_headers(args):
    fields, _ = read_csv(args.file)
    for f in fields:
        print(f)

def cmd_pretty(args):
    fields, rows = read_csv(args.file)
    if args.where:
        key, val = args.where.split("=", 1)
        rows = [r for r in rows if r.get(key) == val]
    if args.limit:
        rows = rows[:args.limit]
    widths = {f: max(len(f), max((len(str(r.get(f, ""))) for r in rows), default=0)) for f in fields}
    header = " | ".join(f.ljust(widths[f]) for f in fields)
    sep = "-+-".join("-" * widths[f] for f in fields)
    print(header)
    print(sep)
    for r in rows:
        print(" | ".join(str(r.get(f, "")).ljust(widths[f]) for f in fields))

def main():
    parser = argparse.ArgumentParser(prog="csvq", description="Query and transform CSV from your terminal. Zero dependencies.")
    sub = parser.add_subparsers(dest="command")

    p_q = sub.add_parser("query", help="query/filter CSV")
    p_q.add_argument("file", help="CSV file or - for stdin")
    p_q.add_argument("--where", default=None, help="filter rows (key=value)")
    p_q.add_argument("--select", default=None, help="select columns (comma-separated)")
    p_q.add_argument("--limit", type=int, default=None, help="limit rows")
    p_q.add_argument("--json", action="store_true", help="JSON output")
    p_q.set_defaults(func=cmd_query)

    p_c = sub.add_parser("count", help="count rows")
    p_c.add_argument("file", help="CSV file or - for stdin")
    p_c.add_argument("--where", default=None, help="filter rows (key=value)")
    p_c.set_defaults(func=cmd_count)

    p_h = sub.add_parser("headers", help="list column headers")
    p_h.add_argument("file", help="CSV file or - for stdin")
    p_h.set_defaults(func=cmd_headers)

    p_p = sub.add_parser("pretty", help="pretty-print as table")
    p_p.add_argument("file", help="CSV file or - for stdin")
    p_p.add_argument("--where", default=None, help="filter rows (key=value)")
    p_p.add_argument("--limit", type=int, default=None, help="limit rows")
    p_p.set_defaults(func=cmd_pretty)

    args = parser.parse_args()
    if not args.command:
        if len(sys.argv) > 1 and not sys.argv[1].startswith("-"):
            args.command = "query"
            args.file = sys.argv[1]
            args.where = None
            args.select = None
            args.limit = None
            args.json = False
            cmd_query(args)
            return
        parser.print_help()
        sys.exit(1)
    args.func(args)

if __name__ == "__main__":
    main()
