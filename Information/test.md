# HA_RFPlayer Test

Composant/intégration personnalisé RFPlayer pour Home assistant

## Installation

Copiez le dossier `custom_component/rfplayer` dans votre répertoire de configuration..

## Puis passer au .1 (ci-dessous)

Il est possible de faire l'intégration par HACS, avec un ajout de dêpot personnalisé 

[Dépôt]()

https://github.com/Doubledom45/HA_Rfplayer_TEST

[Catégorie]()

Intégration

![image](https://user-images.githubusercontent.com/97252459/224387410-5852fc9d-ce53-4cf7-94b9-6475520f0ac6.png)

Puis ![image](https://user-images.githubusercontent.com/97252459/224387270-2e84753a-deb7-4d5b-b7f7-7285123528f8.png)

Si ok,

![image](https://user-images.githubusercontent.com/97252459/224387582-fbdd8cd8-5b39-483c-b60b-d7a85a10f9b8.png)

repasser sur intégration , le nouveau dépôt devrait être présent ! rechercher "rfplayer"

![image](https://user-images.githubusercontent.com/97252459/224388042-0e232be6-bb4d-4a5f-a093-e3e8e4b17b7f.png)

Cliquer SUR ![image](https://user-images.githubusercontent.com/97252459/224388892-0537bda7-145f-4e7e-b055-96e591e513ca.png)

![image](https://user-images.githubusercontent.com/97252459/224388614-c65ed3fb-7bab-497e-81c0-faa9b163b696.png)

Cliquer en bas sur! ![image](https://user-images.githubusercontent.com/97252459/224389317-4bfade2f-8666-4d0d-b610-6f803a127f59.png)

![image](https://user-images.githubusercontent.com/97252459/224389455-cd05ff3b-7cd8-4299-8b57-aaf5537fb7a6.png)

Confirmer le téléchargement cliquer sur !![image](https://user-images.githubusercontent.com/97252459/224389628-e46e01af-ade6-4d3d-a24e-8bfe0f7a1c94.png)

ALORS! EN HAUT sur la flêche  

Cliquer sur <- ![image](https://user-images.githubusercontent.com/97252459/224390487-143eaa02-17e1-4dcf-a1ff-9cdc513166af.png)



Il faut redémarrer HA !

![image](https://user-images.githubusercontent.com/97252459/224391469-947b67b3-072d-4a78-baa4-d96fbf92cd32.png)

![image](https://user-images.githubusercontent.com/97252459/224391603-485faddb-8a47-438a-a474-e23bcaaef814.png)

![image](https://user-images.githubusercontent.com/97252459/224391686-f852970a-09a5-4378-86cc-a231b6df57a8.png)

![image](https://user-images.githubusercontent.com/97252459/224391930-a5b25536-56ec-4bb1-bc11-7b523c490543.png)

![image](https://user-images.githubusercontent.com/97252459/224391992-47cc8c8c-3fe4-4488-a4b9-9194b366d1bc.png)


#          .1

Aprés redémarrage

Passer sur Paramètres

Appareils et services

Cliquer sur
![image](https://user-images.githubusercontent.com/97252459/188457665-35314cf4-fb1a-4e07-ae04-70a864da2a6c.png)

Rechercher intégration [rfplayer]()

![image](https://user-images.githubusercontent.com/97252459/224392633-0967b596-49e4-422a-9976-c8f0fdbebec3.png)

![image](https://user-images.githubusercontent.com/97252459/224393108-b01c4c38-8709-4ec0-b400-fddfaf6f065f.png)


Sélectionnez le périphérique USB dans la liste et validez.

![image](https://user-images.githubusercontent.com/97252459/188458404-cbe00813-e6b5-4903-bc55-b4ede158fe4a.png)

![image](https://user-images.githubusercontent.com/97252459/188461028-b7149bfb-e439-4e34-a0b9-e5964a0d8f79.png)

Repasser dans Intégration

![image](https://user-images.githubusercontent.com/97252459/188461765-4115be83-6354-404e-8bb7-dc06028c67d9.png)





## Usage

Les capteurs sont créés automatiquement si vous l'activez lors de l'installation ou sur le bouton d'option (menu Intégration)
![image](https://user-images.githubusercontent.com/97252459/199841626-7a8ffd4e-a4c1-42b9-9ad9-c610741a671d.png)

![image](https://user-images.githubusercontent.com/97252459/199841538-7dde2fb0-1f8e-4d89-b9ff-0d3f4708bf53.png)

OU sur les points verticaux![image](https://user-images.githubusercontent.com/97252459/199842127-361021e0-f7ab-49b0-b7a2-6e2a0910b44d.png)et ![image](https://user-images.githubusercontent.com/97252459/199841884-c2ade168-90db-427b-b59b-c344ccd6db6d.png)


## ATTENTION LES ENTITIES PEUVENT AUGMENTER ASSEZ RAPIDEMENT 
## UTLISER QUE SI BESOIN !![image](https://user-images.githubusercontent.com/97252459/199841327-8c286819-0fe7-431a-9f91-1d93452e61bf.png)

Vous pouvez utiliser le service `rfplayer.send_command` pour envoyer des commandes à vos appareils et ajouter l'appareil en tant que nouvelle entité de commutateur.

## Outil de développement 'services' '
'Dans l'outil de développement 'services' '
    'Beta_RFPlayer: send_command'
    ![image](https://user-images.githubusercontent.com/97252459/199838206-f197c378-09bf-40f5-8ef9-90c415bc4bc3.png)
    
Les commandes peuvent être saisies directement avec les parties complétées:

![image](https://user-images.githubusercontent.com/97252459/199838738-264fff55-25ec-4ad2-87ce-6bf48597834e.png)

![image](https://user-images.githubusercontent.com/97252459/199838823-bce151ab-f860-497c-83fe-f607ab99eea1.png)

![image](https://user-images.githubusercontent.com/97252459/199838879-af833a07-dc2c-4f72-8dc5-1b3ee08377ae.png)

![image](https://user-images.githubusercontent.com/97252459/199838930-68cf3308-dcf6-4fcd-897d-bb8f0b0def84.png)

La description de protocole/commmande et addresse: voir pages 13,14 du rfplayer_api_v1.15.pdf

et si besoin :
![image](https://user-images.githubusercontent.com/97252459/199839009-bad0ef35-ea41-4d52-9c56-d0fa4c85b5d2.png)

Puis en cliquant sur:![image](https://user-images.githubusercontent.com/97252459/199839178-5425c0a9-1cd4-4ccc-82d1-2915a6e5114d.png)

Si OK :![image](https://user-images.githubusercontent.com/97252459/199839322-42aed914-e67e-4d22-8d6f-ab79d5d653e5.png)

Si erreur : ![image](https://user-images.githubusercontent.com/97252459/199839448-92e692ce-21ff-4538-ace9-ec312fe3000e.png)

  Vérifier les entités crées dans la partie ![image](https://user-images.githubusercontent.com/97252459/199840717-bb44c813-2359-44bc-87eb-81e33b36871c.png)

  ![image](https://user-images.githubusercontent.com/97252459/199840557-b6b9628d-fe1f-408f-9055-2fa62bf897ea.png)
------>
![image](https://user-images.githubusercontent.com/97252459/199840662-d71280e3-fdca-4ea2-894b-aedfa3335e8f.png)

La liste des entités
  ![image](https://user-images.githubusercontent.com/97252459/199840129-1b7f4e19-8baa-4149-b5cb-b9cff201b87c.png)


## LOG
Pour les logs ajouter dans le configuration.yaml, partie logger 

        custom_components.rfplayer: debug
( si "logger" n'existe pas il faut créer )

Exemple:

    logger:
      default: info
      logs:
        custom_components.rfplayer: debug
        homeassistant.components.rfxtrx: debug
    

## Credits
Version TEST, pour remonter entité correctement !

En attente de test pour version GCE

ORIGIN [GCE](https://github.com/gce-electronics/HA_RFPlayer) & [crazymikefra](https://github.com/crazymikefra/HA_RFPlayer)
