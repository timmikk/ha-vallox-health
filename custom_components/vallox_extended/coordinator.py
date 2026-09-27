"""Read-only polling coordinator for Vallox Extended."""

from __future__ import annotations

import logging
from collections.abc import Mapping

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from vallox_websocket_api import Vallox, ValloxApiException

from .const import ALLOWED_METRICS, DOMAIN, STATE_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)


class ValloxExtendedCoordinator(DataUpdateCoordinator[Mapping[str, int | float | None]]):
    """Fetch and retain only the explicitly approved Vallox metrics."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry, client: Vallox) -> None:
        super().__init__(
            hass,
            _LOGGER,
            config_entry=entry,
            name=f"{DOMAIN} data coordinator",
            update_interval=STATE_SCAN_INTERVAL,
        )
        self.client = client

    async def _async_update_data(self) -> Mapping[str, int | float | None]:
        try:
            data = await self.client.fetch_metrics()
        except ValloxApiException as err:
            raise UpdateFailed("Unable to refresh Vallox Extended metrics") from err
        return {key: data.get(key) for key in ALLOWED_METRICS}
