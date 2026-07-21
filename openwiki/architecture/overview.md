---
type: Architecture Overview
title: Add-on layout
description: Dockerfile, config.json, and data scripts for the SNMP agent.
tags: [architecture]
timestamp: 2026-07-21T00:00:00Z
---

# Add-on layout

- `config.json` — add-on manifest (arch: aarch64 / amd64)
- `Dockerfile` — container image
- `data/run.sh` — entrypoint
- `data/snmpd_configurator.py` / `get_sensor_data.py` — SNMP / sensor plumbing
- `DOCS.md` — user-facing options
