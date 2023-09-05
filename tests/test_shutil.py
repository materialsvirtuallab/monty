import os
import platform
import shutil
import tempfile
import unittest
from gzip import GzipFile
from pathlib import Path

import pytest

from monty.shutil import (
    compress_dir,
    compress_file,
    copy_r,
    decompress_dir,
    decompress_file,
    gzip_dir,
    remove,
)

test_dir = os.path.join(os.path.dirname(__file__), "test_files")


class TestCopyR:
    def setup_method(self):
        os.mkdir(os.path.join(test_dir, "cpr_src"))
        with open(os.path.join(test_dir, "cpr_src", "test"), "w") as f:
            f.write("what")
        os.mkdir(os.path.join(test_dir, "cpr_src", "sub"))
        with open(os.path.join(test_dir, "cpr_src", "sub", "testr"), "w") as f:
            f.write("what2")

    def test_recursive_copy_and_compress(self):
        copy_r(os.path.join(test_dir, "cpr_src"), os.path.join(test_dir, "cpr_dst"))
        assert os.path.exists(os.path.join(test_dir, "cpr_dst", "test"))
        assert os.path.exists(os.path.join(test_dir, "cpr_dst", "sub", "testr"))

        compress_dir(os.path.join(test_dir, "cpr_src"))
        assert os.path.exists(os.path.join(test_dir, "cpr_src", "test.gz"))
        assert os.path.exists(os.path.join(test_dir, "cpr_src", "sub", "testr.gz"))

        decompress_dir(os.path.join(test_dir, "cpr_src"))
        assert os.path.exists(os.path.join(test_dir, "cpr_src", "test"))
        assert os.path.exists(os.path.join(test_dir, "cpr_src", "sub", "testr"))
        with open(os.path.join(test_dir, "cpr_src", "test")) as f:
            txt = f.read()
            assert txt == "what"

    def test_pathlib(self):
        test_path = Path(test_dir)
        copy_r(test_path / "cpr_src", test_path / "cpr_dst")
        assert (test_path / "cpr_dst" / "test").exists()
        assert (test_path / "cpr_dst" / "sub" / "testr").exists()

    def teardown_method(self):
        shutil.rmtree(os.path.join(test_dir, "cpr_src"))
        shutil.rmtree(os.path.join(test_dir, "cpr_dst"))


class TestCompressFileDir:
    def setup_method(self):
        with open(os.path.join(test_dir, "tempfile"), "w") as f:
            f.write("hello world")

    def test_compress_and_decompress_file(self):
        fname = os.path.join(test_dir, "tempfile")
        for fmt in ["gz", "bz2"]:
            compress_file(fname, fmt)
            assert os.path.exists(fname + "." + fmt)
            assert not os.path.exists(fname)
            decompress_file(fname + "." + fmt)
            assert os.path.exists(fname)
            assert not os.path.exists(fname + "." + fmt)
        with open(fname) as f:
            txt = f.read()
            assert txt == "hello world"
        with pytest.raises(ValueError):
            compress_file("whatever", "badformat")

        # test decompress non-existent/non-compressed file
        assert decompress_file("non-existent") is None
        assert decompress_file("non-existent.gz") is None
        assert decompress_file("non-existent.bz2") is None

    def teardown_method(self):
        os.remove(os.path.join(test_dir, "tempfile"))


class TestGzipDir:
    def setup_method(self):
        os.mkdir(os.path.join(test_dir, "gzip_dir"))
        with open(os.path.join(test_dir, "gzip_dir", "tempfile"), "w") as f:
            f.write("what")

        self.mtime = os.path.getmtime(os.path.join(test_dir, "gzip_dir", "tempfile"))

    def test_gzip(self):
        full_f = os.path.join(test_dir, "gzip_dir", "tempfile")
        gzip_dir(os.path.join(test_dir, "gzip_dir"))

        assert os.path.exists(f"{full_f}.gz")
        assert not os.path.exists(full_f)

        with GzipFile(f"{full_f}.gz") as g:
            assert g.readline().decode("utf-8") == "what"

        assert os.path.getmtime(f"{full_f}.gz") == pytest.approx(self.mtime, 4)

    def test_handle_sub_dirs(self):
        sub_dir = os.path.join(test_dir, "gzip_dir", "sub_dir")
        sub_file = os.path.join(sub_dir, "new_tempfile")
        os.mkdir(sub_dir)
        with open(sub_file, "w") as f:
            f.write("anotherwhat")

        gzip_dir(os.path.join(test_dir, "gzip_dir"))

        assert os.path.exists(f"{sub_file}.gz")
        assert not os.path.exists(sub_file)

        with GzipFile(f"{sub_file}.gz") as g:
            assert g.readline().decode("utf-8") == "anotherwhat"

    def teardown_method(self):
        shutil.rmtree(os.path.join(test_dir, "gzip_dir"))


class TestRemove:
    @unittest.skipIf(platform.system() == "Windows", "Skip on windows")
    def test_remove_file(self):
        tempdir = tempfile.mkdtemp(dir=test_dir)
        tempf = tempfile.mkstemp(dir=tempdir)[1]
        remove(tempf)
        assert not os.path.isfile(tempf)
        shutil.rmtree(tempdir)

    @unittest.skipIf(platform.system() == "Windows", "Skip on windows")
    def test_remove_folder(self):
        tempdir = tempfile.mkdtemp(dir=test_dir)
        remove(tempdir)
        assert not os.path.isdir(tempdir)

    @unittest.skipIf(platform.system() == "Windows", "Skip on windows")
    def test_remove_symlink(self):
        tempdir = tempfile.mkdtemp(dir=test_dir)
        tempf = tempfile.mkstemp(dir=tempdir)[1]

        os.symlink(tempdir, os.path.join(test_dir, "temp_link"))
        templink = os.path.join(test_dir, "temp_link")
        remove(templink)
        assert os.path.isfile(tempf)
        assert os.path.isdir(tempdir)
        assert not os.path.islink(templink)
        remove(tempdir)

    @unittest.skipIf(platform.system() == "Windows", "Skip on windows")
    def test_remove_symlink_follow(self):
        tempdir = tempfile.mkdtemp(dir=test_dir)
        tempf = tempfile.mkstemp(dir=tempdir)[1]

        os.symlink(tempdir, os.path.join(test_dir, "temp_link"))
        templink = os.path.join(test_dir, "temp_link")
        remove(templink, follow_symlink=True)
        assert not os.path.isfile(tempf)
        assert not os.path.isdir(tempdir)
        assert not os.path.islink(templink)
