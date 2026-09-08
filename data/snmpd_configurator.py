#!/usr/bin/python
"""Append snmpd `extend` lines for filtered Home Assistant entities using the Supervisor API."""

import fnmatch
import json
import os
import subprocess
import sys
import time

from requests import get

configFile = sys.argv[1]
sensors_to_expose = sys.argv[2]
SupervisorToken = os.environ["SUPERVISOR_TOKEN"]

MAX_ATTEMPTS = 12
RETRY_SLEEP = 5
EXTEND_SCRIPT = "/get_sensor_data_pyconvert.sh"

sensors_to_expose = sensors_to_expose.replace(" ", "")
if sensors_to_expose != "all" and sensors_to_expose != "":
    if "," in sensors_to_expose:
        sensorlist = sensors_to_expose.split(",")
    else:
        sensorlist = [sensors_to_expose]
else:
    sensorlist = ["*"]

URL = "http://supervisor/core/api/states"
headers = {
    "Authorization": "Bearer " + SupervisorToken,
    "content-type": "application/json",
}

HA_SENSORS = None
for attempt in range(1, MAX_ATTEMPTS + 1):
    ha_sensors_request = get(URL, headers=headers, timeout=30)

    status_code = ha_sensors_request.status_code
    content_type = ha_sensors_request.headers.get("Content-Type", "")

    print(f"Response HTTP status code: {status_code}, Content-Type: {content_type}")

    if status_code == 200 and content_type.startswith("application/json"):
        try:
            payload = ha_sensors_request.json()
        except json.JSONDecodeError as e:
            print(f"Error occurred trying to decode JSON response: {e}")
        else:
            if isinstance(payload, list):
                HA_SENSORS = payload
                break
            print("Supervisor JSON was not a list of states")
    else:
        print(
            "The supervisor has returned invalid information, waiting 5 seconds to retry..."
        )

    if attempt == MAX_ATTEMPTS:
        print(f"Supervisor API did not return JSON after {MAX_ATTEMPTS} attempts.")
        sys.exit(1)

    time.sleep(RETRY_SLEEP)

print("Generated SNMP OIDs:")
with open(configFile, "a", encoding="utf-8") as configFileObject:
    for sensor in HA_SENSORS:
        sensorID = sensor["entity_id"]

        TOTAL_MATCHES = 0
        for wildcardelement in sensorlist:
            TOTAL_MATCHES += len(fnmatch.filter([sensorID], wildcardelement))

        if TOTAL_MATCHES <= 0:
            continue

        sensorOID = subprocess.check_output(
            [
                "snmptranslate",
                "-On",
                'NET-SNMP-EXTEND-MIB::nsExtendOutput1Line."' + sensorID + '"',
            ],
            stderr=subprocess.STDOUT,
            text=True,
        )

        configFileObject.write(
            "extend " + sensorID + " " + EXTEND_SCRIPT + " " + sensorID + "\n"
        )
        print("Added SNMP sensor " + sensorID + " with OID: " + sensorOID)
