import pandas as pd 
import json
import os
import sys
def Procedure(data):
    print(data['id'])
    print(data['code']['coding'][0]['code'])
    print(data['code']['coding'][0]['display'])
    print(data['status'])
    print(data['subject']['reference'])
    print(data['encounter']['reference'])
    print(data['performedPeriod']['start'])
    print(data['performedPeriod']['end'])
    print(data['location']['display'])

def Medication(data):
    print(data['id'])
    print(data['code']['coding'][0]['code'])
    print(data['code']['coding'][0]['display'])
    print(data['status'])
def DiagnosticReport(data):
    print(data['id'])
    print(data['status'])
    print(data['category'][0]['coding'][0]['code'])
    print(data['category'][0]['coding'][0]['display'])
    print(data['code']['coding'][0]['code'])
    print(data['code']['coding'][0]['display'])
    print(data['subject']['reference'])
    print(data['encounter']['reference'])
    print(data['effectiveDateTime'])
    print(data['issued'])
    print(data['performer'][0]['display'])
    if 'result' in data:
        print(data['result'][0]['reference'])
        print(data['result'][0]['display'])

def ExplanationOfBenefit(data):
    print(data['id'])
    for contained in data['contained']:
        if contained['resourceType'] == "ServiceRequest":
            print(contained['resourceType'])
            print(contained['id'])
            print(contained['status'])
            print(contained['intent'])
            print(contained['subject']['reference'])
            print(contained['requester']['reference'])
            print(contained['performer'][0]['reference'])
        else:
            print(contained['resourceType'])
            print(contained['id'])
            print(contained['status'])
            print(contained['type']['text'])
            print(contained['beneficiary']['reference'])
            print(contained['payor'][0]['display'])
    for identifier in data['identifier']:
        print(identifier['value'])
    print(data['status'])
    print(data['type']['coding'][0]['code'])
    print(data['use'])
    print(data['patient']['reference'])
    print(data['billablePeriod']['start'])
    print(data['billablePeriod']['end'])
    print(data['created'])
    print(data['insurer']['display'])
    print(data['provider']['reference'])
    print(data['referral']['reference'])
    print(data['facility']['display'])
    print(data['claim']['reference'])
    print(data['outcome'])
    for careteam in data['careTeam']:
        print(careteam['sequence'])
        print(careteam['provider']['reference'])
        print(careteam['role']['coding'][0]['display'])
    print(data['insurance'][0]['focal'])
    print(data['insurance'][0]['coverage']['display'])
    for item in data['item']:
        print(item['sequence'])
        print(item['category']['coding'][0]['code'])
        print(item['category']['coding'][0]['display'])
        print(item['productOrService']['coding'][0]['code'])
        print(item['productOrService']['coding'][0]['display'])
        print(item['servicedPeriod']['start'])
        print(item['servicedPeriod']['end'])
        print(item['locationCodeableConcept']['coding'][0]['code'])
        print(item['locationCodeableConcept']['coding'][0]['display'])
        if 'encounter' in item:
            print("encounter section")
            print(item['encounter'][0]['reference'])
        if 'net' in item:
            print("Net section")
            print(item['net']['value'])
            print(item['net']['currency'])
        if 'adjudication'in item:
            for adjudication in item['adjudication']:
                print("adjudication section")
                print(adjudication['category']['coding'][0]['display'])
                if 'amount' in adjudication:
                    print("price:"+str(adjudication['amount']['value']))
                    print(adjudication['amount']['currency'])

def SupplyDelivery(data):
    print(data['id'])
    print(data['status'])
    print(data['patient']['reference'])
    for type in data['type']['coding']:
        print(type['display'])
    print(data['suppliedItem']['quantity']['value'])
    if 'itemCodeableConcept' in data:
        for itemcodeableconcept in data['itemCodeableConcept']['coding']:
            print(itemcodeableconcept['code'])
            print(itemcodeableconcept['display'])
    print(data['occurrenceDateTime'])

def DocumentReference(data):
    print(data['id'])
    for identifier in data['identifier']:
        print(identifier['system'])
        print(identifier['value'])
    print(data['status'])
    for type in data['type']['coding']:
        print(type['code'])
        print(type['display'])
    for category in data['category'][0]['coding']:
        print(category['code'])
        print(category['display'])
    print(data['subject']['reference'])
    print(data['date'])
    for author in data['author']:
        print(author['display'])
    print(data['custodian']['display'])
    for content in data['content']:
        print(content['attachment']['contentType'])
        print(content['attachment']['data'])
        print(content['format']['code'])
        print(content['format']['display'])
    print(data['context']['encounter'][0]['reference'])
    if 'period' in data:
        print(data['period']['start'])
        print(data['period']['end'])

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
        print(data['resource']['abatementDateTime'])
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
    print(data['id'])
    print(data['status'])
    print(data['type']['coding'][0]['code'])
    print(data['use'])
    print(data['patient']['reference'])
    if 'display' in data['patient']:
        print(data['patient']['display'])
    print(data['billablePeriod']['start'])
    print(data['billablePeriod']['end'])
    print(data['created'])
    print(data['provider']['display'])
    print(data['priority']['coding'][0]['code'])
    if 'facility' in data:
        print(data['facility']['display'])
    if 'procedure' in data:
        for procedure in data['procedure']:
            print(procedure['sequence'])
            print(procedure['procedureReference']['reference'])
        print(data['insurance'][0]['sequence'])
        print(data['insurance'][0]['focal'])
        print(data['insurance'][0]['coverage']['display'])
    for item in data['item']:
        print(item['sequence'])
        if 'procedureSequence' in item:
            print(item['procedureSequence'][0])
        print(item['productOrService']['coding'][0]['code'])
        print(item['productOrService']['coding'][0]['display'])
        if 'encounter' in item:
            print(item['encounter'][0]['reference'])
        if 'net' in item:
            print(item['net']['value'])
            print(item['net']['currency'])

    print(data['total']['value'])
    print(data['total']['currency'])

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
                Claim(data['resource'])
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
                pass
                #DocumentReference(data['resource'])
            elif data['resource']['resourceType'] == 'SupplyDelivery':
                pass
                #SupplyDelivery(data['resource'])
            elif data['resource']['resourceType'] == 'ExplanationOfBenefit':
                pass
                #ExplanationOfBenefit(data['resource'])
            elif data['resource']['resourceType'] == 'DiagnosticReport':
                pass
                #DiagnosticReport(data['resource'])
            elif data['resource']['resourceType'] == 'Medication':
                pass
                #Medication(data['resource'])
            elif data['resource']['resourceType'] == 'Procedure':
                pass
                #Procedure(data['resource'])


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
