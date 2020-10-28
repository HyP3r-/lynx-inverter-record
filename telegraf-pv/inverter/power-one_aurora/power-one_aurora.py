#!/usr/bin/env python3

__author__ = "Andreas Fendt"
__copyright__ = "Copyright 2020"
__credits__ = ["Andreas Fendt"]
__license__ = "LGPL v3"
__version__ = "0.0.1"
__maintainer__ = "Andreas Fendt"
__email__ = "mail@andreas-fendt.de"
__status__ = "Development"

import subprocess
import json
import argparse


class PowerOneAurora:
    def __init__(self):
        # configuration
        self.aurora_program = "aurora"

        # response to telegraf
        self.response = {}

        self.timeout = 2
        self.default_arguments_prefix = None
        self.default_arguments_suffix = None

    def call_aurora(self, command, columnize=True):
        """
        Call the aurora tool and wait for response
        """

        return subprocess.check_output(self.default_arguments_prefix +
                                       (["--columnize"] if columnize else []) +
                                       [command] +
                                       self.default_arguments_suffix,
                                       timeout=self.timeout).decode()

    def execute(self):
        """
        Parse given arguments, call execute targets and send to telegraf
        """

        parser = argparse.ArgumentParser()
        parser.add_argument("-a", "--address", type=int, default=2)
        parser.add_argument("-r", "--retries", type=int, default=3)
        parser.add_argument("-t", "--timeout", type=int, default=2)
        parser.add_argument("-d", "--device", type=str, default="/dev/ttyUSB0")
        args = parser.parse_args()

        # default arguments
        self.timeout = args.timeout
        self.default_arguments_prefix = [self.aurora_program, f"--retries={args.retries}",
                                         f"--address={args.address}"]
        self.default_arguments_suffix = [args.device]

        # execute targets
        run_targets = [self.execute_energy, self.execute_alarm]
        for run_target in run_targets:
            try:
                run_target()
            except:
                pass

        # send to telegraf
        self.output()

    def execute_energy(self):
        """
        process energy
        """

        output = self.call_aurora("--get-energy").split()
        if output[7] != "OK":
            return
        self.response["ac-total-energy"] = float(output[5])

    def execute_alarm(self):
        """
        process alarms
        """

        output = self.call_aurora("--last-alarms", columnize=False).split("\n")
        alarms = list(filter(lambda s: str(s).startswith("Alarm"), output))
        alarms = list(map(lambda s: str(s)[23:], alarms))
        self.response.update({f"alarm-{index}": alarms[index] for index in range(4)})

    def output(self):
        """
        output for telegraf
        """

        print(json.dumps(self.response))


if __name__ == "__main__":
    power_one_aurora = PowerOneAurora()
    power_one_aurora.execute()
