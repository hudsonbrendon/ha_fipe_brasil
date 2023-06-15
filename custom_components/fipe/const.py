from datetime import timedelta

BASE_URL = "https://brasilapi.com.br/api/fipe/preco/v1/"
ICON = "mdi:car"

CONF_CODIGO_FIPE = "codigo_fipe"
CONF_MODELO = "modelo"
SCAN_INTERVAL = timedelta(minutes=120)
DOMAIN = "fipe"
