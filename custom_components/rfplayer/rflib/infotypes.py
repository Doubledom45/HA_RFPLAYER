import logging

##Debogage des infotypes
infotypes_debug=False

log = logging.getLogger(__name__)

id_PHY_OREGON = {
    0x0 : "OREGONV1",
    0x1A2D : "THGR228",
    0xCA2C : "THGR328",
    0x0ACC : "RTGR328",
    0xEA4C : "THWR288",
    0x1A3D : "THGR918",
    0x5A6D : "THGR918N",
    0x1A89 : "WGR800",
    0xCA48 : "THWR800",
    0xFA28 : "THGR810",
    0x2A19 : "PCR800",
    0xDA78 : "UVN800",
}

def check_bitL2R(byte, bit):
    return bool(byte & (0b10000000>>bit))

def check_bitR2L(byte, bit):
    return bool(byte & (0b1<<bit))

def infoType_0_decode(infos:list,allowEmptyID:bool=False) -> list:
    if infotypes_debug: log.debug("Decode InfoType 0")
    fields_found = {}
    match infos["subType"]:
        case 0 :
            fields_found["subType"]="OFF"
        case 1 :
            fields_found["subType"]="ON"
        case 2 :
            fields_found["subType"]="BRIGHT"
        case 3 :
            fields_found["subType"]="DIM"
        case 4 :
            fields_found["subType"]="ALL_OFF"
        case 5 :
            fields_found["subType"]="ALL_ON"
    
    fields_found["id"]=infos["id"]
    fields_found["command"]=infos["subType"]

    if fields_found["id"]!="0" or allowEmptyID:
        return fields_found

def infoType_1_decode(infos:list,allowEmptyID:bool=False) -> list:
    if infotypes_debug: log.debug("Decode InfoType 1")
    fields_found = {}
    """
    match infos["subType"]:
        case 0 :
            fields_found["subType"]="OFF"
        case 1 :
            fields_found["subType"]="ON"
        case 4 :
            fields_found["subType"]="ALL_OFF"
        case 5 :
            fields_found["subType"]="ALL_ON"
        case _ :
            fields_found["subType"]=infos["subType"]
    """

    fields_found["subType"]=infos.get("subTypeMeaning")
    if fields_found["subType"] == None or fields_found["subType"] == "" : fields_found["subType"]=infos.get("subType")

    fields_found["id"]=infos["id"]
    fields_found["command"]=fields_found["subType"]
# # Voir pour différencier le Bouton G [All] dans un ID particulier Test sur ALL_ON ou OFF car sinon reprend l'ID du Bp1
    if fields_found["command"] == "ALL_ON" or fields_found["command"] == "ALL_OFF":
        fields_found["id"]=infos["id"]+"G"

    if fields_found["id"]!="0" or allowEmptyID:
        return fields_found

def infoType_2_decode(infos:list,allowEmptyID:bool=False) -> list:
    if infotypes_debug: log.debug("Decode InfoType 2: %s",str(infos))
    fields_found = {}
    binQualifier=int(infos["qualifier"])
    try:
        match infos["subType"]:
            case "0" :
                fields_found["subType"]="SENSOR"
                fields_found["tamper"]=(binQualifier >> 1) & 0x01
                fields_found["alarm"]=(binQualifier >> 2) &0x01
                fields_found["battery_level"]=(1-((binQualifier >> 3) &0x01))*100
                fields_found["battery_level_unit"]="%"
                fields_found["supervisor"]=(binQualifier >> 2) &0x04
            case "1" :
                fields_found["subType"]="REMOTE"
                fields_found["button1"]=binQualifier==0x08
                fields_found["button2"]=binQualifier==0x10
                fields_found["button3"]=binQualifier==0x20
                fields_found["button4"]=binQualifier==0x40
    except Exception as ex:
        log.debug("Erreur décodage infotype2 - qualifier : %s => %s",str(binQualifier),ex)    
        log.debug("infos : %s",str(infos)) 
    fields_found["id"]=infos["id"]

    if fields_found["id"]!="0" or allowEmptyID:
        return fields_found

