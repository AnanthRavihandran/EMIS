import pandas as pd 
import json
import os
import configparser
import ast

def Procedure(data):
    procedure_df.loc[len(procedure_df.index)] = [data['id'], data['status'], str(data['code']['coding'][0]['code'])+"-"+str(data['code']['coding'][0]['display']), data['subject']['reference'], data['encounter']['reference'], data['performedPeriod']['start'], data['performedPeriod']['end'], data['location']['display']]

def Medication(data):
    medication_df.loc[len(medication_df.index)] = [data['id'], data['code']['coding'][0]['code'], data['code']['coding'][0]['display'], data['status']]

def DiagnosticReport(data):
    diagnosticreport_df.loc[len(diagnosticreport_df.index)] = [data['id'],data['status'],data['category'][0]['coding'][0]['code']+"-"+data['category'][0]['coding'][0]['display'],data['code']['coding'][0]['code']+"-"+data['code']['coding'][0]['display'],data['subject']['reference'],data['encounter']['reference'],data['effectiveDateTime'],data['issued'],data['performer'][0]['display']]
    if 'result' in data:
        diagnosticreportresult_df.loc[len(diagnosticreportresult_df.index)] = [data['id'],data['result'][0]['reference'],data['result'][0]['display']]

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
    if 'itemCodeableConcept' in data:
        code =  data['itemCodeableConcept']['coding'][0]['code']
        display = data['itemCodeableConcept']['coding'][0]['display']
    else:
        code =""
        display =""
    supplydelivery_df.loc[len(supplydelivery_df.index)] = [data['id'], data['status'],data['patient']['reference'], data['type']['coding'][0]['display'],data['suppliedItem']['quantity']['value'],code,display, data['occurrenceDateTime'] ]

def DocumentReference(data):
    identifier_system = []
    identifier_value = []
    type_code = []
    type_name = []
    category_name = []
    author =[]
    for identifier in data['identifier']:
        identifier_system.append(identifier['system'])
        identifier_value.append(identifier['value'])
    for type in data['type']['coding']:
        type_code.append(type['code'])
        type_name.append(type['display'])
    for category in data['category'][0]['coding']:
        category_name.append(category['display'])
    for author in data['author']:
        author.append(author['display'])
    for content in data['content']:
        documentreference_file_df.loc[len(documentreference_file_df.index)] =[data['id'],content['attachment']['contentType'],content['attachment']['data'],content['format']['code'],content['format']['display']]
    if 'period' in data:
        start = data['period']['start']
        end = data['period']['end']
    else:
        start = ""
        end = ""
    documentreference_df.loc[len(documentreference_df.index)] = [data['id'],identifier_system,identifier_value,data['status'],type_code,type_name,category_name,data['subject']['reference'],data['date'],author,data['custodian']['display'],data['context']['encounter'][0]['reference'],start,end]
       
def Provenance(data):
    reference_list = []
    for target in data['target']:
        reference_list.append(target['reference'])
    procedure_df.loc[len(procedure_df.index)] = [data['id'],reference_list,data['recorded']]
    for agent in data['agent']:
        provenance_participant_df.loc[len(provenance_participant_df.index)] = [data['id'], agent['type']['text'], agent['who']['display'],agent['onBehalfOf']['display']]

def CareTeam(data):
    reasoncode = []
    reasoncode_name = []
    if 'end' in data:
        period_end = data['period']['end']
    else:
        period_end = ""
    for participant in data['participant']:
        careteam_participant_df.loc[len(careteam_participant_df.index)] = [data['id'],participant['role'][0]['coding'][0]['code'],participant['role'][0]['coding'][0]['display'],participant['member']['display']]
    if 'reasonCode' in  data:
        for reasoncode in data['reasonCode']:
            reasoncode.append(reasoncode['coding'][0]['code'])
            reasoncode_name.append(reasoncode['coding'][0]['display'])
    careteam_df.loc[len(careteam_df.index)] = [data['id'],data['status'],data['subject']['reference'],data['encounter']['reference'],data['period']['start'],period_end,reasoncode,reasoncode_name,data['managingOrganization'][0]['display']]

def ImagingStudy(data):
    imagingstudy_df.loc[len(imagingstudy_df.index)] = [data['id'],data['identifier'][0]['system'],data['identifier'][0]['value'],data['status'],data['subject']['reference'],data['encounter']['reference'],data['started'],data['numberOfSeries'],data['numberOfInstances'],data['procedureCode'][0]['coding'][0]['code'],data['procedureCode'][0]['coding'][0]['display'],data['location']['display'])
    for series in data['series']:
        imagingStudy_series_df.loc[len(imagingStudy_series_df.index)] = [data['id'],series['uid'],series['number'],series['modality']['code'],series['modality']['display'],series['numberOfInstances'],series['bodySite']['code'],series['bodySite']['display'],series['started']]
        for instance in series['instance']:
            imagingstudy_instances_df.loc[len(imagingstudy_instances_df.index)] = [data['id'],instance['uid'],instance['sopClass']['code'],instance['number'],instance['title']]

