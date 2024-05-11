import pandas as pd 
import json
import os
import sys
def Procedure():
    pass
def Medication():
    pass
def DiagnosticReport():
    pass
def ExplanationOfBenefit():
    pass
def SupplyDelivery():
    pass
def DocumentReference(data):
    print(data)
def Provenance(data):
    print(data['id'])
    for target in data['target']:
        print(target['reference'])
    print(data['recorded'])
    for agent in data['agent']:
        print(agent['type']['text'])
        print(agent['who']['display'])
        print(agent['onBehalfOf']['display'])

def CareTeam(data):
    print(data['resource']['id'])
    print(data['resource']['status'])
    print(data['resource']['subject']['reference'])
    print(data['resource']['encounter']['reference'])
    print(data['resource']['period']['start'])
    if 'end' in data['resource']:
        print(data['resource']['period']['end'])
    for participant in data['resource']['participant']:
        print(participant['role'][0]['coding'][0]['code'])
        print(participant['role'][0]['coding'][0]['display'])
        print(participant['member']['display'])
    if 'reasonCode' in  data['resource']:
        for reasoncode in data['resource']['reasonCode']:
            print(reasoncode['coding'][0]['code'])
            print(reasoncode['coding'][0]['display'])
    print(data['resource']['managingOrganization'][0]['display'])


def ImagingStudy(data):
    print(data['resource']['id'])
    print(data['resource']['identifier'][0]['system'])
    print(data['resource']['identifier'][0]['value'])
    print(data['resource']['status'])
    print(data['resource']['subject']['reference'])
    print(data['resource']['encounter']['reference'])
    print(data['resource']['started'])
    print(data['resource']['numberOfSeries'])
    print(data['resource']['numberOfInstances'])
    print(data['resource']['procedureCode'][0]['coding'][0]['code'])
    print(data['resource']['procedureCode'][0]['coding'][0]['display'])
    print(data['resource']['location']['display'])
    print(data['resource']['series'][0]['uid'])
    for series in data['resource']['series']:
        print(series['uid'])
        print(series['number'])
        print(series['modality']['code'])
        print(series['modality']['display'])
        print(series['numberOfInstances'])
        print(series['bodySite']['code'])
        print(series['bodySite']['display'])
        print(series['started'])
        for instance in series['instance']:
            print(instance['uid'])
            print(instance['number'])
            print(instance['title'])


def AllergyIntolerance(data):
    print(data['resource']['id'])
    print(data['resource']['clinicalStatus']['coding'][0]['code'])
    print(data['resource']['verificationStatus']['coding'][0]['code'])
    print(data['resource']['type'])
    print(data['resource']['category'][0])
    print(data['resource']['criticality'])
    print(data['resource']['code']['coding'][0]['code'])
    print(data['resource']['code']['coding'][0]['display'])
    print(data['resource']['patient']['reference'])
    print(data['resource']['recordedDate'])

def Encounter(data):
    print(data['resource']['id'])
    print(data['resource']['identifier'][0]['value'])
    print(data['resource']['status'])
    print(data['resource']['class']['code'])
    print(data['resource']['type'][0]['coding'][0]['code'])
    print(data['resource']['type'][0]['coding'][0]['display'])
    print(data['resource']['subject']['reference'])
    print(data['resource']['subject']['display'])
    print(data['resource']['participant'][0]['type'][0]['coding'][0]['code'])
    print(data['resource']['participant'][0]['type'][0]['coding'][0]['display'])
    print(data['resource']['participant'][0]['period']['start'])
    print(data['resource']['participant'][0]['period']['end'])
    print(data['resource']['participant'][0]['individual']['display'])
    print(data['resource']['participant'][0]['period']['start'])
    print(data['resource']['participant'][0]['period']['end'])
    print(data['resource']['location'][0]['location']['display'])
    print(data['resource']['serviceProvider']['display'])

def Condition(data):
    print(data['resource']['id'])
    print(data['resource']['clinicalStatus']['coding'][0]['code'])
    print(data['resource']['verificationStatus']['coding'][0]['code'])
    print(data['resource']['category'][0]['coding'][0]['code'])
    print(data['resource']['code']['coding'][0]['code'])
    print(data['resource']['code']['coding'][0]['display'])
    print(data['resource']['subject']['reference'])
    print(data['resource']['encounter']['reference'])
    print(data['resource']['onsetDateTime'])
    if 'abatementDateTime' in data['resource']:
        print(print(data['resource']['abatementDateTime']))
    print(data['resource']['recordedDate'])

