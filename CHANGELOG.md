# Changelog

All notable changes to this project will be documented in this file. Format
follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-09-26

### Added

- Initial read-only Vallox Health integration with bypass, defrost, heater,
  and fault diagnostic telemetry.
- Explicit protocol allowlist and tests preventing unapproved raw fields from
  entering coordinator state.

## [0.0.1] - 2026-09-26

- Initial scaffold via infra task #200 (`scripts/setup-ha-component-repo.sh`).
  Empty `async_setup` shell; not yet functional.
