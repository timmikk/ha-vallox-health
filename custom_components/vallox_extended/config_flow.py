"""Config flow for vallox_extended."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_HOST
from homeassistant.util.network import is_ip_address
from vallox_websocket_api import Vallox, ValloxApiException

from .const import DEFAULT_NAME, DOMAIN

_LOGGER = logging.getLogger(__name__)
CONFIG_SCHEMA = vol.Schema({vol.Required(CONF_HOST): str})


class ValloxExtendedConfigFlow(ConfigFlow, domain=DOMAIN):
    """Configure an extended read-only Vallox connection."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial setup flow."""
        if user_input is None:
            return self.async_show_form(step_id="user", data_schema=CONFIG_SCHEMA)

        host = user_input[CONF_HOST]
        errors: dict[str, str] = {}
        if not is_ip_address(host):
            errors[CONF_HOST] = "invalid_host"
        else:
            self._async_abort_entries_match({CONF_HOST: host})
            try:
                await Vallox(host).fetch_metric_data()
            except ValloxApiException:
                errors["base"] = "cannot_connect"
            except Exception:  # The device protocol must not leak into logs.
                _LOGGER.exception("Unexpected Vallox Extended connection failure")
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(title=DEFAULT_NAME, data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=self.add_suggested_values_to_schema(
                CONFIG_SCHEMA, {CONF_HOST: host}
            ),
            errors=errors,
        )
