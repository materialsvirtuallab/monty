from __future__ import annotations

from monty.subprocess import Command


def test_command():
    """Test Command class"""
    sleep05 = Command("sleep 0.5")

    sleep05.run(timeout=1)
    # DEBUG: this unit test fail in Windows CI intermittently (PR702)
    full_msg = f"{sleep05=}\n{sleep05.error=}\n{sleep05.output}"
    assert sleep05.retcode == 0, full_msg
    assert not sleep05.killed

    sleep05.run(timeout=0.1)
    assert sleep05.retcode != 0
    assert sleep05.killed
