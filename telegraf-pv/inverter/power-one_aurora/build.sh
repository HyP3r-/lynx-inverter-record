#!/usr/bin/env bash
# Build the aurora tool from Curtis J. Blank
# Copyright (C) 2020 Andreas Fendt (mail@andreas-fendt.de)
# Permission to copy and modify is granted under the GNU LESSER GENERAL PUBLIC LICENSE Version 3

# build aurora
cd /tmp && \
wget --no-verbose http://www.curtronics.com/Solar/ftp/aurora-1.9.4.tar.gz && \
tar xzf aurora-1.9.4.tar.gz && \
cd aurora-1.9.4 && \
make && \
make install
rm -rf /tmp/aurora-1.9.4.tar.gz /tmp/aurora-1.9.4
