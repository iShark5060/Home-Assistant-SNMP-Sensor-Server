# Home Assistant Add-on: SNMP Sensor Server

SNMP agent for Home Assistant: **v2c**, **v3** (SHA-256 / AES-128), both, or off. Optional exposure of entity `state` strings through Net-SNMP `extend`, plus `sysName` / `sysLocation` / `sysContact`.

64-bit Supervisor only: **aarch64** and **amd64**. Default UDP map is **161**.

## Installation

From the Supervisor add-on store, add this repository:

https://github.com/iShark5060/Home-Assistant-SNMP-Sensor-Server

Install **SNMP Sensor Server**.

## How to use

1. Set `snmp_version` to `off`, `v2c`, `v3`, or `v2c+v3`. For v2c, set `community`. For v3, set `v3_username` and both passphrases. Fill in the other options if you wish.
2. Set the UDP port under Network if you do not want the default `161`.
3. Save the add-on configuration.
4. Start the add-on.

The add-on talks to Home Assistant through the Supervisor API (`homeassistant_api`). Entity exposure will not work without that. The entity list is built at start. Restart the add-on after you add entities or change the whitelist.

## Configuration

Example:

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

### Option: `snmp_version`

Which SNMP access to offer. Default `v2c`.

- `off`: add-on stays running but does not start snmpd.
- `v2c`: community string only.
- `v3`: SNMPv3 `authPriv` only (SHA-256 / AES-128).
- `v2c+v3`: both.

### Option: `community`

SNMP v2c community string the monitor must use. Default `public`. Required when `snmp_version` is `v2c` or `v2c+v3`. Ignored for `v3` and `off`.

### Option: `sysname`

`sysName` reported by snmpd. Default `Home Assistant`.

### Option: `location`

`sysLocation`. Empty by default.

### Option: `name`

Contact display name. Combined with `email` into snmpd `sysContact` as `name <email>`.

### Option: `email`

Contact email used in `sysContact` with `name`.

### Option: `expose_sensors`

When `true` (default), the add-on queries Supervisor for entity states and adds an snmpd `extend` line per matching entity. A GET of that OID runs `/get_sensor_data.py`, which returns the current `state` string. A failed Supervisor call prints `unavailable` instead of failing the extend.

When `false`, only `sysName`, `sysLocation`, and `sysContact` are set in snmpd.conf. Compiled-in mibII may still appear. UCD-SNMP disk/load is not configured.

Entity generation retries the Supervisor API up to 12 times (5s apart). After that the add-on start fails.

### Option: `sensors_to_expose`

Whitelist of Home Assistant `entity_id` patterns, comma-separated. `*` is a wildcard. `all` or empty exposes every entity, not only `sensor.*`. Spaces around commas are ignored.

Examples: `sensor.temperature_*`, `light.*,switch.office`.

### Option: `v3_username`

SNMPv3 USM user name. Default `hass`. Set this to whatever your monitor should log in as. Required when `snmp_version` is `v3` or `v2c+v3`. Letters, numbers, `.`, `_`, and `-` only.

The user is created with snmpd's `createUser` in the persistent store (`/data/net-snmp/snmpd.conf`) **before** snmpd starts. snmpd rewrites that file on shutdown, so a `createUser` written while the daemon is running is dropped. Access is `rouser <username> priv`.

Example walk from another host (username `hass` here; use your `v3_username`):

```bash
snmpwalk -v3 -l authPriv -u hass \
  -a SHA-256 -A 'your-auth-passphrase' \
  -x AES -X 'your-priv-passphrase' \
  <home-assistant-ip> sysDescr
```

### Option: `v3_auth_passphrase`

SHA-256 authentication passphrase. Required when `snmp_version` is `v3` or `v2c+v3`. At least 8 characters.

### Option: `v3_priv_passphrase`

AES-128 privacy passphrase. Required when `snmp_version` is `v3` or `v2c+v3`. At least 8 characters.

## Entity OIDs

Walk `NET-SNMP-EXTEND-MIB::nsExtendOutput1Line."<entity_id>"`. The old `expose_sensors_OID_base` option is removed. If an upgrade fails on an unknown option, delete that key from the add-on YAML.

## Support

In case you've found a bug, please [open an issue on GitHub][issue].

[issue]: https://github.com/iShark5060/Home-Assistant-SNMP-Sensor-Server/issues
[repository]: https://github.com/iShark5060/Home-Assistant-SNMP-Sensor-Server
