# SUITE MODIFICATION HA 2024.3 Référentiel Archivé
Voir sur https://github.com/Doubledom45/TEST-RFPLAYER pour la suite !

# HA_Rfplayer
`Complete redesign of the add-on`

RFPlayer custom component/integration for Home assistant

## Installation

Copy the `custom_component/rfplayer` folder in your config directory.

Go to Home-Assistant UI, Configuration > Integrations, button (+ Add Integration) and search GCE RFPlayer

Select the USB device in the list and valid.

## Usage

Sensor are created automatically if you enable it during the installation or on the option button (Integration menu)

You can use the service `rfplayer.send_command` to send commands to your devices, and add the device as a new switch entity.

## Credits

ORIGIN [GCE](https://github.com/gce-electronics/HA_RFPlayer) & [crazymikefra](https://github.com/crazymikefra/HA_RFPlayer)

Based on  rflink integration

## Information

[Voir les fichiers pdf pour l'API](https://github.com/Doubledom45/HA_RFPLAYER/tree/main/Information) et [Information FR](https://github.com/Doubledom45/HA_RFPLAYER/blob/main/Information/installation.md) pour plus d'information en Français ! 

Voir [Forum HA FR](https://forum.hacf.fr/) @Doubledom en MP
