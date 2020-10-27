FROM telegraf

COPY telegraf.conf /etc/telegraf/telegraf.conf

COPY inverter /opt/inverter

RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends build-essential python3 && \
    rm -rf /var/lib/apt/lists/*

RUN /opt/inverter/build.sh