def infoType_3_decode(infos:list,allowEmptyID:bool=False) -> list:
    if infotypes_debug: log.debug("Decode InfoType 3")
    fields_found = {}
    fields_found["subType"]=infos["subTypeMeaning"]
    if fields_found["subType"] == None or fields_found["subType"] == "" : fields_found["subType"]=infos.get("subType")
    match int(infos["qualifier"]):
        case 1 :
            fields_found["qualifier"]="OFF"
        case 4 : 
            fields_found["qualifier"]="MY"
        case 7 : 
            fields_found["qualifier"]="ON"
        case 13 : 
            fields_found["qualifier"]="ASSOC"
        case 5 : 
            fields_found["qualifier"]="LBUTTON"
        case 6 : 
            fields_found["qualifier"]="RBUTTON"

    fields_found["id"]=infos["id"]

    if fields_found["id"]!="0" or allowEmptyID:
        return fields_found

def infoType_4_decode(infos:list,allowEmptyID:bool=False) -> list:
    if infotypes_debug: log.debug("Decode InfoType 4")
    fields_found = {}
    
    fields_found["subType"]=infos.get("subTypeMeaning")
    if fields_found["subType"] == None or fields_found["subType"] == "" : fields_found["subType"]=infos.get("subType")
    fields_found["id_PHY"]= infos["id_PHYMeaning"]
    fields_found["adr_channel"]=infos["adr_channel"]
    fields_found["qualifier"]=infos["qualifier"]
    fields_found["battery_level"]=(1-int(infos["lowBatt"]))*100
    fields_found["battery_level_unit"]="%"

    match int(infos["qualifier"])>>4:
        case 1 :
            fields_found["oreg_protocol"]="V1"
        case 2 : 
            fields_found["oreg_protocol"]="V2"
        case 3 : 
            fields_found["oreg_protocol"]="V3"
    elements={'temperature':'°C','hygrometry':'%'}
    for measure in infos["measures"]:
        #log.debug("%s",str(measure))
        if measure['type'] in elements:
            fields_found[measure['type']]= measure['value']
            if elements[measure['type']] != '':
                fields_found[measure['type']+'_unit']= elements[measure['type']]

    fields_found["id"]=infos["adr_channel"]
    
    if fields_found["id"]!="0" or allowEmptyID:
        return fields_found
    
def infoType_5_decode(infos:list,allowEmptyID:bool=False) -> list:
    if infotypes_debug: log.debug("Decode InfoType 5")
    fields_found = {}
    
    fields_found["subType"]=infos.get("subTypeMeaning")
    if fields_found["subType"] == None or fields_found["subType"] == "" : fields_found["subType"]=infos.get("subType")
    fields_found["id_PHY"]= infos["id_PHYMeaning"]
    fields_found["adr_channel"]=infos["adr_channel"]
    fields_found["battery_level"]=(1-int(infos["lowBatt"]))*100
    fields_found["battery_level_unit"]="%"
    fields_found["battery_unit"]="%"

    match int(infos["qualifier"])>>4:
        case 1 :
            fields_found["oreg_protocol"]="V1"
        case 2 : 
            fields_found["oreg_protocol"]="V2"
        case 3 : 
            fields_found["oreg_protocol"]="V3"
    elements={'temperature':'°C','hygrometry':'%','pressure':'hPa'}
    for measure in infos["measures"]:
        if measure['type'] in elements:
            fields_found[measure['type']]= measure['value']
            if elements[measure['type']] != '':
                fields_found[measure['type']+'_unit']= elements[measure['type']]

    fields_found["id"]=infos["adr_channel"]
    
    if fields_found["id"]!="0" or allowEmptyID:
        return fields_found

def infoType_6_decode(infos:list,allowEmptyID:bool=False) -> list:
    if infotypes_debug: log.debug("Decode InfoType 6")
    fields_found = {}
    
    fields_found["subType"]=infos.get("subTypeMeaning")
    if fields_found["subType"] == None or fields_found["subType"] == "" : fields_found["subType"]=infos.get("subType")
    fields_found["id_PHY"]= infos["id_PHYMeaning"]
    fields_found["adr_channel"]=infos["adr_channel"]
    fields_found["qualifier"]=infos["qualifier"]
    fields_found["battery_level"]=(1-int(infos["lowBatt"]))*100
    fields_found["battery_level_unit"]="%"
    
    match int(infos["qualifier"])>>4:
        case 1 :
            fields_found["oreg_protocol"]="V1"
        case 2 : 
            fields_found["oreg_protocol"]="V2"
        case 3 : 
            fields_found["oreg_protocol"]="V3"
    elements={'speed':'m/s','direction':'°'}
    for measure in infos["measures"]:
        if measure['type'] in elements:
            fields_found[measure['type']]= measure['value']
            if elements[measure['type']] != '':
                fields_found[measure['type']+'_unit']= elements[measure['type']]

    fields_found["id"]=infos["adr_channel"]
    
    if fields_found["id"]!="0" or allowEmptyID:
        return fields_found

