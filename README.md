# SNMP Sensor Server

Home Assistant add-on that runs an SNMP v2c agent so you can monitor Home Assistant entities (and host details) from tools such as LibreNMS or Nagios.

![aarch64](https://img.shields.io/badge/aarch64-yes-green.svg)
![amd64](https://img.shields.io/badge/amd64-yes-green.svg)

## Requirements

This add-on targets **64-bit** Home Assistant installations only, matching [current Supervisor support](https://www.home-assistant.io/blog/2025/05/22/deprecating-core-and-supervised-installation-methods-and-32-bit-systems/): **aarch64** (ARM64, e.g. Raspberry Pi 4/5) and **amd64** (x86_64). Older 32-bit platforms (`armhf`, `armv7`, `i386`) are not listed in the add-on manifest, so they are unsupported here as well.

## Installation

1. In Home Assistant, open **Settings** → **Add-ons** → **Add-on store** (or **Backup & Supervisor** → **Add-on store** on older layouts).
2. Open the menu (**⋮**) → **Repositories**.
3. Add this repository URL and confirm:

   `https://github.com/iShark5060/Home-Assistant-SNMP-Sensor-Server`

4. Refresh the add-on store, then find **SNMP Sensor Server** and install it.

## Configuration

See **[DOCS.md](DOCS.md)** for options (`community`, `sysname`, `location`, sensor exposure, and so on).

## Support

- [Issues](https://github.com/iShark5060/Home-Assistant-SNMP-Sensor-Server/issues)
- [License](LICENSE.md)

## Credits

This fork continues development of **[PecceG2/Home-Assistant-SNMP-Sensor-Server](https://github.com/PecceG2/Home-Assistant-SNMP-Sensor-Server)**, which extended the earlier **[darthsebulba04/hassio-snmpd](https://github.com/darthsebulba04/hassio-snmpd/)** project. Licensed under the MIT License (see `LICENSE.md`).
