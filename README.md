# ha-vallox-extended

Extended read-only Vallox telemetry

Home Assistant custom integration. Development happens on
[git.clo.dy.fi/timo/ha-vallox-extended](https://git.clo.dy.fi/timo/ha-vallox-extended);
the public GitHub mirror at
[timmikk/ha-vallox-extended](https://github.com/timmikk/ha-vallox-extended) is
HACS-installable. See `info.md` for install/rollback instructions.

## Development

- Component code lives in `custom_components/vallox_extended/`.
- Tests: `pytest` (uses `pytest-homeassistant-custom-component`).
- CI: `.forgejo/workflows/ci.yml` runs `hassfest` + `hacs/action` + pytest.
- Release: tag `vX.Y.Z` on Forgejo → mirror syncs → HACS offers the version
  in the UI. A GitHub Release object is not needed.

## Supported telemetry

Version 0.1.1 is intentionally a small diagnostic surface: bypass state,
defrosting, post-heater state, active-fault indication, and current/total
fault counters. It has no writable entities or services.

The component accepts only an explicit allowlist of protocol metric keys. It
does not retain or expose raw device responses: Vallox protocol responses can
include configuration and credential-bearing fields. Metrics whose polarity,
unit, or availability is not confirmed are left out rather than guessed.

This component is separate from Home Assistant's core `vallox` integration.
Keep the core integration installed for its existing fan controls and
automations; configure Vallox Extended with the same device IP only after its
HACS release is installed.

## Secrets policy

This repo is **public**. Never commit tokens, passwords, or personal data.
Home Assistant fills those at runtime from `configuration.yaml`, config-flow
options, or `secrets.yaml` on the host — none of that touches this repo.

## Pipeline

See [`docs/ha-custom-components.md`](https://git.clo.dy.fi/timo/infra/src/branch/main/docs/ha-custom-components.md)
in the infra repo for the full pipeline (Forgejo primary + public GitHub
mirror + HACS registration + release/rollback flow).
