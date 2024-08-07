# OAuth request handling

import logging

import aiohttp

from homeassistant.components.http import HomeAssistantView

_LOGGER = logging.getLogger(__name__)


class OAuthView(HomeAssistantView):
    url = "/auth/external/callback"
    name = "auth:external:callback"
    requires_auth = False

    async def get(self, request):
        hass = request.app["hass"]
        # Handle the OAuth callback here
        return aiohttp.web.Response(text="OAuth callback received")
