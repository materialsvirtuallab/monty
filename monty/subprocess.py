# coding: utf-8
from __future__ import absolute_import, print_function, division, \
    unicode_literals

__author__ = 'Matteo Giantomass'
__copyright__ = "Copyright 2014, The Materials Virtual Lab"
__version__ = '0.1'
__maintainer__ = 'Matteo Giantomassi'
__email__ = 'gmatteo@gmail.com'
__date__ = '10/26/14'


class Command(object):
    """
    Enables to run subprocess commands in a different thread with TIMEOUT
    option.

    Based on jcollado's solution:
        http://stackoverflow.com/questions/1191374/subprocess-with-timeout/4825933#4825933
    and
        https://gist.github.com/kirpit/1306188

    .. attribute:: retcode

        Return code of the subprocess

    .. attribute:: killed

        True if subprocess has been killed due to the timeout

    .. attribute:: output

        stdout of the subprocess

    .. attribute:: error

        stderr of the subprocess

    Example:
        com = Command("sleep 1").run(timeout=2)
        print(com.retcode, com.killed, com.output, com.output)
    """

    def __init__(self, command):
        from .string import is_string
        if is_string(command):
            import shlex
            command = shlex.split(command)

        self.command = command
        self.process = None
        self.retcode = None
        self.output, self.error = '', ''
        self.killed = False

    def __str__(self):
        return "command: %s, retcode: %s" % (self.command, self.retcode)

    def run(self, timeout=None, **kwargs):
        """
        Run a command in a separated thread and wait timeout seconds.
        kwargs are keyword arguments passed to Popen.

        Return: self
        """
        from subprocess import Popen, PIPE

        def target(**kw):
            try:
                # print('Thread started')
                self.process = Popen(self.command, **kw)
                self.output, self.error = self.process.communicate()
                self.retcode = self.process.returncode
                # print('Thread stopped')
            except:
                import traceback
                self.error = traceback.format_exc()
                self.retcode = -1

        # default stdout and stderr
        if 'stdout' not in kwargs:
            kwargs['stdout'] = PIPE

        if 'stderr' not in kwargs:
            kwargs['stderr'] = PIPE

        # thread
        import threading
        thread = threading.Thread(target=target, kwargs=kwargs)
        thread.start()
        thread.join(timeout)

        if thread.is_alive():
            # print("Terminating process")
            self.process.terminate()
            self.killed = True
            thread.join()

        return self
