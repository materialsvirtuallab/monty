from __future__ import annotations

import os
from pathlib import Path

import pytest
from monty.io import zopen
from monty.os import cd, makedirs_p
from monty.os.path import find_exts, zpath

module_dir = os.path.dirname(__file__)
test_dir = os.path.join(module_dir, "test_files")


class TestPath:
    def test_zpath(self, tmp_path: Path):
        tmp_gz = tmp_path / "tmp.gz"
        tmp_gz.touch()
        ret_path = zpath(str(tmp_gz))
        assert ret_path == str(tmp_gz)

        tmp_not_bz2 = tmp_path / "tmp_not_bz2"
        tmp_not_bz2.touch()

        ret_path = zpath(f"{tmp_not_bz2}.bz2")
        assert ret_path == str(tmp_not_bz2)

    def test_find_exts(self):
        assert len(find_exts(module_dir, "py")) >= 18
        assert len(find_exts(module_dir, "bz2")) == 2
        n_bz2_excl_tests = len(find_exts(module_dir, "bz2", exclude_dirs="test_files"))
        assert n_bz2_excl_tests == 0
        n_bz2_w_tests = find_exts(module_dir, "bz2", include_dirs="test_files")
        assert len(n_bz2_w_tests) == 2


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
