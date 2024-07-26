from __future__ import annotations

import os
from pathlib import Path
from unittest.mock import patch

import pytest
from monty.io import (
    FileLock,
    FileLockException,
    reverse_readfile,
    reverse_readline,
    zopen,
)
from monty.tempfile import ScratchDir

TEST_DIR = os.path.join(os.path.dirname(__file__), "test_files")


class TestReverseReadline:
    NUMLINES = 3000

    def test_reverse_readline(self):
        """
        We are making sure a file containing line numbers is read in reverse
        order, i.e. the first line that is read corresponds to the last line.
        number
        """
        with open(os.path.join(TEST_DIR, "3000_lines.txt")) as f:
            for idx, line in enumerate(reverse_readline(f)):
                assert (
                    int(line) == self.NUMLINES - idx
                ), f"read_backwards read {line} whereas it should have read {self.NUMLINES - idx}"

    def test_reverse_readline_fake_big(self):
        """
        Make sure that large text files are read properly.
        """
        with open(os.path.join(TEST_DIR, "3000_lines.txt")) as f:
            for idx, line in enumerate(reverse_readline(f, max_mem=0)):
                assert (
                    int(line) == self.NUMLINES - idx
                ), f"read_backwards read {line} whereas it should have read {self.NUMLINES - idx}"

    def test_reverse_readline_bz2(self):
        """
        Make sure a file containing line numbers is read in reverse order,
        i.e. the first line that is read corresponds to the last line number.
        """
        lines = []
        with zopen(os.path.join(TEST_DIR, "myfile_bz2.bz2"), "rb") as f:
            for line in reverse_readline(f):
                lines.append(line.strip())
        assert lines[-1].strip(), ["HelloWorld." in b"HelloWorld."]

    def test_empty_file(self):
        """
        Make sure an empty file does not throw an error when reverse_readline
        is called, which was a problem with an earlier implementation.
        """
        with open(os.path.join(TEST_DIR, "empty_file.txt")) as f:
            for _line in reverse_readline(f):
                raise ValueError("an empty file is being read!")

    @pytest.fixture()
    def test_line_ending(self):
        contents = ("Line1", "Line2", "Line3")

        # Mock Linux/MacOS
        with patch("os.name", "posix"):
            linux_line_end = os.linesep
            assert linux_line_end == "\n"

            with ScratchDir("./test_files"):
                with open("sample_unix_mac.txt", "w", newline=linux_line_end) as file:
                    file.write(linux_line_end.join(contents))

                with open("sample_unix_mac.txt") as file:
                    for idx, line in enumerate(reverse_readfile(file)):
                        assert line == contents[len(contents) - idx - 1]

        # Mock Windows
        with patch("os.name", "nt"):
            windows_line_end = os.linesep
            assert windows_line_end == "\r\n"

            with ScratchDir("./test_files"):
                with open("sample_windows.txt", "w", newline=windows_line_end) as file:
                    file.write(windows_line_end.join(contents))

                with open("sample_windows.txt") as file:
                    for idx, line in enumerate(reverse_readfile(file)):
                        assert line == contents[len(contents) - idx - 1]


class TestReverseReadfile:
    NUMLINES = 3000

    def test_reverse_readfile(self):
        """
        Make sure a file containing line numbers is read in reverse order,
        i.e. the first line that is read corresponds to the last line number.
        """
        fname = os.path.join(TEST_DIR, "3000_lines.txt")
        for idx, line in enumerate(reverse_readfile(fname)):
            assert int(line) == self.NUMLINES - idx

    def test_reverse_readfile_gz(self):
        """
        Make sure a file containing line numbers is read in reverse order,
        i.e. the first line that is read corresponds to the last line number.
        """
        fname = os.path.join(TEST_DIR, "3000_lines.txt.gz")
        for idx, line in enumerate(reverse_readfile(fname)):
            assert int(line) == self.NUMLINES - idx

    def test_reverse_readfile_bz2(self):
        """
        Make sure a file containing line numbers is read in reverse order,
        i.e. the first line that is read corresponds to the last line number.
        """
        fname = os.path.join(TEST_DIR, "3000_lines.txt.bz2")
        for idx, line in enumerate(reverse_readfile(fname)):
            assert int(line) == self.NUMLINES - idx

    def test_empty_file(self):
        """
        Make sure an empty file does not throw an error when reverse_readline
        is called, which was a problem with an earlier implementation.
        """
        for _line in reverse_readfile(os.path.join(TEST_DIR, "empty_file.txt")):
            raise ValueError("an empty file is being read!")

    @pytest.fixture
    def test_line_ending(self):
        contents = ("Line1", "Line2", "Line3")

        # Mock Linux/MacOS
        with patch("os.name", "posix"):
            linux_line_end = os.linesep
            assert linux_line_end == "\n"

            with ScratchDir("./test_files"):
                with open("sample_unix_mac.txt", "w", newline=linux_line_end) as file:
                    file.write(linux_line_end.join(contents))

                for idx, line in enumerate(reverse_readfile("sample_unix_mac.txt")):
                    assert line == contents[len(contents) - idx - 1]

        # Mock Windows
        with patch("os.name", "nt"):
            windows_line_end = os.linesep
            assert windows_line_end == "\r\n"

            with ScratchDir("./test_files"):
                with open("sample_windows.txt", "w", newline=windows_line_end) as file:
                    file.write(windows_line_end.join(contents))

                for idx, line in enumerate(reverse_readfile("sample_windows.txt")):
                    assert line == contents[len(contents) - idx - 1]


class TestZopen:
    def test_zopen(self):
        with zopen(os.path.join(TEST_DIR, "myfile_gz.gz"), mode="rt") as f:
            assert f.read() == "HelloWorld.\n\n"
        with zopen(os.path.join(TEST_DIR, "myfile_bz2.bz2"), mode="rt") as f:
            assert f.read() == "HelloWorld.\n\n"
        with zopen(os.path.join(TEST_DIR, "myfile_bz2.bz2"), "rt") as f:
            assert f.read() == "HelloWorld.\n\n"
        with zopen(os.path.join(TEST_DIR, "myfile_xz.xz"), "rt") as f:
            assert f.read() == "HelloWorld.\n\n"
        with zopen(os.path.join(TEST_DIR, "myfile_lzma.lzma"), "rt") as f:
            assert f.read() == "HelloWorld.\n\n"
        with zopen(os.path.join(TEST_DIR, "myfile"), mode="rt") as f:
            assert f.read() == "HelloWorld.\n\n"

    def test_Path_objects(self):
        p = Path(TEST_DIR) / "myfile_gz.gz"

        with zopen(p, mode="rt") as f:
            assert f.read() == "HelloWorld.\n\n"


class TestFileLock:
    def setup_method(self):
        self.file_name = "__lock__"
        self.lock = FileLock(self.file_name, timeout=1)
        self.lock.acquire()

    def test_raise(self):
        with pytest.raises(FileLockException):
            new_lock = FileLock(self.file_name, timeout=1)
            new_lock.acquire()

    def teardown_method(self):
        self.lock.release()
