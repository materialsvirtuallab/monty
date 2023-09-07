import os
import shutil
import unittest

from monty.tempfile import ScratchDir

test_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_files")


class TestScratchDir:
    def setup_method(self):
        self.cwd = os.getcwd()
        os.chdir(test_dir)
        self.scratch_root = os.path.join(test_dir, "..", "..", "tempscratch")
        os.mkdir(self.scratch_root)

    def test_with_copy(self):
        # We write a pre-scratch file.
        with open("pre_scratch_text", "w") as f:
            f.write("write")

        with ScratchDir(
            self.scratch_root,
            copy_from_current_on_enter=True,
            copy_to_current_on_exit=True,
        ) as d:
            with open("scratch_text", "w") as f:
                f.write("write")
            files = os.listdir(d)
            assert "scratch_text" in files
            assert "empty_file.txt" in files
            assert "pre_scratch_text" in files

            # We remove the pre-scratch file.
            os.remove("pre_scratch_text")

        # Make sure the tempdir is deleted.
        assert not os.path.exists(d)
        files = os.listdir(".")
        assert "scratch_text" in files

        # We check that the pre-scratch file no longer exists (because it is
        # deleted in the scratch)
        assert "pre_scratch_text" not in files
        os.remove("scratch_text")

    def test_with_copy_gzip(self):
        # We write a pre-scratch file.
        with open("pre_scratch_text", "w") as f:
            f.write("write")
        init_gz = [f for f in os.listdir(os.getcwd()) if f.endswith(".gz")]
        with ScratchDir(
            self.scratch_root,
            copy_from_current_on_enter=True,
            copy_to_current_on_exit=True,
            gzip_on_exit=True,
        ):
            with open("scratch_text", "w") as f:
                f.write("write")
        files = os.listdir(os.getcwd())

        # Make sure the stratch_text.gz exists
        assert "scratch_text.gz" in files
        for f in files:
            if f.endswith(".gz") and f not in init_gz:
                os.remove(f)
        os.remove("pre_scratch_text")

    def test_with_copy_nodelete(self):
        # We write a pre-scratch file.
        with open("pre_scratch_text", "w") as f:
            f.write("write")

        with ScratchDir(
            self.scratch_root,
            copy_from_current_on_enter=True,
            copy_to_current_on_exit=True,
            delete_removed_files=False,
        ) as d:
            with open("scratch_text", "w") as f:
                f.write("write")
            files = os.listdir(d)
            assert "scratch_text" in files
            assert "empty_file.txt" in files
            assert "pre_scratch_text" in files

            # We remove the pre-scratch file.
            os.remove("pre_scratch_text")

        # Make sure the tempdir is deleted.
        assert not os.path.exists(d)
        files = os.listdir(".")
        assert "scratch_text" in files

        # We check that the pre-scratch file DOES still exists
        assert "pre_scratch_text" in files
        os.remove("scratch_text")
        os.remove("pre_scratch_text")

    def test_no_copy(self):
        with ScratchDir(
            self.scratch_root,
            copy_from_current_on_enter=False,
            copy_to_current_on_exit=False,
        ) as d:
            with open("scratch_text", "w") as f:
                f.write("write")
            files = os.listdir(d)
            assert "scratch_text" in files
            assert "empty_file.txt" not in files

        # Make sure the tempdir is deleted.
        assert not os.path.exists(d)
        files = os.listdir(".")
        assert "scratch_text" not in files

    def test_symlink(self):
        if os.name != "nt":
            with ScratchDir(
                self.scratch_root,
                copy_from_current_on_enter=False,
                copy_to_current_on_exit=False,
                create_symbolic_link=True,
            ) as d:
                with open("scratch_text", "w") as f:
                    f.write("write")
                files = os.listdir(d)
                assert "scratch_text" in files
                assert "empty_file.txt" not in files

            # Make sure the tempdir is deleted.
            assert not os.path.exists(d)
            files = os.listdir(".")
            assert "scratch_text" not in files

            # Make sure the symlink is removed
            assert not os.path.islink("scratch_link")

    def test_bad_root(self):
        with ScratchDir("bad_groot") as d:
            assert d == test_dir

    def teardown_method(self):
        os.chdir(self.cwd)
        shutil.rmtree(self.scratch_root)


if __name__ == "__main__":
    unittest.main()
