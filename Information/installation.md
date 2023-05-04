# HA_RFPlayer

Composant/intégration personnalisé RFPlayer pour Home assistant

## ATTENTION SI INSTALLATION VERSION RFPLAYER AUTRES SINON PASSAGE Installation !
Vérifier la présence ou non du répertoire "rfplayer"
Il faut désinstaller proprement cette version !
## N' OUBLIER PAS DE FAIRE UNE SAUVEGARDE DE VOTRE HA !
Si présence voir dans ![image](https://user-images.githubusercontent.com/97252459/224483549-5ce9f3e0-9eee-4d9f-b7d3-cd8e0eae232e.png)

Puis Vérifier dans ![image](https://user-images.githubusercontent.com/97252459/224483582-366479e1-230b-46ce-a170-0b7bc17d2ddb.png)

la présence du Rfplayer, qu'il faut désinstaller !

Ensuite désinstallation « propre » de l’addon du Rfplayer !
Les 3pts verticaux et supprimer
![image](https://user-images.githubusercontent.com/97252459/224483682-32e5f47d-ece7-4342-ba51-a3415cdb1874.png)

Puis dans HACS on va voir l’addon et on désinstalle !

![image](https://user-images.githubusercontent.com/97252459/224483768-021a619c-b07e-4f73-8058-a861582a01e3.png)

Bien redémarré HA !
Suivant comment on a installer la version, il se peut qu’il y ai encore une trace du Rfplayer ( répertoire ?)

## A VERIFIER ! IL DOIT être supprimer pour passer à la suite !

# Installation propre par HACS

SINON Copiez le dossier `custom_component/rfplayer` dans votre répertoire de configuration..

## -HACS INSTALLATION

Il est possible de faire l'intégration par HACS, avec un ajout de dêpot personnalisé 

![image](https://user-images.githubusercontent.com/97252459/224483977-d47eb6af-28e0-4c1e-9b95-9c0b87a44929.png)

UN Clic sur![image](https://user-images.githubusercontent.com/97252459/224484013-7b0516bf-3434-4a84-a113-1d261938c1aa.png)



[Dépôt]()

[https://github.com/Doubledom45/HA_Rfplayer]

[Catégorie]()

Intégration



Puis [Ajouter]()

![image](https://user-images.githubusercontent.com/97252459/236184535-f63ebc80-838e-4631-a72d-5cd2d88b7477.png)

Il peut y avoir d'autres intégrations, bien faire un clic sur cette version!
Devrait devenir, puis cliquer sur la croix pour fermer :

![image](https://user-images.githubusercontent.com/97252459/236185781-54d6aef3-2ac9-49e8-997d-264efde2fe02.png)



Si ok, le nouveau dépôt devrait être présent dans HA

![image](https://user-images.githubusercontent.com/97252459/236187859-ae13d033-4f6c-444c-b28c-a5c1f5b8c299.png)

Clic sur cette intégration !

![image](https://user-images.githubusercontent.com/97252459/236186387-ee45e8b8-86c8-40f1-9a32-21d28023a38c.png)


Un clic sur ![image](https://user-images.githubusercontent.com/97252459/236188971-e68a7b96-ab44-443f-a5d2-103d23f80913.png)

![image](https://user-images.githubusercontent.com/97252459/236189314-6d7ed618-9489-4ece-a52b-6c06ae6afe8c.png)


Confirmer le téléchargement![image](https://user-images.githubusercontent.com/97252459/236189484-90e7afc5-ecc7-4fe8-952a-02c3cd6ba741.png)


Devrait-être maintenant dans le répertoire config/custom_components/

ON REPASSE SOUS HA !
![image](https://user-images.githubusercontent.com/97252459/224484449-29376bec-4bc5-4533-8355-415c88ece7d7.png)

IL DEVRAIT Y AVOIR AU MOINS CETTE CORRECTION A FAIRE
![image](https://user-images.githubusercontent.com/97252459/236189834-5d9777cf-c938-46c3-bea8-a280f54c9a26.png)


ON DOIT valider
![image](https://user-images.githubusercontent.com/97252459/236190042-b66049c1-089e-4f02-874a-d5eb65f26aeb.png)

Puis on attend que HA redémarre, on peux cliquer sur terminer !
![image](https://user-images.githubusercontent.com/97252459/224484520-b18ef2bf-b71f-483a-b4a5-e47e688b3eda.png)
![image](https://user-images.githubusercontent.com/97252459/236193829-dc82ee5c-7fa1-4c0e-86e0-09b26fcbe84e.png)

ON REPASSE SUR
![image](https://user-images.githubusercontent.com/97252459/224484572-51d460f3-ee54-4c91-ae1a-affa70de1280.png)

PUIS SUR

![image](https://user-images.githubusercontent.com/97252459/224484600-09a1095b-0160-4120-b358-fcd74454cadc.png)

DANS CONFIGURER UNE NOUVELLE INTEGRATION
ON ENTRE "rfplayer"

![image](https://user-images.githubusercontent.com/97252459/236191481-c2732228-1446-4666-8a9d-fe6dee69cdff.png)

PUIS ON CLIC SUR CELLE-CI
L’assistant devrait démarrer

![image](https://user-images.githubusercontent.com/97252459/224484864-f75f416d-2b6a-456a-b93f-9df96fcfce18.png)

ENSUITE ATTENTION DE SELECTIONNER LE BON PORT QUAND DEJA D’AUTRES EN COURS !!

Il faut un avec FTDI et FT232R

![image](https://user-images.githubusercontent.com/97252459/224484891-02df16b8-2029-4813-b1a5-6a27ced6bd0d.png)

Si VALIDER

![image](https://user-images.githubusercontent.com/97252459/224484991-24ef2315-98a3-404e-8cf5-5b8899e38073.png)

Puis Terminer

![image](https://user-images.githubusercontent.com/97252459/236192065-10f32514-d76d-4950-9e8c-4545042de21d.png) Clic sur ![image](https://user-images.githubusercontent.com/97252459/236192522-f3733c4c-461b-4ab1-b1d5-1105e4f5a6f7.png)![image](https://user-images.githubusercontent.com/97252459/236192355-c39fe6bf-f33c-4f14-b41a-a01e04ffdbfe.png)

Choisir l'ajout automatique (c'est mieux !) Puis ![image](https://user-images.githubusercontent.com/97252459/236192807-fa193378-9346-497d-9dc4-6d83e33ded0f.png)

![image](https://user-images.githubusercontent.com/97252459/236192977-ac3ce17a-bee3-46f7-b750-6ae53769204a.png)

Clic sur ![image](https://user-images.githubusercontent.com/97252459/236193122-baf6d8d4-f70e-4b92-bbd3-e2776a53f9b4.png)


ON DOIT VOIR LES ENTITES SE REMPLIR ON PEUT CLIQUER SUR 1 appareil

ICI UNE VERSION
![image](https://user-images.githubusercontent.com/97252459/224485058-59eb7b0b-6907-4592-b1c3-ad7a81a20e38.png)

Recharger la page pour avoir le Journal !



