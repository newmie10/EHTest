import aiohttp
import logging
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

_LOGGER = logging.getLogger(__name__)

DOMAIN = "eh"

CONF_EMAIL = "email"
CONF_SYSTEM_ID = "system_id"

class EffortlessConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for your integration."""

    VERSION = 1

    def __init__(self):
        """Initialize the config flow."""
        self.email = None
        self.system_id = None

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            self.email = user_input[CONF_EMAIL]
            self.system_id = user_input[CONF_SYSTEM_ID]
            # Validate the credentials
            if await self._validate_customer(self.email, self.system_id):
                return self.async_create_entry(title=self.email, data=user_input)
            else:
                errors["base"] = "invalid_auth"
        data_schema = vol.Schema(
            {
                vol.Required(CONF_EMAIL, description="Effortless Email"): str,
                vol.Required(CONF_SYSTEM_ID, description="Effortless ID"): str,
            }
        )

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )

    async def _validate_customer(self, email, system_id):
        """Validate the customer using the RESTful API."""
        url = f"https://devcust.effortlesshome.co/getcustomerbyemail/{email}"
        headers = {
            "accept": "application/json, text/html",
            "X-Custom-PSK": "665e459692f515b1528312cf-999asdfadsfkdsafadskjlfadsf",
            "eh_system_id": system_id,
            "Content-Type": "application/json; charset=utf-8",
        }

        session = async_get_clientsession(self.hass)

        try:
            async with session.post(url, headers=headers) as response:
                _LOGGER.debug("API response status: %s", response.status)
                _LOGGER.debug("API response headers: %s", response.headers)
                content = await response.text()
                _LOGGER.debug("API response content: %s", content)
                if response.status == 200:
                    result = await response.json()
                    _LOGGER.debug("API JSON response: %s", result)
                    # Check if the request was successful
                    if result.get("success", False):
                        # Check if there is at least one result
                        return len(result.get("results", [])) > 0
                else:
                    _LOGGER.error("Unexpected response status: %s", response.status)
        except aiohttp.ClientError as e:
            _LOGGER.error("API Request failed with exception: %s", e)

        return False

    async def async_setup_entry(
        hass: HomeAssistant, entry: config_entries.ConfigEntry
    ) -> bool:
        """Set up your integration from a config entry."""
        # Retrieve customer data using the stored email and system ID
        email = entry.data[CONF_EMAIL]
        system_id = entry.data[CONF_SYSTEM_ID]

        # Optionally, fetch and store additional customer info here
        # ...

        hass.data[DOMAIN] = {
            "email": email,
            "system_id": system_id,
            # Add other relevant customer info here
        }

        # Set up platforms, e.g., light, switch, etc.
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, "light"),
            hass.config_entries.async_forward_entry_setup(entry, "alarm_control_panel"),
            hass.config_entries.async_forward_entry_setup(entry, "sensor"),
             hass.config_entries.async_forward_entry_setup(entry, "customer")
            )

        return True
