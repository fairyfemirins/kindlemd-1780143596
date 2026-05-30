#!/usr/bin/env python3
"""
KindleMD: Convert Kindle 'My Clippings.txt' to a searchable Markdown notebook.

Usage:
  kindlemd.py <input_file> <output_file.md> [--json]

Options:
  --json  Output as JSON instead of Markdown.
"""

import re
import json
import click
from pathlib import Path
from collections import defaultdict


def parse_clippings(input_path: str) -> list:
    """Parse Kindle 'My Clippings.txt' into a list of entries."""
    with open(input_path, 'r', encoding='utf-8-sig') as f:
        content = f.read()
    
    entries = []
    for entry in content.split('=========='):
        entry = entry.strip()
        if not entry:
            continue
        
        lines = entry.split('\n')
        if len(lines) < 4:
            continue
        
        title_author = lines[0].strip()
        metadata = lines[1].strip()
        content = '\n'.join(lines[3:]).strip()
        
        # Parse title and author (multi-language)
        title_match = re.match(r'^(.*?)(?: \(|（)(.*?)(?:\)|）)?$', title_author)
        title = title_match.group(1).strip() if title_match else title_author
        author = title_match.group(2).strip() if title_match and title_match.group(2) else "Unknown"
        
        # Parse location and date (multi-language)
        location_match = re.search(r'(?:Location|位置|Page) (\d+-\d+|\d+)', metadata)
        location = location_match.group(1) if location_match else "Unknown"
        
        date_match = re.search(r'Added on (.+)', metadata)
        date = date_match.group(1) if date_match else "Unknown"
        
        entries.append({
            'title': title,
            'author': author,
            'location': location,
            'date': date,
            'content': content
        })
    
    return entries


def group_by_book(entries: list) -> dict:
    """Group entries by book title."""
    books = defaultdict(list)
    for entry in entries:
        books[(entry['title'], entry['author'])].append(entry)
    return books


def export_markdown(books: dict, output_path: str) -> None:
    """Export grouped entries to Markdown."""
    with open(output_path, 'w', encoding='utf-8') as f:
        for (title, author), entries in books.items():
            f.write(f"# {title}\n")
            f.write(f"**Author**: {author}\n\n")
            
            # Sort by location (ascending)
            entries_sorted = sorted(entries, key=lambda x: int(x['location'].split('-')[0]) if '-' in x['location'] else int(x['location']))
            
            for entry in entries_sorted:
                f.write(f"- **Location {entry['location']}** (Added on {entry['date']})\n")
                f.write(f"  {entry['content']}\n\n")


def export_json(books: dict, output_path: str) -> None:
    """Export grouped entries to JSON."""
    data = []
    for (title, author), entries in books.items():
        data.append({
            'title': title,
            'author': author,
            'entries': entries
        })
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


@click.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.argument('output_file', type=click.Path())
@click.option('--json', is_flag=True, help='Output as JSON instead of Markdown.')
def main(input_file: str, output_file: str, json: bool) -> None:
    """Convert Kindle clippings to Markdown or JSON."""
    entries = parse_clippings(input_file)
    books = group_by_book(entries)
    
    if json:
        export_json(books, output_file)
    else:
        export_markdown(books, output_file)
    
    click.echo(f"Successfully exported to {output_file}")


if __name__ == '__main__':
    main()