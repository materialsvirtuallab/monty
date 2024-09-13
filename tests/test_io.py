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
    @pytest.mark.parametrize("l_end", ["\n", "\r\n"])
    def test_get_line_ending(self, l_end):
        """Test files with:
        Unix line ending (\n).
        Windows line ending (\r\n).
        """
        test_file = "test_l_end.txt"
        test_line = f"This is a test{l_end}Second line{l_end}".encode()

        with ScratchDir("."):
            with open(test_file, "wb") as f:
                f.write(test_line)

            assert _get_line_ending(test_file) == l_end
            assert _get_line_ending(Path(test_file)) == l_end

            with open(test_file, "r", encoding="utf-8") as f:
                assert _get_line_ending(f) == l_end

            # Test gzip file
            gzip_filename = f"{test_file}.gz"
            with gzip.open(gzip_filename, "wb") as f:
                f.write(test_line)

            # Opened file
            with gzip.open(gzip_filename, "rb") as f:
                assert _get_line_ending(f) == l_end

            # Filename directly
            assert _get_line_ending(gzip_filename) == l_end

            # Test opened bzip2 file
            bz2_filename = f"{test_file}.bz2"
            with bz2.open(bz2_filename, "wb") as f:
                f.write(test_line)

            # Opened file
            with bz2.open(bz2_filename, "rb") as f:
                assert _get_line_ending(f) == l_end

            # Filename directly
            assert _get_line_ending(bz2_filename) == l_end

    def test_unknown_file_type(self):
        unknown_file = 123

        with pytest.raises(TypeError, match="Unknown file type int"):
            _get_line_ending(unknown_file)

    def test_empty_file(self):
        with ScratchDir("."):
            test_file = "empty_file.txt"
            open(test_file, "w").close()

            with pytest.warns(match="File is empty, return Unix line ending \n"):
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
                assert line == f"{str(self.NUMLINES - idx)}{os.linesep}"

    def test_reverse_readline_fake_big(self):
        """
        Make sure that large text files are read properly,
        by setting max_mem to 0.
        """
        with open(
            os.path.join(TEST_DIR, "3000_lines.txt"), mode="r", encoding="utf-8"
        ) as f:
            for idx, line in enumerate(reverse_readline(f, max_mem=0)):
                assert isinstance(line, str)
                assert line == f"{str(self.NUMLINES - idx)}{os.linesep}"

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
        with pytest.warns(match="File is empty, return Unix line ending \n."):
            with open(os.path.join(TEST_DIR, "empty_file.txt"), encoding="utf-8") as f:
                for _line in reverse_readline(f):
                    pytest.fail("No error should be thrown.")

    @pytest.mark.parametrize("l_end", ["\n", "\r\n"])
    def test_file_with_empty_lines(self, l_end):
        """Empty lines should not be skipped."""
        contents = (f"line1{l_end}", f"{l_end}", f"line3{l_end}")
        filename = "test_empty_line.txt"

        with ScratchDir("."):
            # Test text file
            with open(filename, "wb") as file:
                for line in contents:
                    file.write(line.encode())

            with open(filename, mode="r", newline="") as file:
                revert_contents = tuple(reverse_readline(file))
            assert revert_contents[::-1] == contents

            # # Test gzip file
            # gzip_filename = f"{filename}.gz"
            # with gzip.open(gzip_filename, "w") as file_out:
            #     for line in contents:
            #         file_out.write(line.encode())

            # revert_contents_gzip = tuple(reverse_readline(gzip_filename))
            # assert revert_contents_gzip[::-1] == contents

            # # Test bzip2 file
            # bz2_filename = f"{filename}.bz2"
            # with bz2.open(bz2_filename, "w") as file_out:
            #     for line in contents:
            #         file_out.write(line.encode())

            # revert_contents_bz2 = tuple(reverse_readline(bz2_filename))
            # assert revert_contents_bz2[::-1] == contents

    @pytest.mark.parametrize("l_end", ["\n", "\r\n"])
    def test_line_ending(self, l_end):
        contents = (f"Line1{l_end}", f"Line2{l_end}", f"Line3{l_end}")
        file_name = "test_file.txt"

        with ScratchDir("."):
            with open(file_name, "wb") as file:
                for line in contents:
                    file.write(line.encode())

            # Test text mode
            with open(file_name, "r", encoding="utf-8") as file:
                for idx, line in enumerate(reverse_readline(file)):
                    # Open text in "r" mode would trigger OS
                    # line ending handing
                    assert (
                        line.rstrip(os.linesep) + l_end
                        == contents[len(contents) - idx - 1]
                    )
                    assert isinstance(line, str)

            # # TODO: Test binary mode
            # with open(file_name, "rb") as file:
            #     for idx, line in enumerate(reverse_readline(file)):
            #         assert line == contents[len(contents) - idx - 1]
            #         assert isinstance(line, str)


