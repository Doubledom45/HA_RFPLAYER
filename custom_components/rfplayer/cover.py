"""Support for Rfplayer cover (V2)."""
import logging


from homeassistant.components.cover import (
    DOMAIN as PLATFORM_COVER,
    CoverEntity,
    ATTR_POSITION, ATTR_CURRENT_POSITION,
    STATE_OPEN, STATE_OPENING, STATE_CLOSED, STATE_CLOSING
)


from homeassistant.const import CONF_DEVICE_ID, CONF_DEVICES, CONF_PROTOCOL
#from homeassistant.helpers.entity import EntityCategory
from homeassistant.core import callback


try:
    from homeassistant.components.cover import CoverDeviceClass, CoverEntityFeature
    DEVICE_CLASS_GARAGE = CoverDeviceClass.GARAGEswitch
    DEVICE_CLASS_SHUTTER = CoverDeviceClass.SHUTTER
    SUPPORT_OPEN = CoverEntityFeature.OPEN
    SUPPORT_CLOSE = CoverEntityFeature.CLOSE
    SUPPORT_SET_POSITION = CoverEntityFeature.SET_POSITION
    SUPPORT_STOP = CoverEntityFeature.STOP
except:# fallback (pre 2022.5)
    from homeassistant.components.cover import (
        DEVICE_CLASS_GARAGE, DEVICE_CLASS_SHUTTER,
        SUPPORT_OPEN, SUPPORT_CLOSE,
        SUPPORT_SET_POSITION, SUPPORT_STOP,
    )

from homeassistant.helpers import config_validation as cv, entity_platform, service
from homeassistant.helpers.entity_component import EntityComponent
import voluptuous as vol