def MedicationRequest(data):
    print(data['resource']['id'])
    print(data['resource']['status'])
    print(data['resource']['intent'])
    if 'medicationCodeableConcept' in data['resource']:
        for medicationcodeableconcept in data['resource']['medicationCodeableConcept']['coding']:
            print(medicationcodeableconcept['code'])
            print(medicationcodeableconcept['display'])
    print(data['resource']['subject']['reference'])
    print(data['resource']['encounter']['reference'])
    print(data['resource']['authoredOn'])
    print(data['resource']['requester']['display'])
    if 'reasonReference' in data['resource']:
        print(data['resource']['reasonReference'][0]['reference'])
    if 'dosageInstruction' in data['resource']:
        for dosageinstruction in data['resource']['dosageInstruction']:
            print(dosageinstruction['sequence'])
            if 'timing' in dosageinstruction:
                print(dosageinstruction['timing']['repeat']['frequency'])
                print(dosageinstruction['timing']['repeat']['period'])
                print(dosageinstruction['timing']['repeat']['periodUnit'])
            else:
                print(dosageinstruction['text'])
            if dosageinstruction['asNeededBoolean'] == False:
                for doseandrate in dosageinstruction['doseAndRate']:
                    print(doseandrate['type']['coding'][0]['code'])
                    print(doseandrate['type']['coding'][0]['display'])
                    print(doseandrate['doseQuantity']['value'])

def Claim(data):
    print(data['resource']['id'])
    print(data['resource']['status'])

def Observation(data):
        print(data['resource']['id'])
        print(data['resource']['status'])
        for i,category in enumerate(data['resource']['category']):
            print(category['coding'][i]['code'])
        for i,code in enumerate(data['resource']['code']['coding']):
            print(code['code'])
            print(code['display'])
        print(data['resource']['subject']['reference'])
        print(data['resource']['encounter']['reference'])
        print(data['resource']['effectiveDateTime'])
        print(data['resource']['issued'])
        if 'valueQuantity' in data['resource']:
            print(data['resource']['valueQuantity']['value'])
            print(data['resource']['valueQuantity']['unit'])
        if 'valueCodeableConcept' in data['resource']:
            for code in data['resource']['valueCodeableConcept']['coding']:
                print("valuecodeableConcept")
                print(code['code'])
                print(code['display'])
        if 'component' in data['resource']:
            for component in data['resource']['component']:
                print(component['code']['coding'][0]['code'])
                print(component['code']['coding'][0]['display'])
                if 'valueQuantity' in data['resource']['component']:
                    print(component['valueQuantity']['value'])
                    print(component['valueQuantity']['unit'])
                if 'valueCodeableConcept' in data['resource']['component']:
                     print(component['valueCodeableConcept']['coding'][0]['code'])
                     print(component['valueCodeableConcept']['coding'][0]['display'])

def Immunization(data):
    print(data['resource']['id'])
    print(data['resource']['status'])
    print(data['resource']['patient']['reference'])
    print(data['resource']['encounter']['reference'])
    print(data['resource']['occurrenceDateTime'])
    print(data['resource']['primarySource'])
    print(data['resource']['location']['display'])
    for vaccinecode in data['resource']['vaccineCode']['coding']:
        print(vaccinecode['code'])
        print(vaccinecode['display'])
    

def CarePlan(data):
    print(data['resource']['id'])
    print(data['resource']['status'])
    print(data['resource']['intent'])
    for category in data['resource']['category']:
        print(category['coding'][0]['code'])
        if 'display' in category['coding'][0]:
            print(category['coding'][0]['display'])
        else:
            print('null')
    print(data['resource']['subject']['reference'])
    print(data['resource']['encounter']['reference'])
    print(data['resource']['period']['start'])
    print(data['resource']['careTeam'][0]['reference'])
    if 'addresses' in data['resource']:
        print(data['resource']['addresses'][0]['reference'])
    else:
        print('null')

    if 'activity' in data['resource']:
        for activity in data['resource']['activity']:
            print(activity['detail']['code']['coding'][0]['code'])
            print(activity['detail']['code']['coding'][0]['display'])
            print(activity['detail']['status'])
            print(activity['detail']['location']['display'])
      
def MedicationAdministration(data):
    print(data['resource']['id'])
    print(data['resource']['status'])
    print(data['resource']['medicationCodeableConcept']['coding'][0]['code'])
    print(data['resource']['medicationCodeableConcept']['coding'][0]['display'])
    print(data['resource']['subject']['reference'])
    print(data['resource']['context']['reference'])
    print(data['resource']['effectiveDateTime'])
    if 'reasonReference' in data['resource']:
        print(data['resource']['reasonReference'][0]['reference'] )
    else:
        print("NUll")
    

