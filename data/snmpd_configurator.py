#!/usr/bin/python
"""Append snmpd `extend` lines for filtered Home Assistant entities using the Supervisor API."""

import fnmatch
import json
import os
import re
import subprocess
import sys
import time

from requests import get

configFile = sys.argv[1]
OIDPrefix = sys.argv[2]
sensors_to_expose = sys.argv[3]
SupervisorToken = os.environ["SUPERVISOR_TOKEN"]


def sensor_finder(patterns, string):
    """Return True if ``string`` matches pattern in ``patterns``; ``*`` matches any substring."""
    for element in patterns:
        regex = re.escape(element).replace("\\*", ".*")
        if re.fullmatch(regex, string):
            return True
    return False


sensors_to_expose = sensors_to_expose.replace(" ", "")
if sensors_to_expose != "all" and sensors_to_expose != "":
    if "," in sensors_to_expose:
        sensorlist = sensors_to_expose.split(",")
    else:
        sensorlist = [sensors_to_expose]
else:
    sensorlist = ["*"]

configFileObject = open(configFile, "a", encoding="utf-8")

URL = "http://supervisor/core/api/states"
headers = {
    "Authorization": "Bearer " + SupervisorToken,
    "content-type": "application/json",
}


while True:
    ha_sensors_request = get(URL, headers=headers, timeout=30)

    status_code = ha_sensors_request.status_code
    content_type = ha_sensors_request.headers.get("Content-Type", "")

    print(f"Response HTTP status code: {status_code}, Content-Type: {content_type}")

    if status_code == 200 and content_type.startswith("application/json"):
        try:
            ha_sensors = ha_sensors_request.json()
            break
        except json.JSONDecodeError as e:
            print(f"Error ocurred trying decode JSON response: {e}")
    else:
        print(
            "The supervisor has returned invalid information, waiting 5 seconds to retry..."
        )

    time.sleep(5)

print("Generated SNMP OIDs:")
for sensor in ha_sensors:
    sensorID = sensor["entity_id"]

    TOTAL_MATCHES = 0
    for wildcardelement in sensorlist:
        TOTAL_MATCHES += len(fnmatch.filter([sensorID], wildcardelement))

    if TOTAL_MATCHES <= 0:
        continue

    sensorOID = subprocess.check_output(
        'snmptranslate -On NET-SNMP-EXTEND-MIB::nsExtendOutput1Line.\\"'
        + sensorID
        + '\\"',
        shell=True,
        stderr=subprocess.STDOUT,
        text=True,
    )

    configFileObject.write(
        "extend " + sensorID + " get_sensor_data_pyconvert.sh " + sensorID + "\n"
    )
    print("Added SNMP sensor " + sensorID + " with OID: " + sensorOID)


configFileObject.close()
