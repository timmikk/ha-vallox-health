"""Shared entity support for Vallox Extended."""

from __future__ import annotations

from homeassistant.const import CONF_HOST
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DEFAULT_NAME, DOMAIN
from .coordinator import ValloxExtendedCoordinator


class ValloxExtendedEntity(CoordinatorEntity[ValloxExtendedCoordinator]):
    """Base entity associated with the configured Vallox device."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: ValloxExtendedCoordinator, key: str) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_{key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.config_entry.entry_id)},
            manufacturer="Vallox",
            name=DEFAULT_NAME,
            configuration_url=f"http://{coordinator.config_entry.data[CONF_HOST]}",
        )
