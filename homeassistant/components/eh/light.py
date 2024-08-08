from homeassistant.components.light import LightEntity  # noqa: D100
from homeassistant.const import CONF_NAME


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the light platform."""
    # Example of setting up light entities
    config = entry.data
    hass.data.setdefault("eh", {})
    hass.data["eh"]["lights"] = []

    # Add a light entity
    light = ExampleLight(config)
    hass.data["eh"]["lights"].append(light)
    async_add_entities([light])

    return True


class ExampleLight(LightEntity):
    """Example implementation of a light entity."""

    def __init__(self, config):
        """Initialize the light."""
        self._name = config.get(CONF_NAME, "Example Light")
        self._state = False

    @property
    def name(self):
        """Return the name of the light."""
        return self._name

    @property
    def is_on(self):
        """Return True if the light is on."""
        return self._state

    async def async_turn_on(self, **kwargs):
        """Turn on the light."""
        self._state = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        """Turn off the light."""
        self._state = False
        self.async_write_ha_state()

    @property
    def supported_features(self):
        """Return the supported features."""
        return 0
