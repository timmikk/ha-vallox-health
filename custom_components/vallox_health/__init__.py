"""Read-only Vallox health telemetry."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from vallox_websocket_api import Vallox

from .const import DOMAIN
from .coordinator import ValloxHealthCoordinator

# Config-flow-only integration; hassfest requires this declaration for any
# integration that implements async_setup.
CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the vallox_health integration from YAML (unused — config flow only)."""
    return True


PLATFORMS = [Platform.BINARY_SENSOR, Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up vallox_health from a config entry."""
    coordinator = ValloxHealthCoordinator(
        hass, entry, Vallox(entry.data[CONF_HOST])
    )
    await coordinator.async_config_entry_first_refresh()
    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