def Device(data):
    print(data['resource']['id'])
    print(data['resource']['udiCarrier'][0]['deviceIdentifier'])
    print(data['resource']['udiCarrier'][0]['carrierHRF'])
    print(data['resource']['status'])
    print(data['resource']['distinctIdentifier'])
    print(data['resource']['manufactureDate'])
    print(data['resource']['expirationDate'])
    print(data['resource']['lotNumber'])
    print(data['resource']['serialNumber'])
    print(data['resource']['deviceName'][0]['name'])
    print(data['resource']['type']['coding'][0]['code'])
    print(data['resource']['patient']['reference'])

def Patient(data):
    print(data['resource']['id'])
    print(data['resource']['text']['status'])
    print(data['resource']['extension'][0]['extension'][0]['valueCoding']['code'])
    print(data['resource']['extension'][0]['extension'][0]['valueCoding']['display'])
    print(data['resource']['extension'][1]['extension'][0]['valueCoding']['code'])
    print(data['resource']['extension'][1]['extension'][0]['valueCoding']['display'])
    print(data['resource']['extension'][2]['valueString'])
    print(data['resource']['extension'][3]['valueCode'])
    print(data['resource']['extension'][4]['valueAddress']['city'])
    print(data['resource']['extension'][4]['valueAddress']['state'])
    print(data['resource']['extension'][4]['valueAddress']['country'])
    print(data['resource']['extension'][5]['valueDecimal'])
    print(data['resource']['extension'][6]['valueDecimal'])
    for i,identifier in enumerate(data['resource']['identifier']):
        if i !=0:
            print(identifier['type']['coding'][0]['code'])
            print(identifier['value'])
    print(str(data['resource']['name'][0]['given'][0]) + str(data['resource']['name'][0]['family']))
    print(data['resource']['telecom'][0]['value'])
    print(data['resource']['telecom'][0]['use'])
    print(data['resource']['gender'])
    print(data['resource']['birthDate'])
    print(data['resource']['address'][0]['line'][0])
    print(data['resource']['address'][0]['city'])
    print(data['resource']['address'][0]['state'])
    print(data['resource']['address'][0]['country'])
    print(data['resource']['maritalStatus']['coding'][0]['code'])

def read_json_data(files,dir_location):
    for file in files:
        print(file)
        f = open(dir_location+file,encoding="utf8")
        data_fromat = json.load(f)
        for data in data_fromat['entry']:
            
            if data['resource']['resourceType'] == 'Patient':
                pass
                #Patient(data)
            elif data['resource']['resourceType'] == 'Device':
                pass
                #Device(data)
            elif data['resource']['resourceType'] == 'MedicationAdministration':
                pass
                #MedicationAdministration(data)
            elif data['resource']['resourceType'] == 'CarePlan':
                pass
                #CarePlan(data)
            elif data['resource']['resourceType'] == 'Immunization':
                pass
                #Immunization(data)
            elif data['resource']['resourceType'] == 'Observation':
                pass
                #Observation(data)
            elif data['resource']['resourceType'] == 'Claim':
                pass
                #Claim(data)
            elif data['resource']['resourceType'] == 'MedicationRequest':
                pass
                #MedicationRequest(data)
            elif data['resource']['resourceType'] == 'Condition':
                pass
                #Condition(data)
            elif data['resource']['resourceType'] == 'Encounter':
                pass
                #Encounter(data)
            elif data['resource']['resourceType'] == 'AllergyIntolerance':
                pass
                #AllergyIntolerance(data)
            elif data['resource']['resourceType'] == 'ImagingStudy':
                pass
                #ImagingStudy(data)
            elif data['resource']['resourceType'] == 'CareTeam':
                pass
                #CareTeam(data)
            elif data['resource']['resourceType'] == 'Provenance':
                #Provenance(data['resource'])
                pass
            elif data['resource']['resourceType'] == 'DocumentReference':
                DocumentReference(data['resource'])



        f.close()
    
if __name__ == "__main__":
    try:
        dir_location = os.path.dirname(__file__)+"\\data\\"
        isdir = os.path.isdir(dir_location)
        if isdir == True:
            file = os.listdir(dir_location)  
            if len(file)>0:
                read_json_data(file,dir_location)
                
            else:
                print("There is no file: "+ str(dir_location))
        else:
            print("The directory is not exists: "+ str(dir_location))
        #read_json_data(file,file_location)
    except Exception as e:
        print(str(e))