def infoType_7_decode(infos:list,allowEmptyID:bool=False) -> list:
    if infotypes_debug: log.debug("Decode InfoType 7")
    fields_found = {}
    
    fields_found["subType"]=infos.get("subTypeMeaning")
    if fields_found["subType"] == None or fields_found["subType"] == "" : fields_found["subType"]=infos.get("subType")
    fields_found["id_PHY"]= infos["id_PHYMeaning"]
    fields_found["adr_channel"]=infos["adr_channel"]
    fields_found["qualifier"]=infos["qualifier"]
    fields_found["battery_level"]=(1-int(infos["lowBatt"]))*100
    fields_found["battery_level_unit"]="%"
    
    match int(infos["qualifier"])>>4:
        case 1 :
            fields_found["oreg_protocol"]="V1"
        case 2 : 
            fields_found["oreg_protocol"]="V2"
        case 3 : 
            fields_found["oreg_protocol"]="V3"
    elements={'UV':'UV index'}
    for measure in infos["measures"]:
        if measure['type'] in elements:
            fields_found[measure['type']]= measure['value']
            if elements[measure['type']] != '':
                fields_found[measure['type']+'_unit']= elements[measure['type']]

    fields_found["id"]=infos["adr_channel"]
    
    if fields_found["id"]!="0" or allowEmptyID:
        return fields_found

def infoType_8_decode(infos:list,allowEmptyID:bool=False) -> list:
    if infotypes_debug: log.debug("Decode InfoType 8")
    fields_found = {}
    
    fields_found["subType"]=infos.get("subTypeMeaning")
    if fields_found["subType"] == None or fields_found["subType"] == "" : fields_found["subType"]=infos.get("subType")
    fields_found["id_PHY"]= infos["id_PHYMeaning"]
    fields_found["adr_channel"]=infos["adr_channel"]
    fields_found["qualifier"]=infos["qualifier"]
    fields_found["battery_level"]=(1-int(infos["lowBatt"]))*100
    fields_found["battery_level_unit"]="%"
    
    match int(infos["qualifier"])>>1:
        case 0 :
            fields_found["measurement"]="General"
        case 1 : 
            fields_found["oreg_protocol"]="Detailed"

    elements={'energy':'Wh','power':'W','P1':'W','P2':'W','P3':'W'}
    for measure in infos["measures"]:
        if measure['type'] in elements:
            fields_found[measure['type']]= measure['value']
            if elements[measure['type']] != '':
                fields_found[measure['type']+'_unit']= elements[measure['type']]

    fields_found["id"]=infos["adr_channel"]
    
    if fields_found["id"]!="0" or allowEmptyID:
        return fields_found

def infoType_9_decode(infos:list,allowEmptyID:bool=False) -> list:
    if infotypes_debug: log.debug("Decode InfoType 9")
    fields_found = {}
    
    fields_found["subType"]=infos.get("subTypeMeaning")
    if fields_found["subType"] == None or fields_found["subType"] == "" : fields_found["subType"]=infos.get("subType")
    fields_found["id_PHY"]= infos["id_PHYMeaning"]
    fields_found["id_channel"]=infos["id_channel"]
    fields_found["qualifier"]=infos["qualifier"]
    fields_found["battery_level"]=(1-int(infos["lowBatt"]))*100
    fields_found["battery_level_unit"]="%"
    
    match int(infos["qualifier"])>>4:
        case 1 :
            fields_found["oreg_protocol"]="V1"
        case 2 : 
            fields_found["oreg_protocol"]="V2"
        case 3 : 
            fields_found["oreg_protocol"]="V3"
    elements={'TotalRain':'mm','Rain':'mm'}
    for measure in infos["measures"]:
        if measure['type'] in elements:
            fields_found[measure['type']]= measure['value']
            if elements[measure['type']] != '':
                fields_found[measure['type']+'_unit']= elements[measure['type']]

    fields_found["id"]=infos["id_channel"]
    
    if fields_found["id"]!="0" or allowEmptyID:
        return fields_found

