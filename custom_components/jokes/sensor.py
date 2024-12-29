"""Joke Sensor."""

from .const import DOMAIN
from homeassistant import core
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import CoordinatorEntity, DataUpdateCoordinator

async def async_setup_platform(
    hass: core.HomeAssistant, config, async_add_entities, discovery_info=None
):
    """Setup the sensor platform."""
    coordinator = hass.data[DOMAIN]["coordinator"]
    config_entry = hass.data[DOMAIN]["config"]
    async_add_entities([JokeEntity(coordinator, config_entry)], True)

class JokeEntity(CoordinatorEntity):
    """Dummy entity to trigger updates."""

    _attr_icon = "mdi:emoticon-excited-outline"

    def __init__(self, coordinator: DataUpdateCoordinator, config: ConfigEntry):
        """Pass coordinator to CoordinatorEntity."""
        super().__init__(coordinator)
        self._name = "sensor.random_joke"
        self.config = config

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
        return self.config.data["name"]

    @name.setter
    def name(self, value):
        """Sets the name of the sensor."""
        self.config.data["name"] = value

    @property
    def state(self):
        """Return the state of the sensor."""
        # Cut off joke at joke_length chars... Full joke exists in extra attributes
        return self.coordinator.data["joke"][:self.config["joke_length"]]

    @property
    def extra_state_attributes(self):
        return self.coordinator.data
