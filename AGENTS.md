# HA-SNMP (SNMP Sensor Server)

## Org standards

CI/README/validate conventions live in AppBase `docs/org-standards/` with personal-repo overrides (`personal-repos.md`). GitHub-hosted `ubuntu-latest`, not Blacksmith. Quality gate: `scripts/validate` (Python `py_compile` + `docker build`).

## Overview

Home Assistant Supervisor add-on that runs an SNMP agent (`snmp_version`: off, v2c, v3, or v2c+v3; v3 is SHA-256/AES-128) and can expose HA entity states (plus sys* fields) to monitors like LibreNMS. Install and user options: `README.md` and `DOCS.md`.

## Add-on contracts

Requires Supervisor (`homeassistant_api: true`); sensor helpers call `http://supervisor/core/api/states` with `SUPERVISOR_TOKEN`. Architectures are **aarch64** and **amd64** only. Default UDP map is `161/udp`.

When `expose_sensors` is true, `snmpd_configurator.py` appends snmpd `extend` lines (whitelist `sensors_to_expose`: `all` or comma-separated patterns with `*`). It retries until Supervisor returns JSON; a bad API response can stall start. `expose_sensors_OID_base` is passed as argv[2] but unused; printed OIDs come from `snmptranslate` on `NET-SNMP-EXTEND-MIB::nsExtendOutput1Line."<entity_id>"`. `run.sh` may `apk add py3-requests` at runtime when exposing sensors.

`snmp_version` is `off` (idle, no snmpd), `v2c`, `v3`, or `v2c+v3`. v2c uses `community`. v3 uses custom `v3_username` plus passphrases: `rouser <user> priv` in `/etc/snmp/snmpd.conf` and `createUser <user> SHA-256 … AES …` in `/data/net-snmp/snmpd.conf` (symlinked as snmpd's persistent dir). That write happens before `snmpd` starts. snmpd rewrites the persistent file on shutdown, so a `createUser` added while it is running is discarded. Prior `usmUser`/`createUser` lines are stripped on each start so username/passphrase changes apply. Passphrases must be 8+ characters.

`scripts/validate` compiles `data/*.py` then builds with `--build-arg BUILD_FROM=…` (default `ghcr.io/home-assistant/amd64-base:3.20`).
