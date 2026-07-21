---
type: Operations
title: CI and PR checks
description: Python compile and Docker build on ubuntu-latest.
tags: [operations, ci]
timestamp: 2026-07-21T00:00:00Z
---

# CI and PR checks

`pr.yml` / `ci.yml` run `bash scripts/validate` on `ubuntu-latest` with `actions/checkout@v7`.
