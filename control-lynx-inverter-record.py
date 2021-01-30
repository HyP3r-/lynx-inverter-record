#!/usr/bin/env bash

__author__ = "Andreas Fendt"
__copyright__ = "Copyright 2021"
__credits__ = ["Andreas Fendt"]
__license__ = "LGPL v3"
__maintainer__ = "Andreas Fendt"
__email__ = "mail@andreas-fendt.de"
__status__ = "Development"

import argparse
import os
import toml
from abc import ABC, abstractmethod


class Inverter:
    @staticmethod
    @abstractmethod
    def get_config_name() -> str:
        pass

    @staticmethod
    @abstractmethod
    def map_configuration(config: dict, index: int) -> dict:
        pass


class KostalPiko(Inverter):
    @staticmethod
    def get_config_name() -> str:
        return "kostal_piko"

    @staticmethod
    def map_configuration(config: dict, index: int) -> dict:
        return {
            "inputs.exec": {
                "commands": [f"/opt/inverter/kostal_piko/kostal_piko.py --hostname {config['hostname']}"],
                "timeout": "10s",
                "name_suffix": f"_inverter_{index}",
                "data_format": "json"
            }
        }


class PowerOneAurora(Inverter):
    @staticmethod
    def get_config_name() -> str:
        return "power-one_aurora"

    @staticmethod
    def map_configuration(config: dict, index: int) -> dict:
        return {
            "inputs.exec": {
                "commands": [f"opt/inverter/power-one_aurora/power-one_aurora.py "
                             f"--address {config['address']} "
                             f"--device {config['device']}"],
                "timeout": "10s",
                "name_suffix": f"_inverter_{index}",
                "data_format": "json"
            }
        }


def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg


class Control:
    def __init__(self):
        known_inverters = [KostalPiko, PowerOneAurora]
        self.known_inverters = {inverter.get_config_name(): inverter for inverter in known_inverters}

    def control(self):
        """
        Control the Lynx Inverter Record System
        """

        # TODO: sanity checks: check for docker and docker-compose

        # parse arguments
        parser = argparse.ArgumentParser(prog="Lynx Inverter Record", description="Control Lynx Inverter Record")

        sp = parser.add_subparsers()
        sp_start = sp.add_parser("start", help="Starts %(prog)s")
        sp_stop = sp.add_parser("stop", help="Stops %(prog)s")
        sp_restart = sp.add_parser("restart", help="Restarts %(prog)s")
        sp_configure = sp.add_parser("configure", help="Configure %(prog)s")
        sp_configure.add_argument("config", help="Path to the configuration file", metavar="FILE",
                                  type=lambda x: is_valid_file(parser, x), nargs="?",
                                  default="/etc/lynx-inverter-record/lynx.toml")

        sp_start.set_defaults(func=self.start)
        sp_stop.set_defaults(func=self.stop)
        sp_restart.set_defaults(func=self.restart)
        sp_configure.set_defaults(func=self.configure)

        args = parser.parse_args()
        args.func(args)

    def start(self, args):
        """
        Load configuration file and generate telegraf configuration
        """

        # TODO: start docker compose
        pass

    def stop(self, args):
        """
        Load configuration file and generate telegraf configuration
        """

        # TODO: stop docker compose
        pass

    def restart(self, args):
        """
        Load configuration file and generate telegraf configuration
        """

        self.stop(args)
        self.start(args)

    def configure(self, args):
        """
        Load configuration file and generate telegraf configuration
        """

        with open(args.config, "r") as config_file:
            input_configuration = toml.load(config_file)

        # map configuration
        index = 0
        output_configuration = []

        for key, configuration_inverter in dict(input_configuration["inverters"]).items():
            if configuration_inverter["model"] not in self.known_inverters.keys():
                raise Exception(f"Unknown Inverter {configuration_inverter['model']}")

            output_configuration += [self.known_inverters[configuration_inverter["model"]]
                                         .map_configuration(configuration_inverter, index)]

            index += 1

        # write template
        # TODO: write template


if __name__ == "__main__":
    control = Control()
    control.control()
