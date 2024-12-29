"""Joke Sensor."""

from .const import DOMAIN
from homeassistant import core
from homeassistant.helpers.update_coordinator import CoordinatorEntity, DataUpdateCoordinator

async def async_setup_platform(
    hass: core.HomeAssistant, config, async_add_entities, discovery_info=None
):
    """Setup the sensor platform."""
    coordinator = hass.data[DOMAIN]["coordinator"]
    async_add_entities([JokeEntity(coordinator)], True)

class JokeEntity(CoordinatorEntity):
    """Dummy entity to trigger updates."""

    _attr_icon = "mdi:emoticon-excited-outline"

    def __init__(self, coordinator: DataUpdateCoordinator):
        """Pass coordinator to CoordinatorEntity."""
        super().__init__(coordinator)
        self._name = "sensor.random_joke"
        self._attr_name = "Random Joke"

    @property
    def unique_id(self) -> str:
        """Return the unique ID of the sensor."""
        return self.coordinator._attr_unique_id

    @property
    def entity_id(self):
        """Return the entity id of the sensor."""
        return self._name

    @entity_id.setter
    def entity_id(self, value):
        """Sets the entity id of the sensor."""
        self._name = value

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._attr_name

    @name.setter
    def name(self, value):
        """Sets the name of the sensor."""
        self._attr_name = value

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.data["joke"]

    @property
    def extra_state_attributes(self):
        return self.coordinator.data
