# SNMP Sensor Server

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE.md)
[![CI](https://github.com/iShark5060/Home-Assistant-SNMP-Sensor-Server/actions/workflows/ci.yml/badge.svg)](https://github.com/iShark5060/Home-Assistant-SNMP-Sensor-Server/actions/workflows/ci.yml)
[![PR](https://github.com/iShark5060/Home-Assistant-SNMP-Sensor-Server/actions/workflows/pr.yml/badge.svg)](https://github.com/iShark5060/Home-Assistant-SNMP-Sensor-Server/actions/workflows/pr.yml)
![aarch64](https://img.shields.io/badge/aarch64-yes-green.svg)
![amd64](https://img.shields.io/badge/amd64-yes-green.svg)
[![Cursor](https://img.shields.io/badge/Cursor-IDE-141414?logo=cursor&logoColor=white)](https://cursor.com)

Home Assistant add-on that runs Net-SNMP `snmpd` on UDP **161**. Access is `off`, `v2c`, `v3`, or both. SNMPv3 is SHA-256 auth and AES-128 privacy.

It can publish Home Assistant entity `state` strings through Net-SNMP `extend`. That is not a custom enterprise tree. The OIDs are:

`NET-SNMP-EXTEND-MIB::nsExtendOutput1Line."<entity_id>"`

A poll of one of those OIDs forks a small Python helper that GETs `http://supervisor/core/api/states/<entity_id>`. There is no cache. A monitor that walks 200 entities makes 200 Supervisor calls. The entity list is built when the add-on starts, so restart after you add entities or change the whitelist.

`sysName`, `sysLocation`, and `sysContact` come from the options below. This is not a full host agent. Disk, load, and memory checks are not configured.

## Requirements

64-bit Home Assistant only, matching [current Supervisor support](https://www.home-assistant.io/blog/2025/05/22/deprecating-core-and-supervised-installation-methods-and-32-bit-systems/): **aarch64** and **amd64**. Older 32-bit platforms (`armhf`, `armv7`, `i386`) are unsupported.

Entity exposure needs Supervisor (`homeassistant_api`). Without that, the extend helpers cannot read states.

## Installation

1. In Home Assistant, open **Settings** → **Add-ons** → **Add-on store** (or **Backup & Supervisor** → **Add-on store** on older layouts).
2. Open the menu (**⋮**) → **Repositories**.
3. Add this repository URL and confirm:

   `https://github.com/iShark5060/Home-Assistant-SNMP-Sensor-Server`

4. Refresh the add-on store, then find **SNMP Sensor Server** and install it.

## Configuration

Default UDP port is **161**. Full option list: **[DOCS.md](DOCS.md)**.

```yaml
sysname: Home Assistant
community: public
location: Home
name: RPi
email: rpi@me.com
expose_sensors: true
sensors_to_expose: all
snmp_version: v2c
v3_username: hass
v3_auth_passphrase: ""
v3_priv_passphrase: ""
```

`sensors_to_expose` is `all` (every entity_id, not only `sensor.*`) or a comma-separated whitelist with `*` wildcards, for example `sensor.temperature_*,light.*`.

`snmp_version` is `off`, `v2c`, `v3`, or `v2c+v3`. For v3, set `v3_username` and both passphrases (8+ characters).

If you are upgrading from 1.5.x and start fails on an unknown option, delete `expose_sensors_OID_base` from the add-on YAML. That field never drove OIDs and is gone.

### Query

v2c, from another host:

```bash
snmpwalk -v2c -c public <home-assistant-ip> NET-SNMP-EXTEND-MIB::nsExtendOutput1Line
```

v3 (`authPriv`, username `hass` unless you changed it):

```bash
snmpwalk -v3 -l authPriv -u hass \
  -a SHA-256 -A 'your-auth-passphrase' \
  -x AES -X 'your-priv-passphrase' \
  <home-assistant-ip> NET-SNMP-EXTEND-MIB::nsExtendOutput1Line
```

## Support

- [Issues](https://github.com/iShark5060/Home-Assistant-SNMP-Sensor-Server/issues)
- [License](LICENSE.md)

## Credits

This fork continues development of **[PecceG2/Home-Assistant-SNMP-Sensor-Server](https://github.com/PecceG2/Home-Assistant-SNMP-Sensor-Server)**, which extended the earlier **[darthsebulba04/hassio-snmpd](https://github.com/darthsebulba04/hassio-snmpd/)** project. Licensed under the MIT License (see `LICENSE.md`).

## Scripts

| Script             | Description                                             |
| ------------------ | ------------------------------------------------------- |
| `scripts/validate` | Python `py_compile` + `docker build` (CI quality gate). |

## Development

Agent notes: [AGENTS.md](AGENTS.md).

Engineering standards: AppBase `docs/org-standards/` with [personal-repos.md](https://github.com/Dark-Avian-Labs/AppBase/blob/main/docs/org-standards/personal-repos.md) (GitHub-hosted runners).