def infoType_10_decode(infos:list,allowEmptyID:bool=False) -> list:
    if infotypes_debug: log.debug("Decode InfoType 10")
    fields_found = {}
    
    fields_found["subType"]=infos.get("subTypeMeaning")
    if fields_found["subType"] == None or fields_found["subType"] == "" : fields_found["subType"]=infos.get("subType")
    fields_found["qualifier"]=infos["qualifier"]
   
    elements={'functionMeaning':'','stateMeaning':'','modeMeaning':'','d0':'','d1':'','d2':'','d3':''}
    for measure,value in infos.items():
        if measure in elements:
            fields_found[measure] = value
            if elements[measure] != '':
                fields_found[measure+'_unit']= elements[measure]

    fields_found["id"]=infos["id"]
    
    if fields_found["id"]!="0" or allowEmptyID:
        return fields_found

def infoType_11_decode(infos:list,allowEmptyID:bool=False) -> list:
    if infotypes_debug: log.debug("Decode InfoType 11 : %d",infos)
    fields_found = {}
    
    fields_found["subType"]=infos.get("subTypeMeaning")
    if fields_found["subType"] == None or fields_found["subType"] == "" : fields_found["subType"]=infos.get("subType")
    fields_found["qualifier"]=infos["qualifier"]

    elements={'functionMeaning':'','stateMeaning':'','modeMeaning':'','d0':'','d1':'','d2':'','d3':''}
    for measure,value in infos.items():
        if measure in elements:
            fields_found[measure] = value
            if elements[measure] != '':
                fields_found[measure+'_unit']= elements[measure]

    if 'flags' in infos['qualifierMeaning']:
        for flag in infos['qualifierMeaning']['flags']:
            fields_found[flag]=1

    fields_found["id"]=infos["id"]
    
    if fields_found["id"]!="0" or allowEmptyID:
        return fields_found
    
def infoType_13_decode(infos:list,allowEmptyID:bool=False) -> list:
    if infotypes_debug: log.debug("Decode InfoType 13: %d",infos)
    fields_found = {}
    
    fields_found["subType"]=infos.get("subTypeMeaning")
    if fields_found["subType"] == None or fields_found["subType"] == "" : fields_found["subType"]=infos.get("subType")
    fields_found["qualifier"]=infos["qualifier"]

    elements={'cnt1':'Wh','cnt2':'Wh','power':'W'}
    for measure in infos["measures"]:
        if measure['type'] in elements:
            fields_found[measure['type']]= measure['value']
            if elements[measure['type']] != '':
                fields_found[measure['type']+'_unit']= elements[measure['type']]

    fields_found["id"]=infos["id"]
    
    if fields_found["id"]!="0" or allowEmptyID:
        return fields_found
    
