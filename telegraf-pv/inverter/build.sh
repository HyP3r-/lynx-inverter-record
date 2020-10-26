#!/usr/bin/env bash

set -ex

# install build tools
DEBIAN_FRONTEND=noninteractive apt-get update && \
DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends build-essential && \
rm -rf /var/lib/apt/lists/*

# build aurora
cd /opt/inverter/aurora && \
wget --no-verbose http://www.curtronics.com/Solar/ftp/aurora-1.9.4.tar.gz && \
tar xzf aurora-1.9.4.tar.gz && \
cd aurora-1.9.4 && \
make && \
make install
rm -rf /opt/inverter/aurora/aurora-1.9.4.tar.gz /opt/inverter/aurora/aurora-1.9.4
