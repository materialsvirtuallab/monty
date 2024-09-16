"""Utility script for monty reverse reader speed benchmark.
- File of various sizes.
- Find the last line, 75 % line and 50 % line, and compare with reading from forwards.
"""

from __future__ import annotations

import os
import platform
import sys
import time

from monty.io import reverse_readfile, reverse_readline

# Test config
FILE_SIZES_MB = (1, 10, 100, 500, 1000, 5000)


def create_test_file(file_path, target_size_mb):
    """Creates a text file with lines until the target size is reached."""
    target_size = target_size_mb * 1024 * 1024  # Convert MB to bytes
    line_number = 1

    start = time.perf_counter()

    # Create a list of lines and concatenate them at the end
    lines = []
    total_bytes_written = 0

    while total_bytes_written < target_size:
        line = f"This is line number {line_number}\n"
        line_bytes = line.encode('utf-8')

        if total_bytes_written + len(line_bytes) > target_size:
            break

        lines.append(line)
        total_bytes_written += len(line_bytes)
        line_number += 1

    with open(file_path, "wb") as f:
        f.write("".join(lines).encode('utf-8'))

    last_time = time.perf_counter() - start

    total_lines = line_number - 1
    print(f"Test file of size {target_size_mb} MB created with {total_lines} lines, time used {last_time:.2f} seconds.")
    return total_lines


def print_separator(title: str):
    print(f"{title}".center(80, "="))
    print("")


def test_builtin_readline(file_path, total_lines):
    """Test built-in readline function."""
    start = time.perf_counter()
    with open(file_path, "r") as f:
        _last_line = f.readlines()[-1]
    last_time = time.perf_counter() - start

    line_75_idx = int(0.75 * total_lines)
    line_50_idx = int(0.5 * total_lines)

    start = time.perf_counter()
    with open(file_path, "r") as f:
        _line = f.readlines()[line_75_idx]
    time_75 = time.perf_counter() - start

    start = time.perf_counter()
    with open(file_path, "r") as f:
        _line = f.readlines()[line_50_idx]
    time_50 = time.perf_counter() - start

    print_separator("Built-in readline")
    print(f"Last line {total_lines} read, time taken: {last_time:.8f} s.")
    print(f"75% line {line_75_idx} read, time taken: {time_75:.8f} s.")
    print(f"50% line {line_50_idx} read, time taken: {time_50:.8f} s.")
    print_separator("End of Built-in readline")

    return last_time, time_75, time_50


def test_reverse_readline(file_path, total_lines):
    """Test reverse_readline function."""
    start = time.perf_counter()
    with open(file_path, "r") as f:
        _last_line = next(reverse_readline(f))
    last_time = time.perf_counter() - start

    line_75_idx = int(0.75 * total_lines)
    line_50_idx = int(0.5 * total_lines)

    start = time.perf_counter()
    with open(file_path, "r") as f:
        for idx, _line in enumerate(reverse_readline(f), 1):
            if idx == total_lines - line_75_idx:
                break
    time_75 = time.perf_counter() - start

    start = time.perf_counter()
    with open(file_path, "r") as f:
        for idx, _line in enumerate(reverse_readline(f), 1):
            if idx == total_lines - line_50_idx:
                break
    time_50 = time.perf_counter() - start

    print_separator("reverse_readline")
    print(f"Last line {total_lines} read, time taken: {last_time:.8f} s.")
    print(f"75% line {line_75_idx} read, time taken: {time_75:.8f} s.")
    print(f"50% line {line_50_idx} read, time taken: {time_50:.8f} s.")
    print_separator("End of reverse_readline")

    return last_time, time_75, time_50


def test_reverse_readfile(file_path, total_lines):
    """Test reverse_readfile function."""
    start = time.perf_counter()
    _last_line = next(reverse_readfile(file_path))
    last_time = time.perf_counter() - start

    line_75_idx = int(0.75 * total_lines)
    line_50_idx = int(0.5 * total_lines)

    start = time.perf_counter()
    for idx, _line in enumerate(reverse_readfile(file_path), 1):
        if idx == total_lines - line_75_idx:
            break
    time_75 = time.perf_counter() - start

    start = time.perf_counter()
    for idx, _line in enumerate(reverse_readfile(file_path), 1):
        if idx == total_lines - line_50_idx:
            break
    time_50 = time.perf_counter() - start

    print_separator("reverse_readfile")
    print(f"Last line {total_lines} read, time taken: {last_time:.8f} s.")
    print(f"75% line {line_75_idx} read, time taken: {time_75:.8f} s.")
    print(f"50% line {line_50_idx} read, time taken: {time_50:.8f} s.")
    print_separator("End of reverse_readfile")

    return last_time, time_75, time_50


def run_benchmark(file_size_mb):
    """Run benchmark for all test functions."""
    print_separator(f"Benchmarking file size: {file_size_mb} MB")

    test_file = f"test_file_{file_size_mb}MB.txt"
    total_lines = create_test_file(test_file, file_size_mb)

    test_builtin_readline(test_file, total_lines)
    test_reverse_readline(test_file, total_lines)
    test_reverse_readfile(test_file, total_lines)

    os.remove(test_file)


if __name__ == "__main__":
    # Show OS info
    os_info = platform.platform()
    python_version = sys.version.split()[0]
    print(f"\nRunning on OS: {os_info}, Python {python_version}")

    # Run benchmark for each file size
    for file_size_mb in FILE_SIZES_MB:
        run_benchmark(file_size_mb)
