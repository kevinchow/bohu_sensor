import logging
import socket
import select
import json

import voluptuous as vol
from homeassistant.components.sensor import PLATFORM_SCHEMA, SensorEntity
from homeassistant.const import (
    CONF_NAME,
    CONF_HOST,
    CONF_PORT,
    CONF_PAYLOAD,
    CONF_TIMEOUT,
    CONF_UNIT_OF_MEASUREMENT,
)
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

CONF_BUFFER_SIZE = "buffer_size"

DEFAULT_NAME = "TCP Air Sensor"
DEFAULT_TIMEOUT = 10
DEFAULT_BUFFER_SIZE = 1024

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_HOST): cv.string,
        vol.Required(CONF_PORT): cv.port,
        vol.Required(CONF_PAYLOAD): cv.string,
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
        vol.Optional(CONF_TIMEOUT, default=DEFAULT_TIMEOUT): cv.positive_int,
        vol.Optional(CONF_BUFFER_SIZE, default=DEFAULT_BUFFER_SIZE): cv.positive_int,
        vol.Optional(CONF_UNIT_OF_MEASUREMENT, default="ppm"): cv.string,
    }
)


def setup_platform(hass, config, add_entities, discovery_info=None):
    add_entities([TcpAirSensor(config)])


class TcpAirSensor(SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, config):
        self._host = config[CONF_HOST]
        self._port = config[CONF_PORT]
        self._payload = config[CONF_PAYLOAD]
        self._timeout = config[CONF_TIMEOUT]
        self._buffer_size = config[CONF_BUFFER_SIZE]

        self._attr_name = config[CONF_NAME]
        self._attr_unit_of_measurement = config[CONF_UNIT_OF_MEASUREMENT]

        self._attr_native_value = None
        self._attr_extra_state_attributes = {}

    # ---------- SAFE CONVERTERS ----------

    def _to_int(self, value):
        try:
            v = int(float(value))
            if v < 0:
                return None
            return v
        except Exception:
            return None

    def _to_float(self, value):
        try:
            v = float(value)
            if v < 0:
                return None
            return v
        except Exception:
            return None

    # ---------- UPDATE ----------

    def update(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(self._timeout)
                sock.connect((self._host, self._port))
                sock.sendall(self._payload.encode())

                readable, _, _ = select.select([sock], [], [], self._timeout)
                if not readable:
                    _LOGGER.warning("TCP timeout waiting for response")
                    return

                raw = sock.recv(self._buffer_size).decode()
                raw = raw.replace(",}", "}")

                data = json.loads(raw)

        except Exception as err:
            _LOGGER.error("TCP sensor error: %s", err)
            return

        # ---------- MAIN STATE (CO2 INT) ----------
        self._attr_native_value = self._to_int(data.get("CO2"))

        # ---------- ATTRIBUTES ----------
        self._attr_extra_state_attributes = {
            # PM → INT
            "pm1": self._to_int(data.get("PM1")),
            "pm25": self._to_int(data.get("PM25")),
            "pm10": self._to_int(data.get("PM10")),

            # AQI / HUM → INT
            "aqi": self._to_int(data.get("AQI")),
            "humidity": self._to_int(data.get("HUM")),

            # FLOAT VALUES
            "temperature": self._to_float(data.get("TEMP")),
            "voc": self._to_float(data.get("VOC")),
            "hcho": self._to_float(data.get("HCHO")),
        }
