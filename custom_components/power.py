DOMAIN = "power"

DEPENDENCIES = ["mqtt"]


TOPIC = "domos/arduino/power"


def setup(hass, config):
    """Set up the Hello MQTT component."""
    mqtt = hass.components.mqtt
    entity_id = "power.switch_"

    id_switch_1= entity_id + "1"
    id_switch_0= entity_id + "0"

    hass.states.set(id_switch_0, "off")
    hass.states.set(id_switch_1, "off")

    def control_switch(switch, state):
        mqtt.publish(TOPIC + str(switch), state)
        
    def switch0(call):
        state = call.data.get("state")
        control_switch(0,state)
        hass.states.set(id_switch_0, state)
    
    def switch1(call):
        state = call.data.get("state")
        control_switch(1,state)
        hass.states.set(id_switch_1, state)

    hass.services.register(DOMAIN, "switch0", switch0)
    hass.services.register(DOMAIN, "switch1", switch1)


    # Return boolean to indicate that initialization was successfully.
    return True