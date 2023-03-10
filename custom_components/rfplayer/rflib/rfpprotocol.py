"""Asyncio protocol implementation of RFplayer."""

import asyncio
from datetime import timedelta
from fnmatch import fnmatchcase
from functools import partial
import logging
from typing import Any, Callable, Coroutine, Optional, Sequence, Tuple, Type

from serial_asyncio import create_serial_connection

from .rfpparser import (
    PacketType,
    decode_packet,
    encode_packet,
    packet_events,
    valid_packet,
)

log = logging.getLogger(__name__)

TIMEOUT = timedelta(seconds=5)


class ProtocolBase(asyncio.Protocol):
    """Manage low level rfplayer protocol."""

    transport = None  # type: asyncio.BaseTransport

    def __init__(
        self,
        loop: Optional[asyncio.AbstractEventLoop] = None,
        disconnect_callback: Optional[Callable[[Optional[Exception]], None]] = None,
        init_options: Optional[Sequence[dict]] = None,
        **kwargs: Any,
    ) -> None:
        """Initialize class."""
        if loop:
            self.loop = loop
        else:
            self.loop = asyncio.get_event_loop()
        self.packet = ""
        self.buffer = ""
        self.packet_callback = None  # type: Optional[Callable[[PacketType], None]]
        self.disconnect_callback = disconnect_callback

    def connection_made(self, transport: asyncio.BaseTransport) -> None:
        """Just logging for now.
        INFO LORS DU FACTORYRESET
        SENSITIVITY H/L =0 Default value - High sensitivity (-0dB)
        SELECTIVITY H/L =0 : Default value - Medium selectivity (300Khz)
        DSPTRIGGER Default values -  H 868Mhz = 6dBm /L 433 Mhz = 8dBm -- Valeur : de 4 à 20 [La valeur 0 remet la valeur par défaut] C'est le niveau de détection Trame et Analyse !
        RFLINK default RFLINK engine is enabled
        RFLINKTRIGGER Default values - H 868Mhz = 10dBm  /L 433 Mhz = 12dBm -- Valeur : de 4 à 20 [La valeur 0 remet la valeur par défaut] C'est le niveau de détection en RFLINK de Trame et Analyse !
        LBT Default value : 16dBm    Val : 6 à 30 dBm Le Rfplayer attendra ( maxi 3 sec) un silence avant d'envoyer des trames        
        """
        self.transport = transport
        self.send_raw_packet("ZIA++HELLO")
##        self.send_raw_packet("ZIA++FACTORYRESET")
##        self.send_raw_packet("ZIA++RECEIVER + *")
##        self.send_raw_packet("ZIA++FORMAT JSON")
##        self.send_raw_packet("ZIA++STATUS TXT") # si tu envoie la demande de status, il faut autoriser le log ?
        if self.init_options['START_COMMANDS']:
            for command in self.init_options['START_COMMANDS']:
                self.send_raw_packet("ZIA++"+command)
 
    def data_received(self, data: bytes) -> None:
        """Add incoming data to buffer."""
        try:
            decoded_data = data.decode()
#             log.debug("data:", decoded_data)
        except UnicodeDecodeError:
            invalid_data = data.decode(errors="replace")
            log.warning("Error during decode of data, invalid data: %s", invalid_data)
        else:
            log.debug("received data: %s", decoded_data.strip())
            self.buffer += decoded_data
            self.handle_lines()

    def handle_lines(self) -> None:
        """Assemble incoming data into per-line packets."""
        while "\n\r" in self.buffer:
            line, self.buffer = self.buffer.split("\n\r", 1)
            if valid_packet(line):
                self.handle_raw_packet(line)
            else:
                log.warning("dropping invalid data: %s", line) # Voir ZIA66 = reception trame EDISIOFRAME

    def handle_raw_packet(self, raw_packet: str) -> None:
        """Handle one raw incoming packet."""
        raise NotImplementedError()

    def send_raw_packet(self, packet: str) -> None:
        """Encode and put packet string onto write buffer."""
        data = bytes(packet + "\n\r", "utf-8")
        log.debug("writing data: %s", repr(data))
        self.transport.write(data)  # type: ignore

    def connection_lost(self, exc: Optional[Exception]) -> None:
        """Log when connection is closed, if needed call callback."""
        if exc:
            log.exception("disconnected due to exception")
        else:
            log.info("disconnected because of close/abort.")
        if self.disconnect_callback:
            self.disconnect_callback(exc)


class PacketHandling(ProtocolBase):
    """Handle translating rfplayer packets to/from python primitives."""

    def __init__(
        self,
        *args: Any,
        packet_callback: Optional[Callable[[PacketType], None]] = None,
        init_options: Optional[Sequence[dict]] = None,
        **kwargs: Any,
    ) -> None:
        """Add packethandling specific initialization.
        packet_callback: called with every complete/valid packet
        received.
        """
        log.debug("PacketHandling")
        super().__init__(*args, **kwargs)
        self.init_options = init_options
        if packet_callback:
            self.packet_callback = packet_callback

    def handle_raw_packet(self, raw_packet: str) -> None:
        """Parse raw packet string into packet dict."""
        packets = []
        try:
            packets = decode_packet(raw_packet)
        except BaseException:
            log.exception("failed to parse packet data: %s", raw_packet)

        if packets:
            for packet in packets:
                if packet != None:
                    #log.debug("decoded packet: %s", packet)
                    if "ok" in packet:
