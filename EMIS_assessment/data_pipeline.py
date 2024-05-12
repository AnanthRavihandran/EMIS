import pandas as pd 
import json
import os
import sys
import configparser
import ast


def Procedure(data):
    procedure_df.loc[len(procedure_df.index)] = [data['id'], data['status'], str(data['code']['coding'][0]['code'])+"-"+str(data['code']['coding'][0]['display']), data['subject']['reference'], data['encounter']['reference'], data['performedPeriod']['start'], data['performedPeriod']['end'], data['location']['display']]

def Medication(data):
    medication_df.loc[len(medication_df.index)] = [data['id'], data['code']['coding'][0]['code'], data['code']['coding'][0]['display'], data['status']]

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
    print(data['id'])
    print(data['status'])
    print(data['subject']['reference'])
    print(data['encounter']['reference'])
    print(data['period']['start'])
    if 'end' in data:
        print(data['period']['end'])
    for participant in data['participant']:
        print(participant['role'][0]['coding'][0]['code'])
        print(participant['role'][0]['coding'][0]['display'])
        print(participant['member']['display'])
    if 'reasonCode' in  data:
        for reasoncode in data['reasonCode']:
            print(reasoncode['coding'][0]['code'])
            print(reasoncode['coding'][0]['display'])
    print(data['managingOrganization'][0]['display'])


def ImagingStudy(data):
    print(data['id'])
    print(data['identifier'][0]['system'])
    print(data['identifier'][0]['value'])
    print(data['status'])
    print(data['subject']['reference'])
    print(data['encounter']['reference'])
    print(data['started'])
    print(data['numberOfSeries'])
    print(data['numberOfInstances'])
    print(data['procedureCode'][0]['coding'][0]['code'])
    print(data['procedureCode'][0]['coding'][0]['display'])
    print(data['location']['display'])
    print(data['series'][0]['uid'])
    for series in data['series']:
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
    print(data['id'])
    print(data['clinicalStatus']['coding'][0]['code'])
    print(data['verificationStatus']['coding'][0]['code'])
    print(data['type'])
    print(data['category'][0])
    print(data['criticality'])
    print(data['code']['coding'][0]['code'])
    print(data['code']['coding'][0]['display'])
    print(data['patient']['reference'])
    print(data['recordedDate'])

def Encounter(data):
    print(data['id'])
    print(data['identifier'][0]['value'])
    print(data['status'])
    print(data['class']['code'])
    print(data['type'][0]['coding'][0]['code'])
    print(data['type'][0]['coding'][0]['display'])
    print(data['subject']['reference'])
    print(data['subject']['display'])
    print(data['participant'][0]['type'][0]['coding'][0]['code'])
    print(data['participant'][0]['type'][0]['coding'][0]['display'])
    print(data['participant'][0]['period']['start'])
    print(data['participant'][0]['period']['end'])
    print(data['participant'][0]['individual']['display'])
    print(data['participant'][0]['period']['start'])
    print(data['participant'][0]['period']['end'])
    print(data['location'][0]['location']['display'])
    print(data['serviceProvider']['display'])

def Condition(data):
    print(data['id'])
    print(data['clinicalStatus']['coding'][0]['code'])
    print(data['verificationStatus']['coding'][0]['code'])
    print(data['category'][0]['coding'][0]['code'])
    print(data['code']['coding'][0]['code'])
    print(data['code']['coding'][0]['display'])
    print(data['subject']['reference'])
    print(data['encounter']['reference'])
    print(data['onsetDateTime'])
    if 'abatementDateTime' in data:
        print(data['abatementDateTime'])
    print(data['recordedDate'])

def MedicationRequest(data):
    print(data['id'])
    print(data['status'])
    print(data['intent'])
    if 'medicationCodeableConcept' in data:
        for medicationcodeableconcept in data['medicationCodeableConcept']['coding']:
            print(medicationcodeableconcept['code'])
            print(medicationcodeableconcept['display'])
    print(data['subject']['reference'])
    print(data['encounter']['reference'])
    print(data['authoredOn'])
    print(data['requester']['display'])
    if 'reasonReference' in data:
        print(data['reasonReference'][0]['reference'])
    if 'dosageInstruction' in data:
        for dosageinstruction in data['dosageInstruction']:
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
        print(data['id'])
        print(data['status'])
        for i,category in enumerate(data['category']):
            print(category['coding'][i]['code'])
        for i,code in enumerate(data['code']['coding']):
            print(code['code'])
            print(code['display'])
        print(data['subject']['reference'])
        print(data['encounter']['reference'])
        print(data['effectiveDateTime'])
        print(data['issued'])
        if 'valueQuantity' in data:
            print(data['valueQuantity']['value'])
            print(data['valueQuantity']['unit'])
        if 'valueCodeableConcept' in data:
            for code in data['valueCodeableConcept']['coding']:
                print("valuecodeableConcept")
                print(code['code'])
                print(code['display'])
        if 'component' in data:
            for component in data['component']:
                print(component['code']['coding'][0]['code'])
                print(component['code']['coding'][0]['display'])
                if 'valueQuantity' in data['component']:
                    print(component['valueQuantity']['value'])
                    print(component['valueQuantity']['unit'])
                if 'valueCodeableConcept' in data['component']:
                     print(component['valueCodeableConcept']['coding'][0]['code'])
                     print(component['valueCodeableConcept']['coding'][0]['display'])

