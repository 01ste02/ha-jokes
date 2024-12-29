"""Config flow for Jokes integration."""

from .const import (
    CONF_DEVICENAME,
    CONF_NAME,
    CONF_UPDATE_INTERVAL,
    CONF_JOKE_LENGTH,
    CONF_NUM_TRIES,
    DOMAIN,
    DEFAULT_DEVICENAME,
    DEFAULT_NAME,
    DEFAULT_JOKE_LENGTH,
    DEFAULT_UPDATE_INTERVAL,
    DEFAULT_RETRIES,
)
from homeassistant.config_entries import (
    ConfigFlow,
    ConfigEntry,
    ConfigFlowResult,
    CONN_CLASS_CLOUD_POLL
)
import voluptuous as vol
from typing import Any
import logging

_LOGGER = logging.getLogger(__name__)

class JokesFlowHandler(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Jokes."""

    VERSION = 1.3
    CONNECTION_CLASS = CONN_CLASS_CLOUD_POLL

    DATA_SCHEMA = vol.Schema({
        vol.Optional(
            CONF_NAME,
            default=DEFAULT_NAME,
        ): str,
        vol.Optional(
            CONF_UPDATE_INTERVAL,
            default=DEFAULT_UPDATE_INTERVAL,
            description="Time between fetching new jokes in seconds.",
        ): int,
        vol.Optional(
            CONF_JOKE_LENGTH,
            default=DEFAULT_JOKE_LENGTH,
            description="Do not allow jokes longer than this.",
        ): int,
        vol.Optional(
            CONF_NUM_TRIES,
            default=DEFAULT_RETRIES,
            description="Number of retries at fetching a joke,",
        ): int,
        vol.Optional(
            CONF_DEVICENAME,
            default=DEFAULT_DEVICENAME,
            description="What to call the devices for this integration.",
        ): str,
    })

    _input_data: dict[str, Any]

    
    async def async_step_user(
            self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Show config Form step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=self.DATA_SCHEMA,
            )

        title = f"Random Joke - {user_input[CONF_UPDATE_INTERVAL]}s"
        await self.async_set_unique_id(title)
        self._abort_if_unique_id_configured()
        return self.async_create_entry(title=title, data=user_input)


    async def async_step_reconfigure(
            self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Add reconfigure step to allow to reconfigure a config entry."""
        config_entry = self.hass.config_entries.async_get_entry(
            self.context["entry_id"]
        )
        
        if user_input is not None:
            # Maybe validate data
            return self.async_update_reload_and_abort(
                config_entry,
                unique_id=config_entry.unique_id,
                data={**config_entry.data, **user_input},
                reason="reconfigure_successful",
            )
        
        return self.async_show_form(
            step_id="reconfigure",
            data_schema=self.DATA_SCHEMA,
        )

            
