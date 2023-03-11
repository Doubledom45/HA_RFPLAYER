# HA_RFPlayer TEST

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

https://github.com/Doubledom45/HA_Rfplayer_TEST

[Catégorie]()

Intégration



Puis [Ajouter]()

![image](https://user-images.githubusercontent.com/97252459/224484066-ad997392-e156-4642-9f10-be08922a4479.png)

Il peut y avoir d'autres intégrations, bien faire un clic sur cette version!

![image](https://user-images.githubusercontent.com/97252459/224484124-354486d5-2335-40f7-a1e8-f3c0a2f8144f.png)



Si ok, le nouveau dépôt devrait être présent !

![image](https://user-images.githubusercontent.com/97252459/224484305-efd58ffc-e4b7-44ee-992a-2fd66c1ccc2e.png)


Puis sur [Téléchargé]()

![image](https://user-images.githubusercontent.com/97252459/224484371-2630234e-0c50-443c-b9cd-64035cea074b.png)


Confirmer le téléchargement

Devrait-être maintenant dans le répertoire config/custom_components/

ON REPASSE SOUS HA !
![image](https://user-images.githubusercontent.com/97252459/224484449-29376bec-4bc5-4533-8355-415c88ece7d7.png)

IL DEVRAIT Y AVOIR AU MOINS CETTE CORRECTION A FAIRE
![image](https://user-images.githubusercontent.com/97252459/224484465-45896811-69f7-4307-81f6-70bce0472ead.png)


ON DOIT valider
![image](https://user-images.githubusercontent.com/97252459/224484504-f913d4c8-6555-4635-8b09-ae38bd6d631d.png)

Puis on attend que HA redémarre, on peux cliquer sur terminer !
![image](https://user-images.githubusercontent.com/97252459/224484520-b18ef2bf-b71f-483a-b4a5-e47e688b3eda.png)

ON REPASSE SUR
![image](https://user-images.githubusercontent.com/97252459/224484572-51d460f3-ee54-4c91-ae1a-affa70de1280.png)

PUIS SUR

![image](https://user-images.githubusercontent.com/97252459/224484600-09a1095b-0160-4120-b358-fcd74454cadc.png)

DANS CONFIGURER UNE NOUVELLE INTEGRATION

![image](https://user-images.githubusercontent.com/97252459/224484708-5c019fe2-941d-4549-a5b7-1efd85470c84.png)

ON ENTRE "rfplayer"

PUIS ON CLIC SUR CELLE-CI
L’assistant devrait démarrer

![image](https://user-images.githubusercontent.com/97252459/224484864-f75f416d-2b6a-456a-b93f-9df96fcfce18.png)

ENSUITE ATTENTION DE SELECTIONNER LE BON PORT QUAND DEJA D’AUTRES EN COURS !!

Il faut un avec FTDI et FT232R

![image](https://user-images.githubusercontent.com/97252459/224484891-02df16b8-2029-4813-b1a5-6a27ced6bd0d.png)

Si VALIDER

![image](https://user-images.githubusercontent.com/97252459/224484991-24ef2315-98a3-404e-8cf5-5b8899e38073.png)

Puis Terminer

![image](https://user-images.githubusercontent.com/97252459/224485005-69ba9b75-82d9-4742-a2ec-c1a218a66fcc.png)

ON DOIT VOIR LES ENTITES SE REMPLIR ON PEUT CLIQUER SUR 1 appareil

ICI UNE VERSION
![image](https://user-images.githubusercontent.com/97252459/224485058-59eb7b0b-6907-4592-b1c3-ad7a81a20e38.png)

Recharger la page pour avoir le Journal !



