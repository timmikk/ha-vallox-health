"""Tests for the Vallox Health integration."""

from unittest.mock import AsyncMock, patch

import pytest
from homeassistant.config_entries import ConfigEntryState
from homeassistant.const import CONF_HOST
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.vallox_health.const import ALLOWED_METRICS, DOMAIN


def test_import():
    """The integration package can be imported."""
    from custom_components import vallox_health  # noqa: F401


def test_allowlist_contains_only_health_metrics():
    """The component's protocol boundary stays narrow and explicit."""
    assert ALLOWED_METRICS == {
        "A_CYC_CELL_STATE",
        "A_CYC_IO_HEATER",
        "A_CYC_FAULT_ACTIVITY",
        "A_CYC_FAULT_COUNT",
        "A_CYC_TOTAL_FAULT_COUNT",
    }


@pytest.mark.asyncio
async def test_setup_and_unload_filters_unapproved_metrics(hass):
    """Setup creates the platforms while coordinator data stays allowlisted."""
    client = type(
        "Client",
        (),
        {
            "fetch_metrics": AsyncMock(
                return_value={
                    "A_CYC_CELL_STATE": 2,
                    "A_CYC_IO_HEATER": 0,
                    "A_CYC_FAULT_ACTIVITY": 0,
                    "A_CYC_FAULT_COUNT": 0,
                    "A_CYC_TOTAL_FAULT_COUNT": 0,
                    "UNAPPROVED_PROTOCOL_FIELD": 1,
                }
            )
        },
    )()
    entry = MockConfigEntry(domain=DOMAIN, data={CONF_HOST: "192.0.2.1"})
    entry.add_to_hass(hass)

    with patch("custom_components.vallox_health.Vallox", return_value=client):
        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    assert entry.state is ConfigEntryState.LOADED
    coordinator = entry.runtime_data
    assert "UNAPPROVED_PROTOCOL_FIELD" not in coordinator.data
    assert set(coordinator.data) == ALLOWED_METRICS

    assert await hass.config_entries.async_unload(entry.entry_id)
    await hass.async_block_till_done()
    assert entry.state is ConfigEntryState.NOT_LOADED
