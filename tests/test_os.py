import os

import pytest

from monty.os import cd, makedirs_p
from monty.os.path import find_exts, zpath

test_dir = os.path.join(os.path.dirname(__file__), "test_files")


class TestPath:
    def test_zpath(self):
        fullzpath = zpath(os.path.join(test_dir, "myfile_gz"))
        assert os.path.join(test_dir, "myfile_gz.gz") == fullzpath

    def test_find_exts(self):
        assert len(find_exts(os.path.dirname(__file__), "py")) >= 18
        assert len(find_exts(os.path.dirname(__file__), "bz2")) == 2
        assert len(find_exts(os.path.dirname(__file__), "bz2", exclude_dirs="test_files")) == 0
        assert len(find_exts(os.path.dirname(__file__), "bz2", include_dirs="test_files")) == 2


class TestCd:
    def test_cd(self):
        with cd(test_dir):
            assert os.path.exists("empty_file.txt")
        assert not os.path.exists("empty_file.txt")

    def test_cd_exception(self):
        with cd(test_dir):
            assert os.path.exists("empty_file.txt")
        assert not os.path.exists("empty_file.txt")


class TestMakedirs_p:
    def setup_method(self):
        self.test_dir_path = os.path.join(test_dir, "test_dir")

    def test_makedirs_p(self):
        makedirs_p(self.test_dir_path)
        assert os.path.exists(self.test_dir_path)
        makedirs_p(self.test_dir_path)
        with pytest.raises(OSError):
            makedirs_p(os.path.join(test_dir, "myfile_txt"))

    def teardown_method(self):
        os.rmdir(self.test_dir_path)
