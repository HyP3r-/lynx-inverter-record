#!/usr/bin/env bash
# Build the different tools and libraries for the inverter
# Copyright (C) 2020 Andreas Fendt (mail@andreas-fendt.de)
# Permission to copy and modify is granted under the GNU LESSER GENERAL PUBLIC LICENSE Version 3

# configure verbosity and exit immediately on error
set -ex

# variables
current_directory="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"

# build inverters
declare -a inverters=("power-one_aurora" "kostal_piko")
for inverter in "${inverters[@]}"; do
  [ -f "$current_directory/$inverter/build.sh" ] && bash "$current_directory/$inverter/build.sh" || true
done