class TestReverseReadfile:
    NUM_LINES = 3000

    def test_reverse_readfile(self):
        """
        Make sure a file containing line numbers is read in reverse order,
        i.e. the first line that is read corresponds to the last line number.
        """
        fname = os.path.join(TEST_DIR, "3000_lines.txt")
        for idx, line in enumerate(reverse_readfile(fname)):
            assert isinstance(line, str)
            # OS would automatically convert line ending in text mode
            assert line == f"{str(self.NUM_LINES - idx)}{os.linesep}"

    def test_reverse_readfile_gz(self):
        """
        Make sure a file containing line numbers is read in reverse order,
        i.e. the first line that is read corresponds to the last line number.
        """
        fname = os.path.join(TEST_DIR, "3000_lines.txt.gz")
        for idx, line in enumerate(reverse_readfile(fname)):
            assert isinstance(line, str)
            assert line == f"{str(self.NUM_LINES - idx)}\n"

    def test_reverse_readfile_bz2(self):
        """
        Make sure a file containing line numbers is read in reverse order,
        i.e. the first line that is read corresponds to the last line number.
        """
        fname = os.path.join(TEST_DIR, "3000_lines.txt.bz2")
        for idx, line in enumerate(reverse_readfile(fname)):
            assert isinstance(line, str)
            assert line == f"{str(self.NUM_LINES - idx)}\n"

    def test_empty_file(self):
        """
        Make sure an empty file does not throw an error when reverse_readline
        is called, which was a problem with an earlier implementation.
        """
        with pytest.warns(match="File is empty, return Unix line ending \n."):
            for _line in reverse_readfile(os.path.join(TEST_DIR, "empty_file.txt")):
                pytest.fail("No error should be thrown.")

    @pytest.mark.parametrize("l_end", ["\n", "\r\n"])
    def test_file_with_empty_lines(self, l_end):
        """Empty lines should not be skipped."""
        contents = (f"line1{l_end}", f"{l_end}", f"line3{l_end}")
        filename = "test_empty_line.txt"

        with ScratchDir("."):
            # Test text file
            with open(filename, "w", newline="", encoding="utf-8") as file:
                for line in contents:
                    file.write(line)

            revert_contents = tuple(reverse_readfile(filename))
            assert revert_contents[::-1] == contents

            # Test gzip file
            gzip_filename = f"{filename}.gz"
            with gzip.open(gzip_filename, "w") as file_out:
                for line in contents:
                    file_out.write(line.encode())

            revert_contents_gzip = tuple(reverse_readfile(gzip_filename))
            assert revert_contents_gzip[::-1] == contents

            # Test bzip2 file
            bz2_filename = f"{filename}.bz2"
            with bz2.open(bz2_filename, "w") as file_out:
                for line in contents:
                    file_out.write(line.encode())

            revert_contents_bz2 = tuple(reverse_readfile(bz2_filename))
            assert revert_contents_bz2[::-1] == contents

    @pytest.mark.parametrize("l_end", ["\n", "\r\n"])
    def test_line_ending(self, l_end):
        contents = (f"Line1{l_end}", f"Line2{l_end}", f"Line3{l_end}")
        filename = "test_file.txt"

        with ScratchDir("."):
            with open(filename, "w", newline="", encoding="utf-8") as file:
                for line in contents:
                    file.write(line)

            revert_contents = tuple(reverse_readfile(filename))
            assert revert_contents[::-1] == contents


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
