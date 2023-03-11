# CHANGELOG

## 1.0.0
-Refonte complet de l'addon

[@+DoM(Ô¿Ô) 🖖]

Dans l'outil de développement, création d'un sélecteur de protocol ! et de "
Entity type"

Le 1er est vide 'space' pour test sans protocol directement dans commande.
Attention à la syntaxe des commandes !


- ICI test commandes RTS 
- La commande ASSOC doit-être avec un ID x
![image](https://user-images.githubusercontent.com/97252459/224477543-e17eeeee-c1d9-41d7-9be3-f859c0a24c75.png)
  Info en mode Yaml:

service: rfplayer.send_command
````
data:
  automatic_add: false
  command: ASSOC
  protocol: RTS
  device_id: "1"
  entity_type: cover
````
- Le "cover" doit être créé normalement avec switch.rts_x ou x est le numéro ID
![image](https://user-images.githubusercontent.com/97252459/224477511-d2c39671-f9dd-4bde-9c35-76f35f1940c6.png)

  Info en mode Yaml [ici avec création du switch.rts_1]
````
service: rfplayer.send_command
data:
  automatic_add: true
  command: "ON"
  protocol: RTS
  device_id: "1"
  entity_type: switch
````
Ce qui doit donner ![image](https://user-images.githubusercontent.com/97252459/224477619-75d91e29-2b70-407a-a4a2-499bdd9ed805.png)
