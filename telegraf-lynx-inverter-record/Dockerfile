FROM telegraf

COPY telegraf.conf /etc/telegraf/telegraf.conf

COPY inverter /opt/inverter

RUN /opt/inverter/build.sh
