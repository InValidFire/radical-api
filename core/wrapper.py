"""Wrapper Class to handle reboots"""
import subprocess
import sys


class Wrapper:
    def __init__(self, args, stdout):
        """
        Wraps another program and helps with restarting should the program request.
        :param args: Arguments used to run program
        :param stdout: The stdout stream to send output to
        """
        self._args = args
        self.process = None
        self._stdout = stdout

    def start(self):
        """
        Start the wrapper.
        :return: None
        """
        self.process = subprocess.Popen(self._args, stdout=self._stdout)
        while True:
            while self.process.poll() is None:
                pass
            if self.process.returncode == 26:
                self.process = subprocess.Popen(self._args, stdout=self._stdout)
            else:
                sys.exit()
