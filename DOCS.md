# Home Assistant Add-on: SNMP Sensor Server

SNMP **v2c** agent for Home Assistant. Optional exposure of entity states (and host `sys*` fields) to monitors such as LibreNMS or Nagios.

64-bit Supervisor only: **aarch64** and **amd64**. Default UDP map is **161**.

## Installation

From the Supervisor add-on store, add this repository:

https://github.com/iShark5060/Home-Assistant-SNMP-Sensor-Server

Install **SNMP Sensor Server**.

## How to use

1. Set `community` (the v2c community string your monitor expects, for example `public`). Fill in the other options if you wish.
2. Set the UDP port under Network if you do not want the default `161`.
3. Save the add-on configuration.
4. Start the add-on.

The add-on talks to Home Assistant through the Supervisor API (`homeassistant_api`). Sensor exposure will not work without that.

## Configuration

Example:

```yaml
sysname: Home Assistant
community: public
location: Home
name: RPi
email: rpi@me.com
expose_sensors: true
expose_sensors_OID_base: "1.3.6.1.4.1.43.10.210."
sensors_to_expose: all
```

### Option: `community`

SNMP v2c community string the monitor must use. Default `public`.

### Option: `sysname`

`sysName` reported by snmpd. Default `Home Assistant`.

### Option: `location`

`sysLocation`. Empty by default.

### Option: `name`

Contact display name. Combined with `email` into snmpd `sysContact` as `name <email>`.

### Option: `email`

Contact email used in `sysContact` with `name`.

### Option: `expose_sensors`

When `true` (default), the add-on queries Supervisor for entity states and adds an snmpd `extend` line per matching entity. Polling an entity returns its current `state` string.

When `false`, only the host `sys*` fields above are served.

Sensor generation retries until Supervisor returns JSON. A bad API response can delay start.

### Option: `sensors_to_expose`

Whitelist of Home Assistant `entity_id` patterns, comma-separated. `*` is a wildcard. `all` or empty exposes every entity (same as 1.3.x). Spaces around commas are ignored.

Examples: `sensor.temperature_*`, `light.*,switch.office`.

### Option: `expose_sensors_OID_base`

Present in the add-on schema (default `1.3.6.1.4.1.43.10.210.`, an inherited 3Com enterprise prefix). The configurator currently **does not apply this value**. Entity OIDs come from Net-SNMP `extend` / `NET-SNMP-EXTEND-MIB::nsExtendOutput1Line."<entity_id>"`. Changing this option has no effect until that wiring exists.

## Support

In case you've found a bug, please [open an issue on GitHub][issue].

[issue]: https://github.com/iShark5060/Home-Assistant-SNMP-Sensor-Server/issues
[repository]: https://github.com/iShark5060/Home-Assistant-SNMP-Sensor-Server
