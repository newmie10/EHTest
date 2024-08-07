"""The effortlesshome integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .oauth import OAuthView

# # TODO List the platforms that you want to support.
# # For your initial PR, limit it to 1 platform.
# PLATFORMS: list[Platform] = [Platform.LIGHT]

# # TODO Create ConfigEntry type alias with API object
# # TODO Rename type alias and update all entry annotations
# type New_NameConfigEntry = ConfigEntry[MyApi]  # noqa: F821


# # TODO Update entry annotation
# async def async_setup_entry(hass: HomeAssistant, entry: New_NameConfigEntry) -> bool:
#     """Set up effortlesshome from a config entry."""

#     # TODO 1. Create API instance
#     # TODO 2. Validate the API connection (and authentication)
#     # TODO 3. Store an API object for your platforms to access
#     # entry.runtime_data = MyAPI(...)

#     await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

#     return True


# # TODO Update entry annotation
# async def async_unload_entry(hass: HomeAssistant, entry: New_NameConfigEntry) -> bool:
#     """Unload a config entry."""
#     return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_setup(hass: HomeAssistant, config: dict):
    hass.http.register_view(OAuthView)
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    # Set up your integration using the config entry
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    # Unload your integration
    return True
