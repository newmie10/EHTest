# Effortlesshome.py
import json
import logging
from typing import Any
import os

from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.exceptions import HomeAssistantError
from .const import DOMAIN, CONF_HOST, CONF_USERNAME, CONF_PASSWORD

_LOGGER = logging.getLogger(__name__)

CREDENTIALS_FILE = "effortlesshome_credentials.json"


class EffortlessHomeHub:
    """Class to handle authentication and communication with EffortlessHome."""

    def __init__(self, host: str) -> None:
        """Initialize."""
        self.host = host
        self.credentials = self._load_credentials()

    def _load_credentials(self) -> dict[str, str]:
        """Load credentials from the JSON file."""
        if not os.path.exists(CREDENTIALS_FILE):
            return {}
        with open(CREDENTIALS_FILE, "r") as file:
            return json.load(file)

    def _save_credentials(self) -> None:
        """Save credentials to the JSON file."""
        with open(CREDENTIALS_FILE, "w") as file:
            json.dump(self.credentials, file)

    def add_user(self, username: str, password: str) -> None:
        """Add a user to the credentials file."""
        self.credentials[username] = password
        self._save_credentials()

    async def authenticate(self, username: str, password: str) -> bool:
        """Authenticate with the EffortlessHome server."""
        # Check if the username exists and the password matches
        stored_password = self.credentials.get(username)
        if stored_password and stored_password == password:
            return True
        return False


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect."""
    hub = EffortlessHomeHub(data[CONF_HOST])

    if not await hub.authenticate(data[CONF_USERNAME], data[CONF_PASSWORD]):
        raise InvalidAuth

    return {"title": "EffortlessHome Device"}


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""