def AllergyIntolerance(data):
    allergyintolerance_df.loc[len(allergyintolerance_df.index)] = [data['id'], data['clinicalStatus']['coding'][0]['code'],data['verificationStatus']['coding'][0]['code'],data['type'],data['category'][0],data['criticality'],data['code']['coding'][0]['code'],data['code']['coding'][0]['display'],data['patient']['reference'],data['recordedDate']]

def Encounter(data):
    encounter_df.loc[len(encounter_df.index)] = [data['id'],data['identifier'][0]['value'],data['status'],data['class']['code'],data['type'][0]['coding'][0]['code'],data['type'][0]['coding'][0]['display'],data['subject']['reference'],data['subject']['display'],data['participant'][0]['type'][0]['coding'][0]['code'],data['participant'][0]['type'][0]['coding'][0]['display'],data['participant'][0]['period']['start'],data['participant'][0]['period']['end'],data['participant'][0]['individual']['display'],data['period']['start'],data['period']['end'],data['location'][0]['location']['display'],data['serviceProvider']['display'] ]

def Condition(data):
    if 'abatementDateTime' in data:
        abatement_datetime = data['abatementDateTime']
    else:
        abatement_datetime = ""
    condition_df.loc[len(condition_df.index)] = [data['id'],data['clinicalStatus']['coding'][0]['code'],data['verificationStatus']['coding'][0]['code'],data['category'][0]['coding'][0]['code'],data['code']['coding'][0]['code'],data['code']['coding'][0]['display'],data['subject']['reference'],data['encounter']['reference'],data['onsetDateTime'],abatement_datetime,data['recordedDate']]

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
    immunization_df.loc[len(immunization_df.index)] = [data['id'], data['status'],data['patient']['reference'],data['occurrenceDateTime'],data['primarySource'],data['location']['display']]
    for vaccinecode in data['vaccineCode']['coding']:
        immunization_vaccineCode_df.loc[len(immunization_vaccineCode_df.index)] = [data['id'], vaccinecode['code'], vaccinecode['display']]

def CarePlan(data):
    category_code =[]
    category_name = []
    for category in data['category']:
        category_code.append(category['coding'][0]['code'])
        if 'display' in category['coding'][0]:
            category_name.append(category['coding'][0]['display'])
        else:
            category_name.append(" ")
    if 'addresses' in data:
       address = data['addresses'][0]['reference']
    else:
        address = ""
    careplan_df.loc[len(careplan_df.index)] = [data['id'], data['status'],data['intent'],category_code,category_name,data['subject']['reference'],data['encounter']['reference'],data['period']['start'],data['period']['end'],data['careTeam'][0]['reference'],address]
    if 'activity' in data:
        for activity in data['activity']:
            careplan_activity_df.loc[len(careplan_activity_df.index)] = [data['id'],activity['detail']['code']['coding'][0]['code'],activity['detail']['code']['coding'][0]['display'],activity['detail']['status'],activity['detail']['location']['display']]

def MedicationAdministration(data):
    if 'reasonReference' in data:
        reason_reference = data['reasonReference'][0]['reference']
    else:
        reason_reference = ""
    medicationadministration_df.loc[len(medicationadministration_df.index)] = [data['id'],data['status'],data['medicationCodeableConcept']['coding'][0]['code'], data['medicationCodeableConcept']['coding'][0]['display'], data['subject']['reference'],data['context']['reference'],data['effectiveDateTime'],reason_reference]

