"""Utility script for monty reverse reader speed benchmark.

Test matrix:
- Different Python versions.
- File of various sizes.
- Find the last line, 75 % line and 50 % line, and compare with reading from forwards.
"""

from __future__ import annotations

import os
import platform
import subprocess
import time

from monty.io import reverse_readline

# Test config
FILE_SIZES_MB = (1, 10, 100, 500, 1000, 5000)
PYTHON_VERS = ("3.12",)

# Env config
CONDA_PATH = "/opt/anaconda3"
PR_URL = "git+https://github.com/DanielYang59/monty.git@readline-line-ending"

ENV_NAME = "monty_benchmark_env"


def prepare_conda_env(python_version, from_url=False):
    """Create conda environment, install monty, and get Python version."""
    subprocess.run(
        [
            f"{CONDA_PATH}/bin/conda",
            "create",
            "-y",
            "-n",
            ENV_NAME,
            f"python={python_version}",
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    print(f"Conda environment {ENV_NAME} created with Python {python_version}.")

    # Install monty
    install_cmd = PR_URL if from_url else "monty"
    subprocess.run(
        [f"{CONDA_PATH}/envs/{ENV_NAME}/bin/pip", "install", install_cmd],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    print(f"monty installed {'from URL' if from_url else 'from PyPI'}.")

    # Get Python version
    result = subprocess.run(
        [f"{CONDA_PATH}/envs/{ENV_NAME}/bin/python", "--version"],
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def create_test_file(file_path, target_size_mb):
    """Creates a text file with lines until the target size is reached."""
    target_size = target_size_mb * 1024 * 1024  # Convert MB to bytes
    line_number = 1

    with open(file_path, "w") as f:
        while os.path.getsize(file_path) < target_size:
            f.write(f"This is line number {line_number}\n")
            line_number += 1

    total_lines = line_number - 1
    print(f"Test file of size {target_size_mb} MB created with {total_lines} lines.")
    return total_lines


def test_readline(file_path, total_lines, readline_func, func_name="readline"):
    """General function to test reading lines using a given readline function."""

    # Read the last line
    start = time.perf_counter()
    with open(file_path, "r") as f:
        _last_line = (
            next(readline_func(f))
            if func_name == "reverse_readline"
            else f.readlines()[-1]
        )
    last_time = time.perf_counter() - start

    # Calculate the 75% and 50% line numbers
    line_75_idx = int(0.75 * total_lines)
    line_50_idx = int(0.5 * total_lines)

    # Read the 75% line
    start = time.perf_counter()  # More accurate timer
    with open(file_path, "r") as f:
        if func_name == "reverse_readline":
            for idx, _line in enumerate(readline_func(f), 1):
                if idx == total_lines - line_75_idx:
                    break
        else:
            _line = f.readlines()[line_75_idx]
    time_75 = time.perf_counter() - start

    # Read the 50% line
    start = time.perf_counter()  # More accurate timer
    with open(file_path, "r") as f:
        if func_name == "reverse_readline":
            for idx, _line in enumerate(readline_func(f), 1):
                if idx == total_lines - line_50_idx:
                    break
        else:
            _line = f.readlines()[line_50_idx]
    time_50 = time.perf_counter() - start

    print(
        f"{func_name.capitalize()} - Last line {total_lines} read, time taken: {last_time:.8f} s."
    )
    print(
        f"{func_name.capitalize()} - 75% line {line_75_idx} read, time taken: {time_75:.8f} s."
    )
    print(
        f"{func_name.capitalize()} - 50% line {line_50_idx} read, time taken: {time_50:.8f} s."
    )

    return last_time, time_75, time_50


def run_benchmark(file_size_mb, python_version):
    """Run benchmark for both monty and built-in readline."""
    print(
        f"\nRunning benchmark for Python {python_version} and file size {file_size_mb} MB."
    )

    test_file = f"test_file_{file_size_mb}MB.txt"
    total_lines = create_test_file(test_file, file_size_mb)

    print(f"\nTesting reverse_readline with file size {file_size_mb} MB...")
    test_readline(test_file, total_lines, reverse_readline, "reverse_readline")

    print(f"\nTesting built-in readline with file size {file_size_mb} MB...")
    test_readline(test_file, total_lines, iter, "readline")

    os.remove(test_file)


if __name__ == "__main__":
    # Show OS info
    os_info = platform.platform()
    print(f"\nRunning on OS: {os_info}")

    for python_version in PYTHON_VERS:
        for from_url in (False, True):
            try:
                source_type = "from URL" if from_url else "from PyPI"
                print(
                    f"\n--- Test started for Python {python_version} ({source_type}) ---"
                )

                # Prepare the environment (create conda env and install monty)
                installed_python_version = prepare_conda_env(
                    python_version, from_url=from_url
                )

                for file_size_mb in FILE_SIZES_MB:
                    # Run benchmark
                    run_benchmark(file_size_mb, installed_python_version)

            finally:
                subprocess.run(
                    [
                        f"{CONDA_PATH}/bin/conda",
                        "remove",
                        "-y",
                        "--name",
                        ENV_NAME,
                        "--all",
                    ],
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                print(f"Conda environment {ENV_NAME} removed.")