from . import DATA_DEVICE_REGISTER, EVENT_KEY_COVER, RfplayerDevice
from .const import (
    COMMAND_ON,
    COMMAND_OFF,
    COMMAND_UP,
    COMMAND_MY,
    COMMAND_DIM,
    COMMAND_DOWN,
    CONF_AUTOMATIC_ADD,
    CONF_DEVICE_ADDRESS,
    CONF_ENTITY_TYPE,
    DATA_ENTITY_LOOKUP,
    DOMAIN,
    EVENT_KEY_ID,
    ENTITY_TYPE_COVER
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    _LOGGER.debug("Add cover entity - hass : %s", str(hass))
    _LOGGER.debug("Add cover entity - entry : %s", str(entry))
    _LOGGER.debug("Add cover entity - async_add_entities : %s", str(async_add_entities))
    """Set up the Rfplayer platform."""
    config = entry.data
    options = entry.options

    platform = entity_platform.current_platform.get()
    
    platform.async_register_entity_service(
        "set_device_address",
        {
            vol.Required("device_address"): cv.string,
        },
        "set_device_address",
    )



    async def add_new_device(device_info):
        #if device_info.get(CONF_ENTITY_TYPE) == ENTITY_TYPE_COVER or device_info.get(CONF_ENTITY_TYPE) == "":
        """Check if cover device is known, otherwise create device entity."""
        #if(((device_info.get("protocol")!=None) and ((device_info.get("device_id")!=None) or (device_info.get("device_address")!=None))) or True):
        
        # create entity
        
        _LOGGER.debug("Add cover entity %s", str(device_info))
        #_LOGGER.debug("Add cover entity - protocol %s", str(device_info[CONF_PROTOCOL]))
        #_LOGGER.debug("Add cover entity - device_address %s", str(device_info.get(CONF_DEVICE_ADDRESS)))
        #_LOGGER.debug("Add cover entity - device_id %s", str(device_info.get(CONF_DEVICE_ID)))
        #_LOGGER.debug("Add cover entity - initial_event %s", str(device_info))

        try:
            
            if (device_info.get(CONF_DEVICE_ADDRESS) != None
            or device_info.get(CONF_DEVICE_ID) != None) :
                _LOGGER.debug("Create from service")
                device = RfplayerCover(
                    protocol=device_info[CONF_PROTOCOL],
                    device_address=device_info.get(CONF_DEVICE_ADDRESS),
                    device_id=device_info.get(CONF_DEVICE_ID),
                    initial_event=device_info,
                    #device_class=DEVICE_CLASS_SHUTTER
                )
            else:
                _LOGGER.debug("Create from event")
                device_id = device_info[EVENT_KEY_ID]
                device = RfplayerCover(
                    protocol=device_id.split("_")[0],
                    device_address=device_info.get(CONF_DEVICE_ADDRESS),
                    device_id=device_id.split("_")[1],
                    initial_event=device_info,
                    # device_class=DEVICE_CLASS_SHUTTER
                )
            async_add_entities([device])
        except :
            _LOGGER.error("Cover creation error : ",str(device_info))
        

    if CONF_DEVICES in config:
        items_to_delete=[]
        for device_id, device_info in config[CONF_DEVICES].items():
            if EVENT_KEY_COVER in device_info:
                if device_info.get("entity_type"):
                    device_info["platform"]=device_info.get("entity_type")
                if device_info.get(CONF_PROTOCOL)!=None and device_info.get("platform")=="cover":
                    await add_new_device(device_info)
                else :
                    _LOGGER.warning("Cover entity not created %s %s", device_id, device_info)
                    items_to_delete.append(device_id)
        for item in items_to_delete:
            config[CONF_DEVICES].pop(item)

    if options.get(CONF_AUTOMATIC_ADD, config[CONF_AUTOMATIC_ADD]):
        hass.data[DOMAIN][DATA_DEVICE_REGISTER][EVENT_KEY_COVER] = add_new_device


class RfplayerCover(RfplayerDevice, CoverEntity):
    """Representation of a Rfplayer cover."""

    _attr_protocol="";

    async def async_added_to_hass(self):
        """Restore RFPlayer device state (ON/OFF)."""
        await super().async_added_to_hass()

        self.hass.data[DOMAIN][DATA_ENTITY_LOOKUP][EVENT_KEY_COVER][
            self._initial_event[EVENT_KEY_ID]
        ] = self.entity_id

        if self._event is None:
            old_state = await self.async_get_last_state()
            if old_state is not None:
                self._state = old_state.state

    async def async_will_remove_from_hass(self):
        await super().async_will_remove_from_hass()
    
    @callback
    def _handle_event(self, event):
        _LOGGER.debug("Event : %s", str(event))
        if "value" in event:
            command = event["value"]
        else:
            command = event["cover"]
        if command in [COMMAND_UP,COMMAND_ON]:
            self._attr_state = STATE_OPEN
        elif command in [COMMAND_DOWN,COMMAND_OFF]:
            self._attr_state = STATE_CLOSED
        elif command in [COMMAND_MY]:
            self._attr_state = STATE_OPEN
        self.schedule_update_ha_state()

    @property
    def supported_features(self):
        return SUPPORT_OPEN | SUPPORT_CLOSE | SUPPORT_STOP

    @property
    def is_opening(self):
        #_LOGGER.debug("Test is opening : %s", str(self))
        return self._attr_state == STATE_OPENING

    @property
    def is_closing(self):
        #_LOGGER.debug("Test is closing : %s", str(self))
        return self._attr_state == STATE_CLOSING

    @property
    def is_closed(self):
        #_LOGGER.debug("Test is closed : %s", str(self))
        return self._attr_state == STATE_CLOSED

    async def async_open_cover(self, **kwargs) :
        _LOGGER.debug("Open cover : %s", str(self))
        """Turn the device on."""
        await self._async_send_command(COMMAND_ON)
        self._attr_state=STATE_OPEN
        self.async_schedule_update_ha_state()


    async def async_close_cover(self, **kwargs):
        _LOGGER.debug("Close cover : %s", str(self))
        """Turn the device off."""
        await self._async_send_command(COMMAND_OFF)
        self._attr_state=STATE_CLOSED
        self.async_schedule_update_ha_state(False)

    async def async_stop_cover(self, **kwargs):
        _LOGGER.debug("Stop cover : %s", str(self))
        await self._async_send_command(COMMAND_DIM)
        self._attr_state=STATE_OPEN
        self.async_schedule_update_ha_state(False)
        