#                        # handle response packets internally
                        log.debug("command response: %s", packet)
                        self.handle_response_packet(packet)
                    else:
                        #log.debug("handle packet: %s", packet)
                        self.handle_packet(packet)
        else:
            log.warning("no valid packet")

    def handle_packet(self, packet: PacketType) -> None:
        """Process incoming packet dict and optionally call callback."""
        if self.packet_callback:
#            # forward to callback
#            #log.debug("forwarding packet: %s to %s", packet,self.packet_callback.__code__)
            self.packet_callback(packet)
        else:
            log.debug("packet with no callback %s", packet)

    def handle_response_packet(self, packet: PacketType) -> None:
        """Handle response packet."""
        raise NotImplementedError()

    def send_packet(self, fields: PacketType) -> None:
        """Concat fields and send packet to gateway."""
        encoded_packet = encode_packet(fields)
        self.send_raw_packet(encoded_packet)

     def send_command(
        self,
        protocol: str,
        command: str,
        device_address: str = None,
        device_id: str = None,
    ) -> None:
        """Send device command to rfplayer gateway."""
        if device_id is not None:
 ###     La commande EDISIOFRAME avec ON ou OFF n'existe PAS MAIS ON PEUX ENVOYER avec PROTOCOL et ID [doit être la commande Hexa]
            if protocol == "EDISIOFRAME" : # A VOIR L'ENVOIE DEVRAIT ETRE DANS Commande ? INSTRUITE PLUS BAS !
                self.send_raw_packet(f"ZIA++{protocol} {device_id}") # EST OK SI ID= commande HEXA !

## modif envoie cde Protocol avec Jamming avec ID et ( commande ) Util si création !
            elif protocol == "JAMMING" :
                if command == "ON" :
                    self.send_raw_packet(f"ZIA++{protocol} {device_id}") # Permet d'avoir un ID qui représente le niveau
                elif command == "OFF" :
                    self.send_raw_packet(f"ZIA++{protocol} 0")
                else:
                    self.send_raw_packet(f"ZIA++{protocol} {command} {device_id}") # dans le cas d'une commande depuis dévelopeur !

## Peut servir pour le SIMULATE mettre dans Commande avec <delay> de  1 à 255 [secondes] Util si création !
            elif protocol == "JAMMING SIMULATE" :
                if command == "ON" :
                    self.send_raw_packet(f"ZIA++{protocol} {device_id}") # Permet d'avoir un ID qui représente le <delay>
                elif command == "OFF" :
                    self.send_raw_packet(f"ZIA++{protocol}") #Envoie le simulate avec réponse dans 5 sec si JAMMING "ON"
                else:
                    self.send_raw_packet(f"ZIA++{protocol} {command} {device_id}") # dans le cas d'une commande depuis dévelopeur avec commande= SIMULATE !

            else :
                self.send_raw_packet(f"ZIA++{command} ID {device_id} {protocol}")

        elif device_address is not None:
            DIM_ADDON=""
            if command == "DIM" :
                DIM_ADDON="%50"
            self.send_raw_packet(f"ZIA++{command} {device_address} {protocol} {DIM_ADDON}")

        elif protocol == "EDISIOFRAME":
            self.send_raw_packet(f"ZIA++{protocol} {command}")

##bug jamming pas d'ID
## modif envoie cde Protocol sans ID si Jamming ( commande ) vient du développeur ! Util si création !
        else:
            if protocol == "JAMMING" :
                if command == "ON" : #la cde n'existe pas vraiement , mais peut-être utilisé pour !
                    self.send_raw_packet(f"ZIA++{protocol} 7")
                elif command == "OFF" : #la cde n'existe pas vraiement , mais peut-être utilisé pour !
                    self.send_raw_packet(f"ZIA++{protocol} 0")
                else:
                    self.send_raw_packet(f"ZIA++{protocol} {command}") # on peut mettre le niveau de détection de 0 à 10

## Peut servir pour le SIMULATE mettre dans Commande avec <delay> de  1 à 255 [secondes] Util si création !

            elif protocol == "JAMMING SIMULATE" :
                if command == "ON" :
                    self.send_raw_packet(f"ZIA++{protocol} 30") # Permet d'avoir un nbr qui représente le <delay> forcé ici 30sec
                elif command == "OFF" :
                    self.send_raw_packet(f"ZIA++{protocol}") #Envoie le simulate avec réponse dans 5 sec si JAMMING [NIVEAU] "ON"

            else :
                self.send_raw_packet(f"ZIA++{command} {protocol}") #ATTENTION AU FORMAT DE LA COMMANDE !

        """Les cde RECEIVER ET REPEATER peuvent être initiés dans commande avec signe + ou - et la sélection du protocol."""
 
