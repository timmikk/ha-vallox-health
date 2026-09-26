"""Read-only Vallox Health binary sensors."""

from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.const import EntityCategory
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import CELL_STATE_BYPASS, CELL_STATE_DEFROSTING
from .coordinator import ValloxHealthCoordinator
from .entity import ValloxHealthEntity


class ValloxHealthBinarySensor(ValloxHealthEntity, BinarySensorEntity):
    """A binary sensor derived from a documented read-only metric."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(
        self,
        coordinator: ValloxHealthCoordinator,
        key: str,
        name: str,
        metric: str,
        expected: int,
        valid_values: frozenset[int],
    ) -> None:
        super().__init__(coordinator, key)
        self._attr_name = name
        self._metric = metric
        self._expected = expected
        self._valid_values = valid_values

    @property
    def is_on(self) -> bool | None:
        value = self.coordinator.data.get(self._metric)
        return value == self._expected if value in self._valid_values else None


async def async_setup_entry(
    _hass, entry, async_add_entities: AddConfigEntryEntitiesCallback
) -> None:
    """Set up the approved Vallox Health binary sensors."""
    coordinator: ValloxHealthCoordinator = entry.runtime_data
    async_add_entities(
        [
            ValloxHealthBinarySensor(
                coordinator,
                "bypass_active",
                "Bypass active",
                "A_CYC_CELL_STATE",
                CELL_STATE_BYPASS,
                frozenset({0, 1, CELL_STATE_BYPASS, CELL_STATE_DEFROSTING}),
            ),
            ValloxHealthBinarySensor(
                coordinator,
                "defrosting",
                "Defrosting",
                "A_CYC_CELL_STATE",
                CELL_STATE_DEFROSTING,
                frozenset({0, 1, CELL_STATE_BYPASS, CELL_STATE_DEFROSTING}),
            ),
            ValloxHealthBinarySensor(
                coordinator,
                "post_heater",
                "Post-heater active",
                "A_CYC_IO_HEATER",
                1,
                frozenset({0, 1}),
            ),
            ValloxHealthBinarySensor(
                coordinator,
                "fault_active",
                "Fault active",
                "A_CYC_FAULT_ACTIVITY",
                1,
                frozenset({0, 1}),
            ),
        ]
    )
