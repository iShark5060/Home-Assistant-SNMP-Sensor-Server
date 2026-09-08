"""Print a Home Assistant entity state from the Supervisor API (CLI helper for SNMP)."""

import os
import sys

from requests import RequestException, get

UNAVAILABLE = "unavailable"

sensorID = sys.argv[1]
SupervisorToken = os.environ["SUPERVISOR_TOKEN"]

url = "http://supervisor/core/api/states/" + sensorID
headers = {
    "Authorization": "Bearer " + SupervisorToken,
    "content-type": "application/json",
}

try:
    ha_sensor_data_request = get(url, headers=headers, timeout=30)
    if ha_sensor_data_request.status_code != 200:
        print(UNAVAILABLE)
        sys.exit(0)
    ha_sensor = ha_sensor_data_request.json()
    print(ha_sensor.get("state", UNAVAILABLE))
except (RequestException, ValueError, TypeError, AttributeError):
    print(UNAVAILABLE)
