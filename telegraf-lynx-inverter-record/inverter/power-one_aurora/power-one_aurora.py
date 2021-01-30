#!/usr/bin/env python3

__author__ = "Andreas Fendt"
__copyright__ = "Copyright 2020"
__credits__ = ["Andreas Fendt"]
__license__ = "LGPL v3"
__maintainer__ = "Andreas Fendt"
__email__ = "mail@andreas-fendt.de"
__status__ = "Development"

import argparse
import json
from collections import namedtuple

import serial
from aurorapy.client import AuroraSerialClient


class PowerOneAurora:
    client: AuroraSerialClient

    def __init__(self):
        """
        initialize power one aurora
        """

        # response to telegraf
        self.response = {}

    def execute(self):
        """
        Parse given arguments, call execute targets and send to telegraf
        """

        parser = argparse.ArgumentParser()
        parser.add_argument("-a", "--address", type=int, default=2)
        parser.add_argument("-r", "--retries", type=int, default=3)
        parser.add_argument("-t", "--timeout", type=int, default=5)
        parser.add_argument("-d", "--device", type=str, default="/dev/ttyUSB0")
        args = parser.parse_args()

        # connect to the inverter
        self.client = AuroraSerialClient(port=args.device, address=args.address, parity=serial.PARITY_NONE,
                                         timeout=args.timeout, tries=args.retries)
        self.client.connect()

        # execute targets
        run_targets = [self.process_state, self.process_measurements, self.process_energy]
        for run_target in run_targets:
            try:
                run_target()
            except:
                pass

        # send to telegraf
        self.output()

        # disconnect the inverter
        self.client.close()

    def process_state(self):
        """
        Read state of the inverter
        """

        mapping = {"inverter-state-global": 1,
                   "inverter-state-inverter": 2,
                   "inverter-state-dcdc-channel-1": 3,
                   "inverter-state-dcdc-channel-2": 4,
                   "inverter-state-alarm": 5}

        for field, state in mapping.items():
            try:
                self.response[field] = self.client.state(state, mapped=False)
            except:
                pass

    def process_measurements(self):
        """
        process measurements
        """

        Measurement = namedtuple("Measurement", ["code", "field", "global_measure"])

        measurements = [
            Measurement(1, "grid-voltage", True),
            Measurement(2, "grid-current", True),
            Measurement(3, "grid-power", True),
            Measurement(4, "grid-frequency", False),
            Measurement(5, "vbulk", False),
            Measurement(6, "ileak-dcdc", False),
            Measurement(7, "ileak-inverter", False),
            Measurement(8, "pin1", True),
            Measurement(9, "pin2", False),
            Measurement(21, "temperature-inverter", False),
            Measurement(22, "temperature-booster", False),
            Measurement(23, "input1-voltage", False),
            Measurement(25, "input1-current", True),
            Measurement(26, "input2-voltage", False),
            Measurement(27, "input2-current", False),
            Measurement(28, "grid-voltage-dcdc", False),
            Measurement(29, "grid-frequency-dcdc", False),
            Measurement(30, "isolation-resistance", False),
            Measurement(31, "vbulk-dcdc", False),
            Measurement(32, "average-grid-vgridavg", False),
            Measurement(33, "vbulkmid", False),
            Measurement(34, "power-peak", False),
            Measurement(35, "power-peak-today", False),
            Measurement(36, "grid-voltage-neutral", False),
            Measurement(37, "wind-generator-frequency", False),
            Measurement(38, "grid-voltage-neutral-phase", False),
            Measurement(39, "grid-current-phase-r", False),
            Measurement(40, "grid-current-phase-s", False),
            Measurement(41, "grid-current-phase-t", False),
            Measurement(42, "frequency-phase-r", False),
            Measurement(43, "frequency-phase-s", False),
            Measurement(44, "frequency-phase-t", False),
            Measurement(45, "vbulk+", False),
            Measurement(46, "vbulk-", False),
            Measurement(47, "temperature-supervisor", False),
            Measurement(48, "temperature-alim", False),
            Measurement(49, "temperature-heatsink", False),
            Measurement(50, "temperature-1", False),
            Measurement(51, "temperature-2", False),
            Measurement(52, "temperature-3", False),
            Measurement(53, "fan1-speed", False),
            Measurement(54, "fan2-speed", False),
            Measurement(55, "fan3-speed", False),
            Measurement(56, "fan4-speed", False),
            Measurement(57, "fan5-speed", False),
            Measurement(58, "power-saturation-limit", False),
            Measurement(59, "ring-bulk-reference", False),
            Measurement(60, "vpanel-micro", False),
            Measurement(61, "grid-voltage-phase-r", False),
            Measurement(62, "grid-voltage-phase-s", False),
            Measurement(63, "grid-voltage-phase-t", False),
        ]

        for measurement in measurements:
            try:
                self.response[measurement.field] = self.client.measure(measurement.code,
                                                                       global_measure=measurement.global_measure)
            except:
                pass

    def process_energy(self):
        """
        process energy
        """

        mapping = {"energy-total": 5,
                   "energy-current-day": 0,
                   "energy-current-week": 1,
                   "energy-current-month": 3,
                   "energy-current-year": 4}

        for field, period in mapping.items():
            try:
                self.response[field] = self.client.cumulated_energy(period)
            except:
                pass

    def output(self):
        """
        output for telegraf
        """

        print(json.dumps(self.response))


if __name__ == "__main__":
    power_one_aurora = PowerOneAurora()
    power_one_aurora.execute()
