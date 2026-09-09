# SNMP Sensor Server

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE.md)
[![CI](https://img.shields.io/github/actions/workflow/status/iShark5060/Home-Assistant-SNMP-Sensor-Server/ci.yml?style=flat-square&label=CI)](https://github.com/iShark5060/Home-Assistant-SNMP-Sensor-Server/actions/workflows/ci.yml)
[![PR](https://img.shields.io/github/actions/workflow/status/iShark5060/Home-Assistant-SNMP-Sensor-Server/pr.yml?style=flat-square&label=PR)](https://github.com/iShark5060/Home-Assistant-SNMP-Sensor-Server/actions/workflows/pr.yml)
![aarch64](https://img.shields.io/badge/aarch64-yes-green.svg?style=flat-square)
![amd64](https://img.shields.io/badge/amd64-yes-green.svg?style=flat-square)
[![Cursor](https://img.shields.io/badge/Cursor-IDE-141414?logo=cursor&logoColor=white&style=flat-square)](https://cursor.com)

Home Assistant add-on that runs Net-SNMP `snmpd` on UDP **161**. Access is `off`, `v2c`, `v3`, or both. SNMPv3 is SHA-256 auth and AES-128 privacy. Optional entity `state` strings go through Net-SNMP `extend`, not a custom enterprise tree:

`NET-SNMP-EXTEND-MIB::nsExtendOutput1Line."<entity_id>"`

Fork of [PecceG2/Home-Assistant-SNMP-Sensor-Server](https://github.com/PecceG2/Home-Assistant-SNMP-Sensor-Server) (itself from [darthsebulba04/hassio-snmpd](https://github.com/darthsebulba04/hassio-snmpd/)). Options: [DOCS.md](DOCS.md).

Add the repository `https://github.com/iShark5060/Home-Assistant-SNMP-Sensor-Server` in **Settings → Add-ons → Add-on store → ⋮ → Repositories**, then install **SNMP Sensor Server**.

```bash
snmpwalk -v2c -c public <home-assistant-ip> NET-SNMP-EXTEND-MIB::nsExtendOutput1Line
```

## Gotchas

- **aarch64** and **amd64** only. Entity exposure needs Supervisor (`homeassistant_api`). Without it, extend helpers cannot read states.
- Each OID poll forks a helper that GETs `http://supervisor/core/api/states/<entity_id>`. There is no cache. Walking 200 entities is 200 Supervisor calls. Failures print `unavailable`.
- The entity list is built at start. Restart after you add entities or change the whitelist (`all`, or comma-separated patterns with `*`).
- This is not a full host agent. Disk, load, and memory checks are not configured.
- v3 passphrases must be 8+ characters. `createUser` is written before snmpd starts; adding it while snmpd is already running is discarded on shutdown.
- Upgrading from 1.5.x: delete `expose_sensors_OID_base` from the add-on YAML if start fails on an unknown option. That field never drove OIDs.

## License

MIT. See [LICENSE.md](LICENSE.md).
