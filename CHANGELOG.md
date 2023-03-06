# CHANGELOG

## 20.0.0
-Refonte complet de l'addon

[@+DoM(Ô¿Ô) 🖖]
## 16.0.2
-Changement calcul retour pour sonde Température EDISIO

[@+DoM(Ô¿Ô) 🖖]

## 16.0.1
-Changement sur le protocol suite a bug sur le mode JAMMING.

[@+DoM(Ô¿Ô) 🖖]

## 16.0.0

- Modifications d'envoie des commandes
- Les commandes RTS devraient être OK en mode UI
- La commande ASSOC doit-être avec un ID x
![image](https://user-images.githubusercontent.com/97252459/199836924-f628ac47-9b2c-452c-8e1f-834584a2c43c.png)

  Info en mode Yaml:

      service: rfplayer.send_command
      data:
        command: ASSOC
        automatic_add: false
        protocol: RTS
        device_id: "1"
    

- Le switch doit être créé normalement avec switch.rts_x ou x est le numéro ID
![image](https://user-images.githubusercontent.com/97252459/199837029-8aa97fac-cebe-427d-91b9-775f66cbd6d2.png)

  Info en mode Yaml [ici avec création du switch.rts_1]

      service: rfplayer.send_command
      data:
        command: "ON"
        automatic_add: true
        protocol: RTS
        device_id: "1"

## 15.0.0

- Ajout Oregon et Edisio protocoles
- Ajout Jamming 
- test autres entités
