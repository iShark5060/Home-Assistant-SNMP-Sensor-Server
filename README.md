# SNMP Sensor Server

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE.md)
[![CI](https://github.com/iShark5060/Home-Assistant-SNMP-Sensor-Server/actions/workflows/ci.yml/badge.svg)](https://github.com/iShark5060/Home-Assistant-SNMP-Sensor-Server/actions/workflows/ci.yml)
[![PR](https://github.com/iShark5060/Home-Assistant-SNMP-Sensor-Server/actions/workflows/pr.yml/badge.svg)](https://github.com/iShark5060/Home-Assistant-SNMP-Sensor-Server/actions/workflows/pr.yml)
![aarch64](https://img.shields.io/badge/aarch64-yes-green.svg)
![amd64](https://img.shields.io/badge/amd64-yes-green.svg)
[![Cursor](https://img.shields.io/badge/Cursor-IDE-141414?logo=cursor&logoColor=white)](https://cursor.com)

Home Assistant add-on that runs an SNMP agent (v2c, v3, both, or off). SNMPv3 uses SHA-256 and AES-128. Expose Home Assistant entities and host details to LibreNMS or Nagios.

## Requirements

This add-on targets **64-bit** Home Assistant installations only, matching [current Supervisor support](https://www.home-assistant.io/blog/2025/05/22/deprecating-core-and-supervised-installation-methods-and-32-bit-systems/): **aarch64** (ARM64, e.g. Raspberry Pi 4/5) and **amd64** (x86_64). Older 32-bit platforms (`armhf`, `armv7`, `i386`) are not listed in the add-on manifest, so they are unsupported here as well.

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
expose_sensors_OID_base: "1.3.6.1.4.1.43.10.210."
sensors_to_expose: all
snmp_version: v2c
v3_username: hass
v3_auth_passphrase: ""
v3_priv_passphrase: ""
```

`sensors_to_expose` is `all` (every entity) or a comma-separated `entity_id` whitelist with `*` wildcards. `expose_sensors_OID_base` is accepted by the UI but is **not applied** yet; entity OIDs come from Net-SNMP `extend`.

`snmp_version` is `off`, `v2c`, `v3`, or `v2c+v3`. For v3, set `v3_username` (your USM name) and both passphrases. Auth is SHA-256, privacy is AES-128.

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
