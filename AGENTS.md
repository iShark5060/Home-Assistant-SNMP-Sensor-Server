# HA-SNMP (SNMP Sensor Server)

## Org standards

CI/README/validate conventions live in AppBase `docs/org-standards/` with personal-repo overrides (`personal-repos.md`). GitHub-hosted `ubuntu-latest`, not Blacksmith. Quality gate: `scripts/validate` (Python `py_compile` + `docker build`).

## Overview

Home Assistant Supervisor add-on that runs Net-SNMP `snmpd` (`snmp_version`: off, v2c, v3, or v2c+v3; v3 is SHA-256/AES-128). Optional HA entity `state` strings via `extend`, plus sys* fields. Install and user options: `README.md` and `DOCS.md`.

## Add-on contracts

Requires Supervisor (`homeassistant_api: true`); sensor helpers call `http://supervisor/core/api/states` with `SUPERVISOR_TOKEN`. Architectures are **aarch64** and **amd64** only. Default UDP map is `161/udp`.

When `expose_sensors` is true, `snmpd_configurator.py` appends snmpd `extend` lines (whitelist `sensors_to_expose`: `all` or comma-separated patterns with `*`). Supervisor fetch retries 12 times then `sys.exit(1)`. Printed OIDs come from `snmptranslate` on `NET-SNMP-EXTEND-MIB::nsExtendOutput1Line."<entity_id>"`. Extend PROG is `/get_sensor_data_pyconvert.sh`. Image includes `py3-requests`. Poll helper prints `unavailable` on API errors.

`snmp_version` is `off` (idle, no snmpd), `v2c`, `v3`, or `v2c+v3`. v2c uses `community`. v3 uses custom `v3_username` plus passphrases: `rouser <user> priv` in `/etc/snmp/snmpd.conf` and `createUser <user> SHA-256 … AES …` in `/data/net-snmp/snmpd.conf` (symlinked as snmpd's persistent dir). That write happens before `snmpd` starts. snmpd rewrites the persistent file on shutdown, so a `createUser` added while it is running is discarded. Prior `usmUser`/`createUser` lines are stripped only when v3 is enabled at start. Passphrases must be 8+ characters.

`scripts/validate` compiles `data/*.py` then builds with `--build-arg BUILD_FROM=…` (default `ghcr.io/home-assistant/amd64-base:3.20`).