def infoType_15_decode(infos:list,allowEmptyID:bool=False) -> list:
    if infotypes_debug: log.debug("Decode InfoType 15 : %d",infos)
    fields_found = {}
   
    fields_found["subType"]=infos.get("subTypeMeaning")
    if fields_found["subType"] == None or fields_found["subType"] == "" : fields_found["subType"]=infos.get("subType")
    fields_found["qualifier"]=infos["qualifier"]

    #fields_found["info"]=infos.get("infoMeaning")
    Fields_Infos=infos.get("infoMeaning").split(",")
    fields_found["model"]=Fields_Infos[0]
    fields_found["battery"]=Fields_Infos[1].split("V")[0] #supression du V dans info bat
    fields_found["battery_unit"]="V"

    fields_found["button"]=int(infos["subType"]) #Ajout d'une info button pour remonter en numérique l'info de la cde 

    match fields_found["subType"]:
        case "NULL" :
            fields_found["command"]=fields_found["subType"]    
        case "ON" :
            fields_found["command"]=fields_found["subType"]
        case "OFF" :
            fields_found["command"]=fields_found["subType"]
        case "TOGGLE" :
            fields_found["command"]=fields_found["subType"]
        case "DIM" :
            fields_found["command"]=fields_found["subType"]
            fields_found["dim"]=infos["add0"]
            fields_found["dim_unit"]=infos["add0"]
        case "DIM-UP" :
            fields_found["command"]=fields_found["subType"]
        case "DIM-DOWN" :
            fields_found["command"]=fields_found["subType"]
        case "DIM-A" :
            fields_found["command"]=fields_found["subType"]
        case "DIM-STOP" :
            fields_found["command"]=fields_found["subType"]
        case "SHUTTER_OPEN" :
            fields_found["command"]=fields_found["subType"]
        case "SHUTTER_CLOSE" :
            fields_found["command"]=fields_found["subType"]
        case "SHUTTER_STOP" :
            fields_found["command"]=fields_found["subType"]
        case "RGB" :
            fields_found["command"]=fields_found["subType"]
            fields_found["debug"]=infos
        case "RGB_C" :
            fields_found["command"]=fields_found["subType"]
        case "RGB_PLUS" :
            fields_found["command"]=fields_found["subType"]
        case "OPEN_SLOW" :
            fields_found["command"]=fields_found["subType"]
        case "SET_SHORT" :
            fields_found["command"]=fields_found["subType"]
        case "SET_5S" :
            fields_found["command"]=fields_found["subType"]
        case "SET_10S" :
            fields_found["command"]=fields_found["subType"]
        case "STUDY" :
            fields_found["command"]=fields_found["subType"]
        case "DEL_BUTTON" :
            fields_found["command"]=fields_found["subType"]
        case "DEL_ALL" :
            fields_found["command"]=fields_found["subType"]
        case "SET_TEMPERATURE" :
            fields_found["command"]=fields_found["subType"]
            fields_found["temperature"]=int(infos['add0'])*0.01
            fields_found["temperature_unit"]="°C"
###
            ## A vérifier si existe un modele qui a l'hygro
            ##fields_found["hygrometry"]=int(infos['add1'])*0.01
            ##fields_found["hygrometry_unit"]="%"
            ##fields_found["debug"]=infos
###

        case "DOOR_OPEN" :
            fields_found["command"]=fields_found["subType"]
        case "BROADCAST_QUERY" :
            fields_found["command"]=fields_found["subType"]
        case "QUERY_STATUS" :
            fields_found["command"]=fields_found["subType"]
        case "REPORT_STATUS" :
            fields_found["command"]=fields_found["subType"]
            fields_found["debug"]=infos
        case "READ_CUSTOM" :
            fields_found["command"]=fields_found["subType"]
        case "SAVE_CUSTOM" :
            fields_found["command"]=fields_found["subType"]
            fields_found["debug"]=infos
        case "REPORT_CUSTOM" :
            fields_found["command"]=fields_found["subType"]
            fields_found["debug"]=infos
        case "SET_SHORT_DIMMER" :
            fields_found["command"]=fields_found["subType"]
            fields_found["debug"]=infos
        case "SET_SHORT_SENSOR" :
            fields_found["command"]=fields_found["subType"]
            fields_found["debug"]=infos

        # #Traduction complémentaire : 0x01 ON , 0x02 ARRET , 0x61(97) HG, 0x62(98) ECO , 0x63(99) CONFORT
        case "1" :
            fields_found["subType"]="ON"
            fields_found["command"]=fields_found["subType"]
        case "2" :
            fields_found["subType"]="ARRET"
            fields_found["command"]=fields_found["subType"]
        case "97" :
            fields_found["subType"]="HG"
            fields_found["command"]=fields_found["subType"]
        case "98" :
            fields_found["subType"]="ECO"
            fields_found["command"]=fields_found["subType"]
        case "99" :
            fields_found["subType"]="CONFORT"
            fields_found["command"]=fields_found["subType"]

        case _ :
            fields_found["command"]=fields_found["subType"]
            fields_found["debug"]=infos

    fields_found["id"]=infos["id"]
    
# # permet de différencier le N° du Bp => plusieurs entités 
    if fields_found["model"] == "EMITRBTN": # Voir si l'on prend le subtype !
        fields_found["id"]=infos["id"]+"-"+infos["qualifier"]
# #
    if fields_found["id"]!="0" or allowEmptyID:
        return fields_found
