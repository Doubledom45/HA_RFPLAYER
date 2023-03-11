# CHANGELOG

## 1.0.0
-Refonte complet de l'addon

[@+DoM(Ô¿Ô) 🖖]
Dans l'outil de développement, création d'un sélecteur de protocol !

Le 1er est vide 'space' pour test sans protocol directement dans commande.
Attention à la syntaxe des commandes !


- Les commandes RTS devraient être OK en mode UI
- La commande ASSOC doit-être avec un ID x
![image](https://user-images.githubusercontent.com/97252459/224477047-cd72b54e-e0b8-4a25-bf09-d4bfda62ebb0.png)
  Info en mode Yaml:

service: rfplayer.send_command
````
data:
  automatic_add: false
  command: ASSOC
  protocol: RTS
  device_id: "1"
  entity_type: switch
````
- Le switch doit être créé normalement avec switch.rts_x ou x est le numéro ID
![image](https://user-images.githubusercontent.com/97252459/224477085-78a7ad43-4391-4149-8e97-1ba653735296.png)

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
