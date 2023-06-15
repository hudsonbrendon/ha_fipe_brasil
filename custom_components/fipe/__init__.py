import logging
from typing import Optional, Union

import requests
from homeassistant import config_entries, core
from homeassistant.const import Platform
from homeassistant.exceptions import ConfigEntryAuthFailed
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from .const import BASE_URL, CONF_CODIGO_FIPE, CONF_MODELO, DOMAIN

PLATFORMS = [Platform.SENSOR]

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: core.HomeAssistant, entry: config_entries.ConfigEntry
):
    if await get_prices(hass=hass, codigo_fipe=entry.data.get(CONF_CODIGO_FIPE)):
        hass.data.setdefault(DOMAIN, {})
        hass.data[DOMAIN][entry.entry_id] = entry.data

        for platform in PLATFORMS:
            hass.async_create_task(
                hass.config_entries.async_forward_entry_setup(entry, platform)
            )
    else:
        raise ConfigEntryAuthFailed("Invalid credentials")
    return True


async def async_unload_entry(
    hass: core.HomeAssistant, entry: config_entries.ConfigEntry
) -> bool:
    """Unload a config entry."""

    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok


async def async_migrate_entry(
    hass: core.HomeAssistant, config_entry: config_entries.ConfigEntry
):
    hass.config_entries.async_update_entry(
        config_entry,
        data={
            CONF_CODIGO_FIPE: config_entry.data.get(CONF_CODIGO_FIPE),
            CONF_MODELO: config_entry.data.get(CONF_MODELO)
        },
    )

    return True


async def get_prices(hass, codigo_fipe: str) -> Union[dict, Optional[None]]:
    def get():
        url = f"{BASE_URL}{codigo_fipe}"
        retry_strategy = Retry(
            total=3,
            status_forcelist=[400, 401, 500, 502, 503, 504],
            allowed_methods=["GET"],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        http = requests.Session()
        http.mount("https://", adapter)

        return http.get(url, headers={"User-Agent": "Mozilla/5.0"})

    response = await hass.async_add_executor_job(get)
    _LOGGER.debug("API Response prices: %s", response.json())

    if response.ok:
        return response.json()
    return None
