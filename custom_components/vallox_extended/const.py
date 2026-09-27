"""Constants for Vallox Extended.

The cell-state mapping is derived from Home Assistant's core Vallox
integration (Apache-2.0); only the read-only subset needed here is retained.
"""

from datetime import timedelta

DOMAIN = "vallox_extended"
DEFAULT_NAME = "Vallox Extended"
STATE_SCAN_INTERVAL = timedelta(seconds=60)

CELL_STATE_BYPASS = 2
CELL_STATE_DEFROSTING = 3

# This is deliberately a narrow allowlist. Raw Vallox responses include
# configuration and credential-bearing values and must never be exposed.
ALLOWED_METRICS = frozenset(
    {
        "A_CYC_CELL_STATE",
        "A_CYC_IO_HEATER",
        "A_CYC_FAULT_ACTIVITY",
        "A_CYC_FAULT_COUNT",
        "A_CYC_TOTAL_FAULT_COUNT",
    }
)
