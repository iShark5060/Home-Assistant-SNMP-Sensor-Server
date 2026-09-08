FROM ghcr.io/home-assistant/base:3.24

ENV LANG C.UTF-8

COPY data/* /
RUN chmod a+x /run.sh /get_sensor_data_pyconvert.sh

RUN apk add --no-cache net-snmp net-snmp-tools python3 py3-requests

CMD [ "/run.sh" ]
