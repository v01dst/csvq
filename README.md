# csvq

Query and transform CSV from your terminal. Zero dependencies, pure Python stdlib.

## Install

```bash
pip install csvq
```

Or run directly:

```bash
python csvq.py --help
```

## Usage

```bash
# Pretty print
csvq pretty data.csv

# Filter rows
csvq query data.csv --where city=nyc

# Select columns
csvq query data.csv --select name,age

# Count rows
csvq count data.csv

# List headers
csvq headers data.csv

# JSON output
csvq query data.csv --json
```

## License

MIT