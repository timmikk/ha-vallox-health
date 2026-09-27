"""Read-only Vallox Extended numeric sensors."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.const import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .coordinator import ValloxExtendedCoordinator
from .entity import ValloxExtendedEntity


class ValloxExtendedFaultCountSensor(ValloxExtendedEntity, SensorEntity):
    """Expose a read-only Vallox fault counter."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_native_unit_of_measurement = "faults"

    def __init__(
        self,
        coordinator: ValloxExtendedCoordinator,
        key: str,
        name: str,
        metric: str,
        total_increasing: bool = False,
    ) -> None:
        super().__init__(coordinator, key)
        self._attr_name = name
        self._metric = metric
        if total_increasing:
            self._attr_state_class = SensorStateClass.TOTAL_INCREASING

    @property
    def native_value(self) -> int | float | None:
        return self.coordinator.data.get(self._metric)


async def async_setup_entry(
    _hass, entry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the approved Vallox Extended fault counters."""
    coordinator: ValloxExtendedCoordinator = entry.runtime_data
    async_add_entities(
        [
            ValloxExtendedFaultCountSensor(
                coordinator,
                "current_fault_count",
                "Current fault count",
                "A_CYC_FAULT_COUNT",
            ),
            ValloxExtendedFaultCountSensor(
                coordinator,
                "total_fault_count",
                "Total fault count",
                "A_CYC_TOTAL_FAULT_COUNT",
                total_increasing=True,
            ),
        ]
    )
