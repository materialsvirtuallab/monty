from __future__ import annotations

import bz2
import gzip
import os
from pathlib import Path

import pytest
from monty.io import (
    FileLock,
    FileLockException,
    _get_line_ending,
    reverse_readfile,
    reverse_readline,
    zopen,
)
from monty.tempfile import ScratchDir

TEST_DIR = os.path.join(os.path.dirname(__file__), "test_files")


class TestGetLineEnding:
    @pytest.mark.parametrize("l_end", ["\n", "\r\n", "\r"])
    def test_get_line_ending(self, l_end):
        """Test files with:
        Unix line ending (\n)
        Windows line ending (\r\n)
        Classic MacOS line ending (\r)
        """
        with ScratchDir("."):
            test_file = "test_l_end.txt"
            test_line = f"This is a test{l_end}Second line{l_end}".encode()
            with open(test_file, "wb") as f:
                f.write(test_line)

            assert _get_line_ending(test_file) == l_end
            assert _get_line_ending(Path(test_file)) == l_end

            with open(test_file, "r", encoding="utf-8") as f:
                assert _get_line_ending(f) == l_end

            # Test gzip file
            with gzip.open(f"{test_file}.gz", "wb") as f:
                f.write(test_line)

            with gzip.open(f"{test_file}.gz", "rb") as f:
                assert _get_line_ending(f) == l_end

            # Test bzip2 file
            with bz2.open(f"{test_file}.bz2", "wb") as f:
                f.write(test_line)

            with bz2.open(f"{test_file}.bz2", "rb") as f:
                assert _get_line_ending(f) == l_end

    def test_unknown_file_type(self):
        unknown_file = 123

        with pytest.raises(TypeError, match="Unknown file type int"):
            _get_line_ending(unknown_file)

    def test_empty_file(self):
        with ScratchDir("."):
            test_file = "empty_file.txt"
            open(test_file, "w").close()

            with pytest.warns(match="File empty, use default line ending \n"):
                assert _get_line_ending(test_file) == "\n"

    def test_unknown_line_ending(self):
        with ScratchDir("."):
            test_file = "test_unknown.txt"
            with open(test_file, "wb") as f:
                f.write(b"This is a test\036")

            with pytest.raises(ValueError, match="Unknown line ending"):
                _get_line_ending(test_file)


class TestReverseReadline:
    NUMLINES = 3000

    def test_reverse_readline(self):
        """
        We are making sure a file containing line numbers is read in reverse
        order, i.e. the first line that is read corresponds to the last line.
        number
        """
        with open(os.path.join(TEST_DIR, "3000_lines.txt"), encoding="utf-8") as f:
            for idx, line in enumerate(reverse_readline(f)):
                assert (
                    int(line) == self.NUMLINES - idx
                ), f"read_backwards read {line} whereas it should have read {self.NUMLINES - idx}"

    def test_reverse_readline_fake_big(self):
        """
        Make sure that large text files are read properly.
        """
        with open(os.path.join(TEST_DIR, "3000_lines.txt"), encoding="utf-8") as f:
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
        assert lines[-1].strip() == b"HelloWorld."

    def test_empty_file(self):
        """
        Make sure an empty file does not throw an error when reverse_readline
        is called, which was a problem with an earlier implementation.
        """
        with pytest.warns(match="File empty, use default line ending \n."):
            with open(os.path.join(TEST_DIR, "empty_file.txt"), encoding="utf-8") as f:
                for _line in reverse_readline(f):
                    raise ValueError("an empty file is being read!")

    @pytest.mark.parametrize("l_end", ["\n", "\r", "\r\n"])
    def test_line_ending(self, l_end):
        contents = ("Line1", "Line2", "Line3")

        with ScratchDir("."):
            with open("test_file.txt", "wb") as file:
                file.write((l_end.join(contents) + l_end).encode())

            with open("test_file.txt", "r", encoding="utf-8") as file:
                for idx, line in enumerate(reverse_readline(file)):
                    assert line.strip() == contents[len(contents) - idx - 1]


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
        with pytest.warns(match="File empty, use default line ending \n."):
            for _line in reverse_readfile(os.path.join(TEST_DIR, "empty_file.txt")):
                raise ValueError("an empty file is being read!")

    @pytest.mark.parametrize("l_end", ["\n", "\r", "\r\n"])
    def test_line_ending(self, l_end):
        contents = ("Line1", "Line2", "Line3")

        with ScratchDir("."):
            with open("test_file.txt", "wb") as file:
                file.write((l_end.join(contents) + l_end).encode())

            with open("test_file.txt", "r", encoding="utf-8") as file:
                for idx, line in enumerate(reverse_readline(file)):
                    assert line.strip() == contents[len(contents) - idx - 1]


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
