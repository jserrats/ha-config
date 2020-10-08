import homeassistant.loader as loader
from homeassistant.helpers import template as templater

# The domain of your component. Should be equal to the name of your component.
DOMAIN = "lcd"

# List of integration names (string) your integration depends upon.
DEPENDENCIES = ["mqtt"]


CONF_TOPIC = "topic"
DEFAULT_TOPIC = "domos/arduino/lcd"


def setup(hass, config):
    """Set up the Hello MQTT component."""
    mqtt = hass.components.mqtt
    topic = config[DOMAIN].get(CONF_TOPIC, DEFAULT_TOPIC)
    base_entity_id = "lcd"
    lines = [base_entity_id + "." + str(i) for i in range(4)]
    backlight = base_entity_id + ".backlight"

    # Set the initial state.
    for line in lines:
        hass.states.set(line, "")

    hass.states.set(line, "off")

    def format_line(call):
        text = templater.Template(call.data.get("text"), hass).async_render()
        return "{:^20.20}".format(text)

    # Service to publish a message on MQTT.
    def print_line_0(call):
        """Service to send a message."""
        text = format_line(call)
        mqtt.publish(topic + "/0", text)
        hass.states.set(lines[0], text)

    def print_line_1(call):
        """Service to send a message."""
        text = format_line(call)
        mqtt.publish(topic + "/1", text)
        hass.states.set(lines[1], text)

    def print_line_2(call):
        """Service to send a message."""
        text = format_line(call)
        mqtt.publish(topic + "/2", text)
        hass.states.set(lines[2], text)

    def print_line_3(call):
        """Service to send a message."""
        text = format_line(call)
        mqtt.publish(topic + "/3", text)
        hass.states.set(lines[3], text)

    def backlight_on(call):
        mqtt.publish(topic + "/bl", "y")
        hass.states.set(backlight, "on")

    def backlight_off(call):
        mqtt.publish(topic + "/bl", "n")
        hass.states.set(backlight, "off")

    def backlight_toggle(call):
        if(hass.states.is_state(backlight, "on")):
            backlight_off(call)
        else:
            backlight_on(call)

    # Register our service with Home Assistant.
    hass.services.register(DOMAIN, "print0", print_line_0)
    hass.services.register(DOMAIN, "print1", print_line_1)
    hass.services.register(DOMAIN, "print2", print_line_2)
    hass.services.register(DOMAIN, "print3", print_line_3)
    hass.services.register(DOMAIN, "backlight_on", backlight_on)
    hass.services.register(DOMAIN, "backlight_off", backlight_off)
    hass.services.register(DOMAIN, "backlight_toggle", backlight_toggle)

    # Return boolean to indicate that initialization was successfully.
    return True
