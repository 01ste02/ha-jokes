"""Provides random jokes."""

from .const import DOMAIN
import aiohttp
import asyncio
from datetime import timedelta
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback, HomeAssistant
from homeassistant.const import Platform
from homeassistant.helpers.discovery import async_load_platform
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
import logging

_LOGGER = logging.getLogger(__name__)

# def set_joke(hass: HomeAssistant, text: str):
#     """Helper function to set the random joke."""
#     _LOGGER.debug("set_joke")
#     hass.states.async_set("jokes.random_joke", text)

def setup(hass: HomeAssistant, config: dict):
    """This setup does nothing, we use the async setup."""
    _LOGGER.debug("setup")
    return True

async def async_setup(hass: HomeAssistant, config: dict):
    """Setup from configuration.yaml."""
    _LOGGER.debug("async_setup")
    
    #`config` is the full dict from `configuration.yaml`.
    #set_joke(hass, "")

    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Setup from Config Flow Result."""
    _LOGGER.debug("async_setup_entry")
    
    coordinator = JokeUpdateCoordinator(
        hass,
        _LOGGER,
        entry,
        update_interval=timedelta(seconds=entry.data["update_interval"])
    )
    await coordinator.async_refresh()
    
    hass.data[DOMAIN] = {
        "coordinator": coordinator,
        "config": entry,
    }
    
    await hass.config_entries.async_forward_entry_setups(entry, Platform.SENSOR)
    entry.async_on_unload(entry.add_update_listener(update_listener))
    
    return True

async def update_listener(hass: HomeAssistant, config_entry: ConfigEntry) -> None:
    """Handle options update."""
    await hass.config_entries.async_reload(config_entry.entry_id)

class JokeUpdateCoordinator(DataUpdateCoordinator):
    """Update handler."""

    def __init__(self, hass, logger, entry, update_interval=None):
        """Initialize global data updater."""
        logger.debug("__init__")

        self._attr_unique_id = "joke" + entry.entry_id + "_" + entry.title
        self._name = entry.title

        super().__init__(
            hass,
            logger,
            name=DOMAIN,
            update_interval=update_interval,
            update_method=self._async_update_data,
        )
        
    async def _async_update_data(self):
        """Fetch a random joke."""
        self.logger.debug("_async_update_data")
        
        #get a random joke (finally)
        try:
            headers = {
                'Accept': 'application/json',
                'User-Agent': 'Jokes custom integration for Home Assistant (https://github.com/LaggAt/ha-jokes)'
            }
            async with aiohttp.ClientSession() as session:
                for _ in range(0, 10):
                    async with session.get(
                            'https://icanhazdadjoke.com/',
                            headers=headers
                    ) as resp:
                        if resp.status == 200:
                            json = await resp.json()
                            if "joke" not in json or len(json["joke"]) > 255:
                                continue
                            # return the joke object
                            return json
                        else:
                            raise UpdateFailed(f"Response status code: {resp.status}")
                raise UpdateFailed(f"Could not get joke after 10 tries")
        except Exception as ex:
            raise UpdateFailed from ex


async def async_migrate_entry(hass, config_entry: ConfigEntry):
    """Migrate old entry."""
    # From home assistant developer documentation
    _LOGGER.debug("Migrating configuration from version %s.%s",
                  config_entry.version,
                  config_entry.minor_version
                  )

    if config_entry.version > 1:
        # This means the user has downgraded from a future version
        return False

    if config_entry.version == 1:
        new_data = {**config_entry.data}
        if config_entry.minor_version < 1:
            new_data["name"] = DEFAULT_NAME
            new_data["update_interval"] = DEFAULT_UPDATE_INTERVAL
            new_data["joke_length"] = DEFAULT_JOKE_LENGTH

            hass.config_entries.async_update_entry(
                config_entry,
                data=new_data,
                minor_version=1,
                version=1
            )

    _LOGGER.debug("Migration to configuration version %s.%s successful",
                  config_entry.version,
                  config_entry.minor_version)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, DOMAIN)

    # Pop add-on data
    hass.data.pop(DOMAIN, None)

    return unload_ok
