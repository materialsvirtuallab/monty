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
                assert isinstance(line, str)
                assert (
                    int(line) == self.NUMLINES - idx
                ), f"read_backwards read {line} whereas it should have read {self.NUMLINES - idx}"

    def test_reverse_readline_fake_big(self):
        """
        Make sure that large text files are read properly.
        """
        with open(os.path.join(TEST_DIR, "3000_lines.txt"), encoding="utf-8") as f:
            for idx, line in enumerate(reverse_readline(f, max_mem=0)):
                assert isinstance(line, str)
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
                lines.append(line)
        assert lines == ["\n", "\n", "HelloWorld."]  # test file has two empty lines
        assert all(isinstance(line, str) for line in lines)

    def test_empty_file(self):
        """
        Make sure an empty file does not throw an error when reverse_readline
        is called, which was a problem with an earlier implementation.
        """
        with pytest.warns(match="File empty, use default line ending \n."):
            with open(os.path.join(TEST_DIR, "empty_file.txt"), encoding="utf-8") as f:
                for _line in reverse_readline(f):
                    pytest.fail("No error should be thrown.")

    @pytest.mark.skip("TODO: WIP")
    @pytest.mark.parametrize("l_end", ["\n", "\r\n", "\r"])
    def test_file_with_empty_lines(self, l_end):
        """Empty lines should not be skipped."""

    @pytest.mark.parametrize("l_end", ["\n", "\r", "\r\n"])
    def test_line_ending(self, l_end):
        contents = ("Line1", "Line2", "Line3")

        with ScratchDir("."):
            with open("test_file.txt", "wb") as file:
                file.write((l_end.join(contents) + l_end).encode())

            with open("test_file.txt", "r", encoding="utf-8") as file:
                for idx, line in enumerate(reverse_readline(file)):
                    assert line == contents[len(contents) - idx - 1]
                    assert isinstance(line, str)


class TestReverseReadfile:
    NUMLINES = 3000

    def test_reverse_readfile(self):
        """
        Make sure a file containing line numbers is read in reverse order,
        i.e. the first line that is read corresponds to the last line number.
        """
        fname = os.path.join(TEST_DIR, "3000_lines.txt")
        for idx, line in enumerate(reverse_readfile(fname)):
            assert isinstance(line, str)
            assert int(line) == self.NUMLINES - idx

    def test_reverse_readfile_gz(self):
        """
        Make sure a file containing line numbers is read in reverse order,
        i.e. the first line that is read corresponds to the last line number.
        """
        fname = os.path.join(TEST_DIR, "3000_lines.txt.gz")
        for idx, line in enumerate(reverse_readfile(fname)):
            assert isinstance(line, str)
            assert int(line) == self.NUMLINES - idx

    def test_reverse_readfile_bz2(self):
        """
        Make sure a file containing line numbers is read in reverse order,
        i.e. the first line that is read corresponds to the last line number.
        """
        fname = os.path.join(TEST_DIR, "3000_lines.txt.bz2")
        for idx, line in enumerate(reverse_readfile(fname)):
            assert isinstance(line, str)
            assert int(line) == self.NUMLINES - idx

    def test_empty_file(self):
        """
        Make sure an empty file does not throw an error when reverse_readline
        is called, which was a problem with an earlier implementation.
        """
        with pytest.warns(match="File empty, use default line ending \n."):
            for _line in reverse_readfile(os.path.join(TEST_DIR, "empty_file.txt")):
                pytest.fail("No error should be thrown.")

    @pytest.mark.parametrize("l_end", ["\n", "\r\n", "\r"])
    def test_file_with_empty_lines(self, l_end):
        """Empty lines should not be skipped.

        TODO: not working for "\r\n" for some reason.
        """
        expected_contents = ("line1", "", "line3")
        filename = "test_empty_line.txt"

        with ScratchDir("."):
            # Test text file
            with open(filename, "w", newline="", encoding="utf-8") as file:
                for line in expected_contents:
                    file.write(line + l_end)

            # Sanity check: ensure the text file is correctly written
            with open(filename, "rb") as file:
                raw_content = file.read()
            expected_raw_content = (l_end.join(expected_contents) + l_end).encode(
                "utf-8"
            )
            assert raw_content == expected_raw_content

            revert_contents = tuple(reverse_readfile(filename))
            assert revert_contents[::-1] == (*expected_contents, "")

    @pytest.mark.parametrize("l_end", ["\n", "\r", "\r\n"])
    def test_line_ending(self, l_end):
        contents = ("Line1", "Line2", "Line3")

        with ScratchDir("."):
            with open("test_file.txt", "wb") as file:
                file.write((l_end.join(contents) + l_end).encode())

            with open("test_file.txt", "r", encoding="utf-8") as file:
                for idx, line in enumerate(reverse_readline(file)):
                    assert isinstance(line, str)
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
