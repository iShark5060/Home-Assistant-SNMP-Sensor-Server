# Changelog

## 1.0

- Initial release

## 1.6

- `snmp_version` selects off, v2c, v3, or v2c+v3. SNMPv3 is SHA-256 auth and AES-128 privacy.
- SNMPv3 username is `v3_username` (any letters, numbers, `.`, `_`, `-`). Users are created in snmpd's persistent store while the daemon is stopped, which is required for `createUser` to stick.
- Removed unused `expose_sensors_OID_base`. Entity OIDs are `NET-SNMP-EXTEND-MIB::nsExtendOutput1Line."<entity_id>"`. Delete the old key from saved add-on YAML if start fails after upgrade.
- `py3-requests` is in the image. Supervisor fetch at start is capped at 12 attempts. Entity polls print `unavailable` instead of crashing the extend.

## 1.5

- updated names and variables to conform with pyLint
- updated to work with current HAOS version