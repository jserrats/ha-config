import homeassistant.loader as loader

DOMAIN = "buttons"

DEPENDENCIES = ["mqtt"]


CONF_TOPIC = "topic"
DEFAULT_TOPIC = "domos/button"


def setup(hass, config):
    """Set up the Hello MQTT component."""
    mqtt = hass.components.mqtt
    topic = config[DOMAIN].get(CONF_TOPIC, DEFAULT_TOPIC)
    entity_id = "buttons.last_button"


    def message_received(msg):
        """Handle new MQTT messages."""
        hass.states.set(entity_id, "-1")
        hass.states.set(entity_id, msg.payload)

    mqtt.subscribe(topic, message_received)
    hass.states.set(entity_id, "-1")


    # Return boolean to indicate that initialization was successfully.
    return True