def Immunization(data):
    print(data['id'])
    print(data['status'])
    print(data['patient']['reference'])
    print(data['encounter']['reference'])
    print(data['occurrenceDateTime'])
    print(data['primarySource'])
    print(data['location']['display'])
    for vaccinecode in data['vaccineCode']['coding']:
        print(vaccinecode['code'])
        print(vaccinecode['display'])
    

def CarePlan(data):
    print(data['id'])
    print(data['status'])
    print(data['intent'])
    for category in data['category']:
        print(category['coding'][0]['code'])
        if 'display' in category['coding'][0]:
            print(category['coding'][0]['display'])
        else:
            print('null')
    print(data['subject']['reference'])
    print(data['encounter']['reference'])
    print(data['period']['start'])
    print(data['careTeam'][0]['reference'])
    if 'addresses' in data:
        print(data['addresses'][0]['reference'])
    else:
        print('null')

    if 'activity' in data:
        for activity in data['activity']:
            print(activity['detail']['code']['coding'][0]['code'])
            print(activity['detail']['code']['coding'][0]['display'])
            print(activity['detail']['status'])
            print(activity['detail']['location']['display'])
      
def MedicationAdministration(data):
    print(data['id'])
    print(data['status'])
    print(data['medicationCodeableConcept']['coding'][0]['code'])
    print(data['medicationCodeableConcept']['coding'][0]['display'])
    print(data['subject']['reference'])
    print(data['context']['reference'])
    print(data['effectiveDateTime'])
    if 'reasonReference' in data:
        print(data['reasonReference'][0]['reference'] )
    else:
        print("NUll")
    

def Device(data):
    print(data['id'])
    print(data['udiCarrier'][0]['deviceIdentifier'])
    print(data['udiCarrier'][0]['carrierHRF'])
    print(data['status'])
    print(data['distinctIdentifier'])
    print(data['manufactureDate'])
    print(data['expirationDate'])
    print(data['lotNumber'])
    print(data['serialNumber'])
    print(data['deviceName'][0]['name'])
    print(data['type']['coding'][0]['code'])
    print(data['patient']['reference'])

def Patient(data):
    print(data['id'])
    for extension in data['extension']:
        print(extension['extension'][0]['valueCoding']['code'])
        print(extension['extension'][0]['valueCoding']['display'])
    for i,identifier in enumerate(data['identifier']):
        if i !=0:
            print(identifier['type']['coding'][0]['code'])
            print(identifier['value'])
    print(str(data['name'][0]['given'][0]) + str(data['name'][0]['family']))
    print(data['telecom'][0]['value'])
    print(data['telecom'][0]['use'])
    print(data['gender'])
    print(data['birthDate'])
    print(data['address'][0]['line'][0])
    print(data['address'][0]['city'])
    print(data['address'][0]['state'])
    print(data['address'][0]['country'])
    print(data['maritalStatus']['coding'][0]['code'])

def read_json_data(files,dir_location):
    for file in files:
        f = open(dir_location+file,encoding="utf8")
        data_fromat = json.load(f)
        for data in data_fromat['entry']:
            if data['resource']['resourceType'] == 'Patient':
                pass
            elif data['resource']['resourceType'] == 'Device':
                pass
                #Device(data['resource'])
            elif data['resource']['resourceType'] == 'MedicationAdministration':
                pass
                #MedicationAdministration(data['resource'])
            elif data['resource']['resourceType'] == 'CarePlan':
                pass
                #CarePlan(data['resource'])
            elif data['resource']['resourceType'] == 'Immunization':
                pass
                #Immunization(data['resource'])
            elif data['resource']['resourceType'] == 'Observation':
                pass
                #Observation(data['resource'])
            elif data['resource']['resourceType'] == 'Claim':
                pass
                #Claim(data['resource'])
            elif data['resource']['resourceType'] == 'MedicationRequest':
                pass
                #MedicationRequest(data['resource'])
            elif data['resource']['resourceType'] == 'Condition':
                pass
                #Condition(data['resource'])
            elif data['resource']['resourceType'] == 'Encounter':
                pass
                #Encounter(data['resource'])
            elif data['resource']['resourceType'] == 'AllergyIntolerance':
                pass
                #AllergyIntolerance(data['resource'])
            elif data['resource']['resourceType'] == 'ImagingStudy':
                pass
                #ImagingStudy(data['resource'])
            elif data['resource']['resourceType'] == 'CareTeam':
                pass
                #CareTeam(data['resource'])
            elif data['resource']['resourceType'] == 'Provenance':
                pass
                #Provenance(data['resource'])
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
                Medication(data['resource'])
            elif data['resource']['resourceType'] == 'Procedure':
                pass
                #Procedure(data['resource'])
        f.close()
    #procedure_df.to_csv('procedure.csv', sep=',', encoding='utf-8')
    medication_df.to_csv('medication.csv', sep=',', encoding='utf-8')

if __name__ == "__main__":
    try:
        config = configparser.ConfigParser()
        config.read('config.ini')

        procedure_cols = ast.literal_eval(config.get("data_category", "Procedure"))
        procedure_df = pd.DataFrame(columns=procedure_cols)
        medication_cols = ast.literal_eval(config.get("data_category", "Medication"))
        medication_df = pd.DataFrame(columns=medication_cols)
        print(medication_df)

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
