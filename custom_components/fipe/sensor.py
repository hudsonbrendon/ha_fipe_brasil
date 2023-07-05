import logging
from typing import List

import homeassistant.helpers.config_validation as cv
import requests
import voluptuous as vol
from aiohttp import ClientSession
from homeassistant import config_entries, const, core
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity import Entity
from homeassistant.util.dt import utc_from_timestamp
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from .const import (
    BASE_URL,
    CONF_CODIGO_FIPE,
    CONF_MODELO,
    DOMAIN,
    ICON,
    SCAN_INTERVAL,
)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_MODELO): cv.string,
        vol.Required(CONF_CODIGO_FIPE): cv.string,
    }
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: core.HomeAssistant,
    config_entry: config_entries.ConfigEntry,
    async_add_entities,
) -> None:
    """Setup sensor platform."""
    config = hass.data[DOMAIN][config_entry.entry_id]

    session = async_get_clientsession(hass)
    sensors = [
        FIPESensor(
            modelo=config[CONF_MODELO],
            codigo_fipe=config[CONF_CODIGO_FIPE],
            session=session,
        )
    ]
    async_add_entities(sensors, update_before_add=True)


class FIPESensor(Entity):
    """Ingresso.com Sensor class"""

    def __init__(
        self,
        modelo: str,
        codigo_fipe: str,
        session: ClientSession,
    ) -> None:
        self._state = None
        self._codigo_fipe = codigo_fipe
        self.session = session
        self._modelo = modelo.capitalize()
        self._prices = []
        self._last_updated = const.STATE_UNKNOWN

    @property
    def modelo(self) -> str:
        return self._modelo

    @property
    def codigo_fipe(self) -> str:
        return self._codigo_fipe

    @property
    def name(self) -> str:
        """Name."""
        return f"{self.modelo}"

    @property
    def state(self) -> str:
        """State."""
        return len(self.prices)

    @property
    def last_updated(self):
        """Returns date when it was last updated."""
        if self._last_updated != "unknown":
            stamp = float(self._last_updated)
            return utc_from_timestamp(int(stamp))

    @property
    def prices(self) -> List[dict]:
        """Movies."""
        return self._prices

    @property
    def icon(self) -> str:
        """Icon."""
        return ICON

    @property
    def extra_state_attributes(self) -> dict:
        """Attributes."""
        return {
            "data": self.prices,
        }

    def update(self) -> None:
        """Update sensor."""
        _LOGGER.debug("%s - Running update", self.name)
        url = f"{BASE_URL}{self.codigo_fipe}"

        retry_strategy = Retry(
            total=3,
            status_forcelist=[400, 401, 500, 502, 503, 504],
            allowed_methods=["GET"],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        http = requests.Session()
        http.mount("https://", adapter)

        prices = http.get(url, headers={"User-Agent": "Mozilla/5.0"})

        if prices.ok:
            self._prices.clear()
            self._prices.extend(
                [
                    dict(
                        modelo=price.get("modelo", "Não informado"),
                        valor=price.get("valor", "Não informado"),
                        marca=price.get("marca", "Não informado"),
                        anoModelo=price.get("anoModelo", "Não informado"),
                        combustivel=price.get("combustivel", "Não informado"),
                        codigoFipe=price.get("codigoFipe", "Não informado"),
                        mesReferencia=price.get("mesReferencia", "Não informado"),
                        tipoVeiculo=price.get("tipoVeiculo", "Não informado"),
                        siglaCombustivel=price.get("siglaCombustivel", "Não informado"),
                        dataConsulta=price.get("dataConsulta", "Não informado"),
                    )
                    for price in prices.json()
                ]
            )
            _LOGGER.debug("Payload received: %s", prices.json())
        else:
            _LOGGER.debug("Error received: %s", prices.content)
