"""Print a Home Assistant entity state from the Supervisor API (CLI helper for SNMP)."""

import json
import os
import sys

from requests import get

sensorID = sys.argv[1]
SupervisorToken = os.environ["SUPERVISOR_TOKEN"]


url = "http://supervisor/core/api/states/" + sensorID
headers = {
    "Authorization": "Bearer " + SupervisorToken,
    "content-type": "application/json",
}

ha_sensor_data_request = get(url, headers=headers, timeout=30)
ha_sensor = json.loads(ha_sensor_data_request.text)

print(ha_sensor["state"])
