import logging
import aiohttp
from homeassistant.components.alarm_control_panel import AlarmControlPanelEntity, AlarmControlPanelEntityFeature
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_NAME,
    STATE_ALARM_ARMED_AWAY,
    STATE_ALARM_ARMED_HOME,
    STATE_ALARM_DISARMED,
    STATE_ALARM_TRIGGERED,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, CONF_SYSTEM_ID

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """Set up the alarm control panel platform."""
    config = entry.data
    async_add_entities([EffortlessHomeAlarm(config, hass)])


class EffortlessHomeAlarm(AlarmControlPanelEntity):
    """Representation of an Effortless Home Alarm."""

    def __init__(self, config, hass: HomeAssistant):
        """Initialize the alarm control panel."""
        self._name = config.get(CONF_NAME, "Effortless Home Alarm")
        self._state = STATE_ALARM_DISARMED
        self._config = config
        self.hass = hass
        self._attr_supported_features = AlarmControlPanelEntityFeature.ARM_HOME | AlarmControlPanelEntityFeature.ARM_AWAY

    @property
    def name(self):
        """Return the name of the device."""
        return self._name

    @property
    def state(self):
        """Return the state of the device."""
        return self._state

    async def async_alarm_disarm(self, code=None):
        """Send disarm command."""
        _LOGGER.info("Disarming the alarm.")
        self._state = STATE_ALARM_DISARMED
        self.async_write_ha_state()

    async def async_alarm_arm_home(self, code=None):
        """Send arm home command."""
        _LOGGER.info("Arming the alarm in home mode.")
        self._state = STATE_ALARM_ARMED_HOME
        self.async_write_ha_state()

    async def async_alarm_arm_away(self, code=None):
        """Send arm away command."""
        _LOGGER.info("Arming the alarm in away mode.")
        self._state = STATE_ALARM_ARMED_AWAY
        self.async_write_ha_state()

    async def async_trigger(self, **kwargs):
        """Trigger the alarm and call the API."""
        _LOGGER.info("Triggering the alarm.")
        self._state = STATE_ALARM_TRIGGERED
        await self._call_create_alarm_api()
        self.async_write_ha_state()

    async def _call_create_alarm_api(self):
        """Call the API to create an alarm."""
        url = "https://dev.effortlesshome.co/createalarm/0"
        headers = {
            "accept": "application/json, text/html",
            "X-Custom-PSK": "665e459692f515b1528312cf-999asdfadsfkdsafadskjlfadsf",
            "eh_system_id": self._config[CONF_SYSTEM_ID],
            "Content-Type": "application/json; charset=utf-8",
        }
        payload = {
            "location": self._config.get("address_json"),
            "workflow": self._config.get("workflow"),
            "meta": self._config.get("meta"),
            "services": self._config.get("services"),
            "name": self._config.get("customer_name"),
            "phone": self._config.get("customer_phone"),
            "pin": self._config.get("alarm_pin"),
            "instructions": self._config.get("instructions_json"),
        }

        _LOGGER.info("Calling create alarm API with payload: %s", payload)

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, headers=headers, json=payload) as response:
                    _LOGGER.debug("API response status: %s", response.status)
                    _LOGGER.debug("API response headers: %s", response.headers)
                    content = await response.text()
                    _LOGGER.debug("API response content: %s", content)
                    if response.status == 200:
                        _LOGGER.info("Alarm successfully created.")
                    else:
                        _LOGGER.error("Failed to create alarm: %s", content)
            except aiohttp.ClientError as e:
                _LOGGER.error("API Request failed with exception: %s", e)
