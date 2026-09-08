#!/usr/bin/with-contenv bashio

bashio::log.info "Preparing SNMP Sensor Server, please wait.."
CONFIG="/etc/snmp/snmpd.conf"
PERSIST_DIR="/data/net-snmp"
PERSIST_FILE="${PERSIST_DIR}/snmpd.conf"

SNMP_VERSION="$(bashio::config 'snmp_version')"
ENABLE_V2C=false
ENABLE_V3=false
case "${SNMP_VERSION}" in
	off) ;;
	v2c) ENABLE_V2C=true ;;
	v3) ENABLE_V3=true ;;
	v2c+v3)
		ENABLE_V2C=true
		ENABLE_V3=true
		;;
	*)
		bashio::log.fatal "Unknown snmp_version '${SNMP_VERSION}'. Use off, v2c, v3, or v2c+v3."
		exit 1
		;;
esac

if [ "${SNMP_VERSION}" = "off" ]; then
	bashio::log.info "SNMP access is off; not starting snmpd."
	exec sh -c 'while true; do sleep 86400; done'
fi

# snmpd keeps USM users and engine ID in its persistent dir. Put that on
# /data so a container recreate does not mint a new engine ID.
mkdir -p "${PERSIST_DIR}" /var/lib
if [ -e /var/lib/net-snmp ] && [ ! -L /var/lib/net-snmp ]; then
	rm -rf /var/lib/net-snmp
fi
ln -sfn "${PERSIST_DIR}" /var/lib/net-snmp

V3_USER="$(bashio::config 'v3_username')"
if [ "${ENABLE_V2C}" = true ]; then
	COMMUNITY="$(bashio::config 'community')"
	if [ -z "${COMMUNITY}" ]; then
		bashio::log.fatal "snmp_version includes v2c but community is empty."
		exit 1
	fi
fi
if [ "${ENABLE_V3}" = true ]; then
	V3_AUTH="$(bashio::config 'v3_auth_passphrase')"
	V3_PRIV="$(bashio::config 'v3_priv_passphrase')"
	if [ -z "${V3_USER}" ] || [ -z "${V3_AUTH}" ] || [ -z "${V3_PRIV}" ]; then
		bashio::log.fatal "snmp_version includes v3 but username or passphrases are empty."
		exit 1
	fi
	case "${V3_USER}" in
		*[!A-Za-z0-9._-]*)
			bashio::log.fatal "SNMPv3 username may only contain letters, numbers, dot, underscore, or hyphen."
			exit 1
			;;
	esac
	if [ "${#V3_AUTH}" -lt 8 ] || [ "${#V3_PRIV}" -lt 8 ]; then
		bashio::log.fatal "SNMPv3 passphrases must be at least 8 characters."
		exit 1
	fi
fi

{
	echo "sysname $(bashio::config 'sysname')"
	echo "syslocation $(bashio::config 'location')"
	echo "syscontact $(bashio::config 'name') <$(bashio::config 'email')>"
	echo "view all included .1 80"
	if [ "${ENABLE_V2C}" = true ]; then
		echo "com2sec readonly default ${COMMUNITY}"
		echo "group MyROGroup v2c readonly"
		echo "access MyROGroup ''      any       noauth    exact  all    none   none"
	fi
	if [ "${ENABLE_V3}" = true ]; then
		echo "rouser ${V3_USER} priv"
	fi
} > "${CONFIG}"

# createUser belongs in the persistent file, and only while snmpd is
# stopped. On shutdown snmpd rewrites that file from memory; a line
# added while it is running is thrown away. This script is PID 1 and
# has not started snmpd yet. Drop any prior usmUser/createUser so a
# username or passphrase change in the add-on options takes effect.
if [ "${ENABLE_V3}" = true ]; then
	bashio::log.info "Creating SNMPv3 user ${V3_USER} (SHA-256 / AES-128)"
	touch "${PERSIST_FILE}"
	grep -v -E '^(createUser|usmUser)([[:space:]]|$)' "${PERSIST_FILE}" > "${PERSIST_FILE}.tmp" || true
	mv "${PERSIST_FILE}.tmp" "${PERSIST_FILE}"
	V3_AUTH_ESC="${V3_AUTH//\\/\\\\}"
	V3_AUTH_ESC="${V3_AUTH_ESC//\"/\\\"}"
	V3_PRIV_ESC="${V3_PRIV//\\/\\\\}"
	V3_PRIV_ESC="${V3_PRIV_ESC//\"/\\\"}"
	printf '%s\n' "createUser ${V3_USER} SHA-256 \"${V3_AUTH_ESC}\" AES \"${V3_PRIV_ESC}\"" >> "${PERSIST_FILE}"
fi

if bashio::var.true "$(bashio::config 'expose_sensors')"; then
	bashio::log.info "Generating OID for HA entities.."
	if ! OUTPUT=$(python3 /snmpd_configurator.py "${CONFIG}" "$(bashio::config 'sensors_to_expose')"); then
		bashio::log.fatal "Failed to generate entity extend lines."
		exit 1
	fi
	bashio::log.info "${OUTPUT}"
fi

bashio::log.info "Listening SNMP Sensor Server (${SNMP_VERSION})..."
exec /usr/sbin/snmpd \
	-c "${CONFIG}" \
	-f \
	< /dev/null
