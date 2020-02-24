import homeassistant.loader as loader

# The domain of your component. Should be equal to the name of your component.
DOMAIN = "indoor_meteo"

# List of integration names (string) your integration depends upon.
DEPENDENCIES = ["mqtt"]

TEMPERATURE = "temperature"
HUMIDITY = "humidity"
PRESSURE = "pressure"

CONF_TOPIC = "topic"
DEFAULT_TOPIC = "domos/info/meteo/"


def setup(hass, config):
    """Set up the Hello MQTT component."""
    mqtt = hass.components.mqtt

    topic_temp = config[DOMAIN].get(CONF_TOPIC, DEFAULT_TOPIC + TEMPERATURE)
    topic_humi = config[DOMAIN].get(CONF_TOPIC, DEFAULT_TOPIC + HUMIDITY)
    topic_pres = config[DOMAIN].get(CONF_TOPIC, DEFAULT_TOPIC + PRESSURE)

    temperature = "indoor_meteo.temperature"
    humidity = "indoor_meteo.humidity"
    pressure = "indoor_meteo.pressure"

    def message_received_temp(msg):
        """Handle new MQTT messages."""
        hass.states.set(temperature, msg.payload)

    def message_received_humi(msg):
        """Handle new MQTT messages."""
        hass.states.set(humidity, msg.payload)

    def message_received_pres(msg):
        """Handle new MQTT messages."""
        hass.states.set(pressure, msg.payload)

    # Subscribe our listener to a topic.
    mqtt.subscribe(topic_temp, message_received_temp)
    mqtt.subscribe(topic_humi, message_received_humi)
    mqtt.subscribe(topic_pres, message_received_pres)


    # Set the initial state.
    hass.states.set(temperature, "-1")
    hass.states.set(humidity, "-1")
    hass.states.set(pressure, "-1")
    
    # Service to publish a message on MQTT.
    # def set_state_service(call):
    #     """Service to send a message."""
    #     mqtt.publish(t, call.data.get("new_state"))

    # # Register our service with Home Assistant.
    # hass.services.register(DOMAIN, "set_state", set_state_service)

    # Return boolean to indicate that initialization was successfully.
    return True
