#!/usr/bin/env python3
"""
Convert MySQL dump to SQLite-compatible SQL - Line by line approach
"""

import re
import sys

def convert_mysql_to_sqlite(input_file, output_file):
    """Convert MySQL dump to SQLite format, line by line."""

    output_lines = []
    output_lines.append("-- SQLite database converted from MySQL dump")
    output_lines.append("-- Original: virtuallab.sql")
    output_lines.append("")
    output_lines.append("PRAGMA foreign_keys = OFF;")
    output_lines.append("PRAGMA encoding = 'UTF-8';")
    output_lines.append("")

    with open(input_file, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    # Skip lines patterns
    skip_patterns = [
        r'^/\*!',           # MySQL version comments
        r'^LOCK TABLES',
        r'^UNLOCK TABLES',
        r'^SET ',
        r'^CREATE DATABASE',
        r'^USE `',
        r'^\s*$',           # Empty lines
    ]

    # Process line by line but handle multi-line statements
    lines = content.split('\n')
    i = 0
    in_create_table = False
    create_table_buffer = []

    while i < len(lines):
        line = lines[i]

        # Skip unwanted lines
        skip = False
        for pattern in skip_patterns:
            if re.match(pattern, line):
                skip = True
                break

        if skip:
            i += 1
            continue

        # Handle CREATE TABLE (multi-line)
        if 'CREATE TABLE' in line:
            in_create_table = True
            create_table_buffer = [line]
            i += 1
            continue

        if in_create_table:
            create_table_buffer.append(line)
            if line.strip().endswith(';'):
                # End of CREATE TABLE
                in_create_table = False
                table_sql = '\n'.join(create_table_buffer)
                converted = convert_create_table(table_sql)
                output_lines.append(converted)
                output_lines.append("")
                create_table_buffer = []
            i += 1
            continue

        # Handle DROP TABLE
        if line.startswith('DROP TABLE'):
            line = line.replace('`', '')
            output_lines.append(line)
            i += 1
            continue

        # Handle INSERT statements
        if line.startswith('INSERT INTO'):
            line = line.replace('`', '')
            line = line.replace("\\'", "''")
            output_lines.append(line)
            i += 1
            continue

        # Handle comments
        if line.startswith('--'):
            output_lines.append(line)
            i += 1
            continue

        # Skip standalone semicolons and junk
        if line.strip() == ';' or line.strip() == '':
            i += 1
            continue

        i += 1

    output_lines.append("")
    output_lines.append("PRAGMA foreign_keys = ON;")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))

    print(f"Conversion complete: {output_file}")


def convert_create_table(table_sql):
    """Convert a CREATE TABLE statement from MySQL to SQLite."""

    # Remove backticks
    table_sql = table_sql.replace('`', '')

    # Remove ENGINE, CHARSET, etc at the end
    table_sql = re.sub(r'\)\s*ENGINE=.*?;', ');', table_sql, flags=re.DOTALL | re.IGNORECASE)

    # Convert integer types
    table_sql = re.sub(r'\bint\(\d+\)', 'INTEGER', table_sql, flags=re.IGNORECASE)
    table_sql = re.sub(r'\bmediumint\(\d+\)', 'INTEGER', table_sql, flags=re.IGNORECASE)
    table_sql = re.sub(r'\bsmallint\(\d+\)', 'INTEGER', table_sql, flags=re.IGNORECASE)
    table_sql = re.sub(r'\btinyint\(\d+\)', 'INTEGER', table_sql, flags=re.IGNORECASE)
    table_sql = re.sub(r'\bbigint\(\d+\)', 'INTEGER', table_sql, flags=re.IGNORECASE)

    # Remove UNSIGNED
    table_sql = re.sub(r'\bunsigned\b', '', table_sql, flags=re.IGNORECASE)

    # Convert string types to TEXT
    table_sql = re.sub(r'\bvarchar\(\d+\)', 'TEXT', table_sql, flags=re.IGNORECASE)
    table_sql = re.sub(r'\bchar\(\d+\)', 'TEXT', table_sql, flags=re.IGNORECASE)
    table_sql = re.sub(r'\bmediumtext\b', 'TEXT', table_sql, flags=re.IGNORECASE)
    table_sql = re.sub(r'\blongtext\b', 'TEXT', table_sql, flags=re.IGNORECASE)
    table_sql = re.sub(r'\btinytext\b', 'TEXT', table_sql, flags=re.IGNORECASE)

    # Convert blob types
    table_sql = re.sub(r'\bmediumblob\b', 'BLOB', table_sql, flags=re.IGNORECASE)
    table_sql = re.sub(r'\blongblob\b', 'BLOB', table_sql, flags=re.IGNORECASE)
    table_sql = re.sub(r'\btinyblob\b', 'BLOB', table_sql, flags=re.IGNORECASE)

    # Convert datetime/timestamp to TEXT
    table_sql = re.sub(r'\bdatetime\b', 'TEXT', table_sql, flags=re.IGNORECASE)
    table_sql = re.sub(r'\btimestamp\b', 'TEXT', table_sql, flags=re.IGNORECASE)

    # Keep DATE as is (SQLite supports it)

    # Convert numeric types
    table_sql = re.sub(r'\bdouble\(\d+,\d+\)', 'REAL', table_sql, flags=re.IGNORECASE)
    table_sql = re.sub(r'\bdouble\b', 'REAL', table_sql, flags=re.IGNORECASE)
    table_sql = re.sub(r'\bfloat\(\d+,\d+\)', 'REAL', table_sql, flags=re.IGNORECASE)
    table_sql = re.sub(r'\bfloat\b', 'REAL', table_sql, flags=re.IGNORECASE)
    table_sql = re.sub(r'\bdecimal\(\d+,\d+\)', 'REAL', table_sql, flags=re.IGNORECASE)

    # Remove CHARACTER SET and COLLATE
    table_sql = re.sub(r'CHARACTER SET \w+', '', table_sql, flags=re.IGNORECASE)
    table_sql = re.sub(r'COLLATE \w+', '', table_sql, flags=re.IGNORECASE)

    # Remove AUTO_INCREMENT
    table_sql = re.sub(r'\bAUTO_INCREMENT\b', '', table_sql, flags=re.IGNORECASE)

    # Remove KEY definitions (indexes)
    table_sql = re.sub(r',\s*KEY\s+\w+\s*\([^)]+\)', '', table_sql)
    table_sql = re.sub(r',\s*UNIQUE KEY\s+\w+\s*\([^)]+\)', '', table_sql)
    table_sql = re.sub(r',\s*FULLTEXT KEY\s+\w+\s*\([^)]+\)', '', table_sql)

    # Convert current_timestamp()
    table_sql = re.sub(r'current_timestamp\(\)', "CURRENT_TIMESTAMP", table_sql, flags=re.IGNORECASE)

    # Clean up extra spaces
    table_sql = re.sub(r'  +', ' ', table_sql)

    # Fix trailing comma before closing paren
    table_sql = re.sub(r',\s*\)', ')', table_sql)

    return table_sql


if __name__ == '__main__':
    input_file = '/opt/inventarium/sql/virtuallab.sql'
    output_file = '/opt/inventarium/sql/virtuallab_sqlite.sql'
    convert_mysql_to_sqlite(input_file, output_file)