class CommandSerialization(PacketHandling):
    """Logic for ensuring asynchronous commands are sent in order."""

    def __init__(
        self,
        *args: Any,
        packet_callback: Optional[Callable[[PacketType], None]] = None,
        init_options: Optional[Sequence[dict]] = None,
        **kwargs: Any,
    ) -> None:
        """Add packethandling specific initialization."""
#        #log.debug("CommandSerialization")
        super().__init__(*args, **kwargs)
        self.init_options = init_options
        if packet_callback:
            self.packet_callback = packet_callback
        self._event = asyncio.Event()
        self._lock = asyncio.Lock()

    def handle_response_packet(self, packet: PacketType) -> None:
        """Handle response packet."""
        log.debug("handle_response_packet")
        self._last_ack = packet
        self._event.set()

    async def send_command_ack(
        self,
        protocol: str,
        command: str,
        device_address: str = None,
        device_id: str = None,
    ) -> bool:
        """Send command, wait for gateway to repond."""
        async with self._lock:
            self.send_command(protocol, command, device_address, device_id)
            self._event.clear()
#            # await self._event.wait()
        return True


class EventHandling(PacketHandling):
    """Breaks up packets into individual events with ids'.

    Most packets represent a single event (light on, measured
    temperature), but some contain multiple events (temperature and
    humidity). This class adds logic to convert packets into individual
    events each with their own id based on packet details (protocol,
    switch, etc).
    """

    def __init__(
        self,
        *args: Any,
        event_callback: Optional[Callable[[PacketType], None]] = None,
        ignore: Optional[Sequence[str]] = None,
        init_options: Optional[Sequence[dict]] = None,
        **kwargs: Any,
    ) -> None:
        """Add eventhandling specific initialization."""
        super().__init__(*args, **kwargs)
        self.event_callback = event_callback
        self.init_options = init_options
#        # suppress printing of packets
        log.debug("EventHandling")
        if not kwargs.get("packet_callback"):
            self.packet_callback = lambda x: None
        if ignore:
            log.debug("ignoring: %s", ignore)
            self.ignore = ignore
        else:
            self.ignore = []

    def _handle_packet(self, packet: PacketType) -> None:
        """Event specific packet handling logic."""
        events = packet_events(packet)

        for event in events:
            if self.ignore_event(event["id"]):
                log.debug("ignoring event with id: %s", event)
                continue
            log.debug("got event: %s", event)
            if self.event_callback:
                self.event_callback(event)
            else:
                self.handle_event(event)

    def handle_event(self, event: PacketType) -> None:
        """Handle of incoming event (print)."""
        log.debug("_handle_event")
        string = "{id:<32} "
        if "command" in event:
            string += "{command}"
        if "cover" in event:
            string += "{cover}"
        if "platform" in event:
            string += "{platform}"
        elif "version" in event:
            if "hardware" in event:
                string += "{hardware} {firmware} "
            string += "V{version} R{revision}"
        else:
            string += "{value}"
            if event.get("unit"):
                string += " {unit}"

        print(string.format(**event))

    def handle_packet(self, packet: PacketType) -> None:
        """Apply event specific handling and pass on to packet handling."""
        self._handle_packet(packet)
        super().handle_packet(packet)

    def ignore_event(self, event_id: str) -> bool:
        """Verify event id against list of events to ignore."""
        for ignore in self.ignore:
            if fnmatchcase(event_id, ignore):
                log.debug("ignore_event")
                return True
        return False


class RfplayerProtocol(CommandSerialization, EventHandling):
    """Combine preferred abstractions that form complete Rflink interface."""


def create_rfplayer_connection(
    port: str,
    baud: int = 115200,
    protocol: Type[ProtocolBase] = RfplayerProtocol,
    packet_callback: Optional[Callable[[PacketType], None]] = None,
    event_callback: Optional[Callable[[PacketType], None]] = None,
    disconnect_callback: Optional[Callable[[Optional[Exception]], None]] = None,
    ignore: Optional[Sequence[str]] = None,
    loop: Optional[asyncio.AbstractEventLoop] = None,
    init_options: Optional[Sequence[dict]] = None
) -> "Coroutine[Any, Any, Tuple[asyncio.BaseTransport, ProtocolBase]]":
    """Create Rflink manager class, returns transport coroutine."""
    if loop is None:
        loop = asyncio.get_event_loop()
    # use default protocol if not specified
    protocol_factory = partial(
        protocol,
        loop=loop,
        packet_callback=packet_callback,
        event_callback=event_callback,
        disconnect_callback=disconnect_callback,
        ignore=ignore if ignore else [],
        init_options=init_options,
    )

    # setup serial connection
    conn = create_serial_connection(loop, protocol_factory, port, baud)

    return conn
