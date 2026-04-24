import logging
import requests
import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA, SensorEntity
from homeassistant.const import (
    CONF_NAME,
    CONF_TIMEOUT,
    CONF_UNIT_OF_MEASUREMENT,
)
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

# New configuration keys for the API
CONF_DEVICE_ID = "device_id"
DEFAULT_NAME = "Bohu Air Sensor"
DEFAULT_TIMEOUT = 10

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_DEVICE_ID): cv.string,
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
        vol.Optional(CONF_TIMEOUT, default=DEFAULT_TIMEOUT): cv.positive_int,
        vol.Optional(CONF_UNIT_OF_MEASUREMENT, default="ppm"): cv.string,
    }
)

def setup_platform(hass, config, add_entities, discovery_info=None):
    add_entities([BohuAirSensor(config)])

class BohuAirSensor(SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, config):
        self._device_id = config[CONF_DEVICE_ID]
        self._timeout = config[CONF_TIMEOUT]
        self._url = f"https://www.bohu-tech.com/iot/api/open/latest?device_id={self._device_id}"

        self._attr_name = config[CONF_NAME]
        self._attr_unit_of_measurement = config[CONF_UNIT_OF_MEASUREMENT]
        self._attr_native_value = None
        self._attr_extra_state_attributes = {}

    # ---------- SAFE CONVERTERS ----------

    def _to_int(self, value):
        if value is None: return None
        try:
            return int(float(value))
        except (ValueError, TypeError):
            return None

    def _to_float(self, value):
        if value is None: return None
        try:
            return float(value)
        except (ValueError, TypeError):
            return None

    # ---------- UPDATE ----------

    def update(self):
        try:
            response = requests.get(self._url, timeout=self._timeout)
            response.raise_for_status()
            res_json = response.json()

            if res_json.get("code") != 0:
                _LOGGER.error("API returned error code: %s", res_json.get("msg"))
                return

            data = res_json.get("data", {}).get("sensors", {})
            
        except Exception as err:
            _LOGGER.error("Error fetching data from Bohu API: %s", err)
            return

        # ---------- MAIN STATE (CO2) ----------
        # Mapping 'co2' from the new API
        self._attr_native_value = self._to_int(data.get("co2"))

        # ---------- ATTRIBUTES ----------
        self._attr_extra_state_attributes = {
            "pm1": self._to_int(data.get("pm1")),
            "pm25": self._to_int(data.get("pm25")),
            "pm10": self._to_int(data.get("pm10")),
            "humidity": self._to_int(data.get("hum")),
            "temperature": self._to_float(data.get("temp")),
            "tvoc": self._to_float(data.get("tvoc")),
            "hcho": self._to_float(data.get("hcho")),
            "last_check_utc": res_json.get("data", {}).get("timestamp")
        }
