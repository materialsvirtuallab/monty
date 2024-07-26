from __future__ import annotations

from monty.subprocess import Command


def test_command():
    """Test Command class"""
    sleep05 = Command("sleep 0.5")

    sleep05.run(timeout=1)
    print(sleep05, sleep05.error, sleep05.output)  # DEBUG
    assert sleep05.retcode == 0, sleep05
    assert not sleep05.killed

    sleep05.run(timeout=0.1)
    assert sleep05.retcode != 0
    assert sleep05.killed
