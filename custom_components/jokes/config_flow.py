"""Config flow for Jokes integration."""

from .const import DOMAIN, DEFAULT_NAME, DEFAULT_JOKE_LENGTH, DEFAULT_UPDATE_INTERVAL
from homeassistant import config_entries
import voluptuous as vol
from typing import Any

@config_entries.HANDLERS.register(DOMAIN)
class JokesFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Jokes."""

    VERSION = 1.2
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    DATA_SCHEMA = vol.Schema({
        vol.Optional(
            "name",
            default=DEFAULT_NAME,
        ): str,
        vol.Optional(
            "update_interval",
            default=DEFAULT_UPDATE_INTERVAL,
            description="Time between fetching new jokes.",
        ): int,
        vol.Optional(
            "joke_length",
            default=DEFAULT_JOKE_LENGTH,
            description="Do not allow jokes longer than this.",
        ): int,
    })
    
    async def async_step_user(self, user_input: dict[str, Any] | None = None):
        """Show config Form step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=DATA_SCHEMA,
            )
        else:
            if len(user_input["name"]) > 0:
                name = user_input["name"]
            else:
                name = DEFAULT_NAME

            return self.async_create_entry(
                title=name,
                data=user_input,
            )

    async def async_step_reconfigure(self, user_input: dict[str, Any] | None = None):
        """Show config Form step."""
        if user_input is None:

            return self.async_show_form(
                step_id="reconfigure",
                data_schema=DATA_SCHEMA,
            )
        else:
            if len(user_input["name"]) > 0:
                name = user_input["name"]
            else:
                name = DEFAULT_NAME

            return self.async_create_entry(
                title=name,
                data=user_input,
            )
