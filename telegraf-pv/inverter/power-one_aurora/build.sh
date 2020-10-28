#!/usr/bin/env bash
# Install python aurorapy from Claudio Catterina
# Copyright (C) 2020 Andreas Fendt (mail@andreas-fendt.de)
# Permission to copy and modify is granted under the GNU LESSER GENERAL PUBLIC LICENSE Version 3

# configure verbosity and exit immediately on error
set -ex

# install aurorapy
DEBIAN_FRONTEND=noninteractive apt-get update &&
  DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3 python3-pip python3-wheel python3-setuptools &&
  pip3 install aurorapy &&
  rm -rf /var/lib/apt/lists/*
