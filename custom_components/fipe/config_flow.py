import voluptuous as vol
from homeassistant import config_entries

from . import get_prices
from .const import CONF_CODIGO_FIPE, CONF_MODELO, DOMAIN

DATA_SCHEMA: vol.Schema = vol.Schema(
    {
        vol.Required(CONF_MODELO): str,
        vol.Required(CONF_CODIGO_FIPE): str,
    }
)


class FIPEConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """FIPE config flow."""

    def __init__(self) -> None:
        """Initialize FIPE config flow."""
        self.modelo: str
        self.codigo_fipe: str

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            if await get_prices(
                hass=self.hass,
                codigo_fipe=user_input.get(CONF_CODIGO_FIPE),
            ):
                self.modelo = user_input.get(CONF_MODELO)
                self.codigo_fipe = user_input.get(CONF_CODIGO_FIPE)

                return self.async_create_entry(
                    title=self.modelo.capitalize(),
                    data={
                        CONF_MODELO: self.modelo,
                        CONF_CODIGO_FIPE: self.codigo_fipe,
                    },
                )

            errors[CONF_MODELO] = "modelo_error"
            errors[CONF_CODIGO_FIPE] = "codigo_fipe_error"

        return self.async_show_form(
            step_id="user",
            data_schema=self.add_suggested_values_to_schema(
                DATA_SCHEMA,
                user_input,
            ),
            errors=errors,
        )
