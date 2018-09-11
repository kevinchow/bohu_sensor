"""
Support for TCP socket based sensors.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/sensor.tcp/
"""
import logging
import socket
import select
import json

import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (
    CONF_NAME, CONF_HOST, CONF_PORT, CONF_PAYLOAD, CONF_TIMEOUT,
    CONF_UNIT_OF_MEASUREMENT, CONF_VALUE_TEMPLATE, STATE_UNKNOWN)
from homeassistant.exceptions import TemplateError
from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

CONF_BUFFER_SIZE = 'buffer_size'
CONF_VALUE_ON = 'value_on'

DEFAULT_BUFFER_SIZE = 1024
DEFAULT_NAME = 'TCP Sensor'
DEFAULT_TIMEOUT = 10

CONF_JSON_ATTRS = 'json_attributes'
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
    vol.Required(CONF_PORT): cv.port,
    vol.Required(CONF_PAYLOAD): cv.string,
    vol.Optional(CONF_JSON_ATTRS, default=[]): cv.ensure_list_csv,
    vol.Optional(CONF_BUFFER_SIZE, default=DEFAULT_BUFFER_SIZE):
        cv.positive_int,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Optional(CONF_TIMEOUT, default=DEFAULT_TIMEOUT): cv.positive_int,
    vol.Optional(CONF_UNIT_OF_MEASUREMENT): cv.string,
    vol.Optional(CONF_VALUE_ON): cv.string,
    vol.Optional(CONF_VALUE_TEMPLATE): cv.template,
})


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the TCP Sensor."""
    json_attrs = config.get(CONF_JSON_ATTRS)
    add_entities([TcpSensor(hass, config, json_attrs)])


class TcpSensor(Entity):
    """Implementation of a TCP socket based sensor."""

    required = tuple()

    def __init__(self, hass, config, json_attrs):
        """Set all the config values if they exist and get initial state."""
        value_template = config.get(CONF_VALUE_TEMPLATE)

        if value_template is not None:
            value_template.hass = hass

        self._json_attrs = json_attrs
        self._hass = hass
        self._value_template = value_template
        self._config = {
            CONF_NAME: config.get(CONF_NAME),
            CONF_HOST: config.get(CONF_HOST),
            CONF_PORT: config.get(CONF_PORT),
            CONF_JSON_ATTRS: config.get(CONF_JSON_ATTRS),
            CONF_TIMEOUT: config.get(CONF_TIMEOUT),
            CONF_PAYLOAD: config.get(CONF_PAYLOAD),
            CONF_UNIT_OF_MEASUREMENT: config.get(CONF_UNIT_OF_MEASUREMENT),
            CONF_VALUE_TEMPLATE: value_template,
            CONF_VALUE_ON: config.get(CONF_VALUE_ON),
            CONF_BUFFER_SIZE: config.get(CONF_BUFFER_SIZE),
        }
        self._state = None
        self.update()

    @property
    def name(self):
        """Return the name of this sensor."""
        name = self._config[CONF_NAME]
        if name is not None:
            return name
        return super(TcpSensor, self).name

    @property
    def state(self):
        """Return the state of the device."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this entity."""
        return self._config[CONF_UNIT_OF_MEASUREMENT]

    @property
    def state_attributes(self):
        """Return the attributes of the entity.

           Provide the parsed JSON data (if any).
        """

        return self._attributes

    def update(self):
        """Get the latest value for this sensor."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(self._config[CONF_TIMEOUT])
            try:
                sock.connect(
                    (self._config[CONF_HOST], self._config[CONF_PORT]))
            except socket.error as err:
                _LOGGER.error(
                    "Unable to connect to %s on port %s: %s",
                    self._config[CONF_HOST], self._config[CONF_PORT], err)
                return

            try:
                sock.send(self._config[CONF_PAYLOAD].encode())
            except socket.error as err:
                _LOGGER.error(
                    "Unable to send payload %r to %s on port %s: %s",
                    self._config[CONF_PAYLOAD], self._config[CONF_HOST],
                    self._config[CONF_PORT], err)
                return

            readable, _, _ = select.select(
                [sock], [], [], self._config[CONF_TIMEOUT])
            if not readable:
                _LOGGER.warning(
                    "Timeout (%s second(s)) waiting for a response after "
                    "sending %r to %s on port %s.",
                    self._config[CONF_TIMEOUT], self._config[CONF_PAYLOAD],
                    self._config[CONF_HOST], self._config[CONF_PORT])
                return

            value = sock.recv(self._config[CONF_BUFFER_SIZE]).decode()
            value =  value.replace(",}", "}")
#            value = '{"PM25":"0","PM1":"0","PM10":"0","CO2":"0","HCHO":"0","TEMR":"25","HIM":"82","AQI":"0","VOC":"0.08"}'

#        if self._config[CONF_VALUE_TEMPLATE] is not None:
#            try:
#                self._state = self._config[CONF_VALUE_TEMPLATE].render(
#                    value=value)
#                return
#            except TemplateError as err:
#                _LOGGER.error(
#                    "Unable to render template of %r with value: %r",
#                    self._config[CONF_VALUE_TEMPLATE], value)
#                return
        if self._json_attrs:
            self._attributes = {}
            if value:
                try:
                    json_dict = json.loads(value)
                    if isinstance(json_dict, dict):
                        attrs = {k: json_dict[k] for k in self._json_attrs
                                 if k in json_dict}
                        self._attributes = attrs
                    else:
                        _LOGGER.warning("JSON result was not a dictionary")
                except ValueError:
                    _LOGGER.warning("REST result could not be parsed as JSON")
                    _LOGGER.debug("Erroneous JSON: %s", value)
            else:
                _LOGGER.warning("Empty reply found when expecting JSON data")
        if value is None:
            value = STATE_UNKNOWN
        elif self._value_template is not None:
            value = self._value_template.render_with_possible_json_value(
                value, STATE_UNKNOWN)
        self._state = value
