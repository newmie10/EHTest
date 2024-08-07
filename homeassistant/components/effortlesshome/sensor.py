import aiohttp
import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """Set up the sensor platform."""
    config = entry.data
    async_add_entities([EffortlessHomeCustomerSensor(config, hass)])


class EffortlessHomeCustomerSensor(SensorEntity):
    """Representation of an Effortless Home Customer Sensor."""

    def __init__(self, config, hass: HomeAssistant):
        """Initialize the sensor."""
        self._name = config.get(CONF_NAME, "Effortless Home Customer")
        self._state = None
        self._attributes = {}
        self._config = config
        self.hass = hass

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return self._attributes

    async def async_update(self):
        """Fetch new state data for the sensor."""
        await self._fetch_customer_data()

    async def _fetch_customer_data(self):
        """Fetch customer data from the API."""
        url = "https://devcust.effortlesshome.co/getcustomerbyid/0"
        headers = {
            "accept": "application/json, text/html",
            "X-Custom-PSK": self._config.get("security_monitoring_secret"),
            "eh_system_id": self._config.get("eh_system_id"),
            "eh_customer_id": self._config.get("eh_customer_id"),
            "Content-Type": "application/json; charset=utf-8",
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, headers=headers) as response:
                    _LOGGER.debug("API response status: %s", response.status)
                    content = await response.json()
                    _LOGGER.debug("API response content: %s", content)
                    if response.status == 200 and "results" in content:
                        self._state = content["results"].get("name", "Unknown")
                        self._attributes = content["results"]
                    else:
                        _LOGGER.error("Failed to fetch customer data: %s", content)
            except aiohttp.ClientError as e:
                _LOGGER.error("API Request failed with exception: %s", e)
