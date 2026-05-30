# KindleMD

Convert Kindle `My Clippings.txt` into a searchable, tagged Markdown notebook with backlinks to the original book and location.

## Features
- **Multi-language support**: Parses `Location` (English), `位置` (Chinese), and `Page` (other languages).
- **Grouped output**: Highlights are grouped by book and sorted by location.
- **Markdown/JSON export**: Choose your preferred format.
- **Deduplication**: SQLite backend (optional, not enabled in this version).

## Installation
```bash
pip install click
```

## Usage
```bash
# Convert to Markdown
python3 kindlemd.py My\ Clippings.txt output.md

# Convert to JSON
python3 kindlemd.py My\ Clippings.txt output.json --json
```

## Example
**Input (`My Clippings.txt`)**:
```text
The Pragmatic Programmer (Andrew Hunt, David Thomas)
- Your Highlight on Location 123-124 | Added on Tuesday, May 26, 2026 10:00:00 AM

The most damaging phrase in the language is “We’ve always done it this way!”
==========
```

**Output (`output.md`)**:
```markdown
# The Pragmatic Programmer
**Author**: Andrew Hunt, David Thomas

- **Location 123-124** (Added on Tuesday, May 26, 2026 10:00:00 AM)
  The most damaging phrase in the language is “We’ve always done it this way!”
```

## Technical Architecture
- **Parser**: Regex-based, with fallbacks for multi-language metadata.
- **Exporter**: Markdown (default) or JSON.
- **CLI**: `click` for user interaction.

## Limitations
- No GUI (CLI-only).
- No cloud sync (local files only).

## License
MIT