def Device(data):
    device_df.loc[len(device_df.index)] = [data['id'], data['udiCarrier'][0]['deviceIdentifier'], data['udiCarrier'][0]['carrierHRF'],data['status'],data['distinctIdentifier'],data['manufactureDate'],data['expirationDate'],data['lotNumber'],data['serialNumber'],data['deviceName'][0]['name'],data['type']['coding'][0]['code'],data['patient']['reference']]

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
                Device(data['resource'])
            elif data['resource']['resourceType'] == 'MedicationAdministration':
                MedicationAdministration(data['resource'])
            elif data['resource']['resourceType'] == 'CarePlan':
                CarePlan(data['resource'])
            elif data['resource']['resourceType'] == 'Immunization':
                Immunization(data['resource'])
            elif data['resource']['resourceType'] == 'Observation':
                Observation(data['resource'])
            elif data['resource']['resourceType'] == 'Claim':
                Claim(data['resource'])
            elif data['resource']['resourceType'] == 'MedicationRequest':
                MedicationRequest(data['resource'])
            elif data['resource']['resourceType'] == 'Condition':
                Condition(data['resource'])
            elif data['resource']['resourceType'] == 'Encounter':
                Encounter(data['resource'])
            elif data['resource']['resourceType'] == 'AllergyIntolerance':
                AllergyIntolerance(data['resource'])
            elif data['resource']['resourceType'] == 'ImagingStudy':
                ImagingStudy(data['resource'])
            elif data['resource']['resourceType'] == 'CareTeam':
                CareTeam(data['resource'])
            elif data['resource']['resourceType'] == 'Provenance':
                Provenance(data['resource'])
            elif data['resource']['resourceType'] == 'DocumentReference':
                DocumentReference(data['resource'])
            elif data['resource']['resourceType'] == 'SupplyDelivery':
                SupplyDelivery(data['resource'])
            elif data['resource']['resourceType'] == 'ExplanationOfBenefit':
                ExplanationOfBenefit(data['resource'])
            elif data['resource']['resourceType'] == 'DiagnosticReport':
                DiagnosticReport(data['resource'])
            elif data['resource']['resourceType'] == 'Medication':
                Medication(data['resource'])
            else:
                Procedure(data['resource'])
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
        diagnosticreport_cols = ast.literal_eval(config.get("data_category", "DiagnosticReport"))
        diagnosticreport_df = pd.DataFrame(columns=diagnosticreport_cols)
        diagnosticreportresult_cols = ast.literal_eval(config.get("data_category", "DiagnosticReportResult"))
        diagnosticreportresult_df = pd.DataFrame(columns=diagnosticreportresult_cols)
        supplydelivery_cols = ast.literal_eval(config.get("data_category", "SupplyDelivery"))
        supplydelivery_df = pd.DataFrame(columns=supplydelivery_cols)
        device_cols = ast.literal_eval(config.get("data_category", "Device"))
        device_df = pd.DataFrame(columns=device_cols)
        medicationadministration_cols = ast.literal_eval(config.get("data_category", "MedicationAdministration"))
        medicationadministration_df = pd.DataFrame(columns=medicationadministration_cols)
        immunization_cols = ast.literal_eval(config.get("data_category", "Immunization"))
        immunization_df = pd.DataFrame(columns=immunization_cols)
        immunization_vaccineCode_cols = ast.literal_eval(config.get("data_category", "Immunization_vaccineCode"))
        immunization_vaccineCode_df = pd.DataFrame(columns=immunization_vaccineCode_cols)
        allergyintolerance_cols = ast.literal_eval(config.get("data_category", "AllergyIntolerance"))
        allergyintolerance_df = pd.DataFrame(columns=allergyintolerance_cols)
        encounter_cols = ast.literal_eval(config.get("data_category", "Encounter"))
        encounter_df = pd.DataFrame(columns=encounter_cols)
        condition_cols = ast.literal_eval(config.get("data_category", "Condition"))
        condition_df = pd.DataFrame(columns=condition_cols)
        provenance_cols = ast.literal_eval(config.get("data_category", "Provenance"))
        provenance_df = pd.DataFrame(columns=provenance_cols)
        provenance_participant_cols = ast.literal_eval(config.get("data_category", "Provenance_participant"))
        provenance_participant_df = pd.DataFrame(columns=provenance_participant_cols)
        careteam_cols = ast.literal_eval(config.get("data_category", "CareTeam"))
        careteam_df = pd.DataFrame(columns=careteam_cols)
        careteam_participant_cols = ast.literal_eval(config.get("data_category", "CareTeam_Participant"))
        careteam_participant_df = pd.DataFrame(columns=careteam_participant_cols)
        imagingstudy_cols = ast.literal_eval(config.get("data_category", "ImagingStudy"))
        imagingstudy_df = pd.DataFrame(columns=imagingstudy_cols)
        imagingStudy_series_cols = ast.literal_eval(config.get("data_category", "ImagingStudy_series"))
        imagingStudy_series_df = pd.DataFrame(columns=imagingStudy_series_cols)
        imagingstudy_instances_cols = ast.literal_eval(config.get("data_category", "ImagingStudy_instances"))
        imagingstudy_instances_df = pd.DataFrame(columns=imagingstudy_instances_cols)
        careplan_cols = ast.literal_eval(config.get("data_category", "CarePlan"))
        careplan_df = pd.DataFrame(columns=careplan_cols)
        careplan_activity_cols = ast.literal_eval(config.get("data_category", "careplan_activity_cols"))
        careplan_activity_df = pd.DataFrame(columns=careplan_activity_cols)

        documentreference_cols = ast.literal_eval(config.get("data_category", "DocumentReference"))
        documentreference_df = pd.DataFrame(columns=documentreference_cols)
        documentreference_file_cols = ast.literal_eval(config.get("data_category", "DocumentReference_file"))
        documentreference_file_df = pd.DataFrame(columns=documentreference_file_cols)




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
