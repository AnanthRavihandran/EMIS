"""
File: data_pipeline.py
Author: Ananth Ravichandran
Date: 05/14/2024
Description: Structuring the given data from the json files and then writing in CSV format .
"""

import pandas as pd
import json
import os
import configparser
import ast


# To get procedure details
def get_procedure(data):
    try:
        procedure_code = ""
        start = ""
        end = ""
        if 'code' in data:
            procedure_code = str(data['code']['coding'][0]['code'])+"-"+ str(data['code']['coding'][0]['display'])
        if 'performedPeriod' in data:
            start = data['performedPeriod']['start']
            end = data['performedPeriod']['end']

        procedure_df.loc[len(procedure_df.index)] = [data['id'], data['status'], procedure_code , data['subject']['reference'], data['encounter']['reference'], start , end, data['location']['display']]
    except Exception as e:
        print("An exception occured in get_procedure:- " + str(e))


# To get medication details
def get_medication(data):
    try:
        medication_df.loc[len(medication_df.index)] = [data['id'], data['code']['coding'][0]['code'], data['code']['coding'][0]['display'], data['status']]
    except Exception as e:
        print("An exception occured in get_medication:- " + str(e))


# To get diagnostic report details
def get_diagnostic_report(data):
    try:
        diagnostic_report_df.loc[len(diagnostic_report_df.index)] = [data['id'], data['status'], data['category'][0]['coding'][0]['code']+"-"+data['category'][0]['coding'][0]['display'], data['code']['coding'][0]['code']+"-"+data['code']['coding'][0]['display'],data['subject']['reference'], data['encounter']['reference'], data['effectiveDateTime'], data['issued'], data['performer'][0]['display']]
        if 'result' in data:
            diagnostic_report_result_df.loc[len(diagnostic_report_result_df.index)] = [data['id'], data['result'][0]['reference'], data['result'][0]['display']]
    except Exception as e:
        print("An exception occured in get_diagnostic_report:- " + str(e))


# To get benefit details
def get_explanation_of_benefit(data):
    try:
        contained_list, identifier, sequence, provider, role = ([] for i in range(5))
        for contained in data['contained']:
            if contained['resourceType'] == "ServiceRequest":
                contained_list.append([contained['resourceType'], contained['id'], contained['status'], contained['intent'], contained['subject']['reference'], contained['requester']['reference'], contained['performer'][0]['reference']])
            else:
                contained_list.append([contained['resourceType'], contained['id'], contained['status'], contained['type']['text'], contained['beneficiary']['reference'], contained['payor'][0]['display']])
        for identifiers in data['identifier']:
            identifier.append(identifiers['value'])
        for careteam in data['careTeam']:
            sequence.append(careteam['sequence'])
            provider.append(careteam['provider']['reference'])
            role.append(careteam['role']['coding'][0]['display'])
        explanation_of_benefit_df.loc[len(explanation_of_benefit_df.index)] = [data['id'], contained_list, identifier, data['status'], data['type']['coding'][0]['code'], data['use'], data['patient']['reference'], data['billablePeriod']['start'], data['billablePeriod']['end'], data['created'], data['insurer']['display'], data['provider']['reference'], data['referral']['reference'], data['facility']['display'], data['claim']['reference'], data['outcome'], sequence, provider, role, data['insurance'][0]['focal'], data['insurance'][0]['coverage']['display']]
        for item in data['item']:
            encounter = ""
            net_value = ""
            net_currency = ""
            if 'encounter' in item:
                 encounter = item['encounter'][0]['reference']
            if 'net' in item:
                net_value = item['net']['value']
                net_currency = item['net']['currency']
            explanation_of_benefit_item_df.loc[len(explanation_of_benefit_item_df.index)] = [data['id'], item['sequence'], item['category']['coding'][0]['code'], item['category']['coding'][0]['display'], item['productOrService']['coding'][0]['code'], item['productOrService']['coding'][0]['display'], item['servicedPeriod']['start'], item['servicedPeriod']['end'], item['locationCodeableConcept']['coding'][0]['code'], item['locationCodeableConcept']['coding'][0]['display'], encounter, net_value, net_currency]
            if 'adjudication' in item:
                for adjudication in item['adjudication']:
                    amount = ""
                    currency = ""
                    if 'amount' in adjudication:
                        amount = adjudication['amount']['value']
                        currency = adjudication['amount']['currency']
                    explanation_of_benefit_adjudication_df.loc[len(explanation_of_benefit_adjudication_df.index)] = [data['id'], adjudication['category']['coding'][0]['display'], amount, currency]
    except Exception as e:
        print("An exception occured in get_explanation_of_benefit:- " + str(e))


# To get supply delivery details 
def get_supply_delivery(data):
    try:
        code = ""
        display = ""
        if 'itemCodeableConcept' in data:
            code = data['itemCodeableConcept']['coding'][0]['code']
            display = data['itemCodeableConcept']['coding'][0]['display']
        supply_delivery_df.loc[len(supply_delivery_df.index)] = [data['id'], data['status'], data['patient']['reference'], data['type']['coding'][0]['display'], data['suppliedItem']['quantity']['value'], code, display, data['occurrenceDateTime']]
    except Exception as e:
        print("An exception occured in get_supply_delivery:- " + str(e))


# To get document ref details
def get_document_reference(data):
    try:
        start = ""
        end = ""
        type_code = []
        type_name = []
        for type in data['type']['coding']:
            type_code.append(type['code'])
            type_name.append(type['display'])
        for content in data['content']:
            document_reference_file_df.loc[len(document_reference_file_df.index)] =[data['id'], content['attachment']['contentType'], content['attachment']['data'], content['format']['code'], content['format']['display']]
        if 'period' in data:
            start = data['period']['start']
            end = data['period']['end']
        document_reference_df.loc[len(document_reference_df.index)] = [data['id'], data['identifier'][0]['system'], data['identifier'][0]['value'], data['status'], type_code, type_name, data['category'][0]['coding'][0]['display'], data['subject']['reference'], data['date'],  data['author'][0]['display'], data['custodian']['display'], data['context']['encounter'][0]['reference'], start, end]
    except Exception as e:
        print("An exception occured in get_document_reference:- " + str(e))


# To get provenance details
def get_provenance(data):
    try:
        reference_list = []
        for target in data['target']:
            reference_list.append(target['reference'])
        provenance_df.loc[len(provenance_df.index)] = [data['id'], reference_list, data['recorded']]
        for agent in data['agent']:
            provenance_participant_df.loc[len(provenance_participant_df.index)] = [data['id'], agent['type']['text'], agent['who']['display'], agent['onBehalfOf']['display']]
    except Exception as e:
        print("An exception occured in get_provenance:- " + str(e))


# To get care team details
def get_care_team(data):
    try:
        period_end = ""
        reason_code_list = []
        reason_code_name = []
        if 'end' in data:
            period_end = data['period']['end']
        for participant in data['participant']:
            care_team_participant_df.loc[len(care_team_participant_df.index)] = [data['id'], participant['role'][0]['coding'][0]['code'], participant['role'][0]['coding'][0]['display'], participant['member']['display']]
        if 'reasonCode' in data:
            for reason_code in data['reasonCode']:
                reason_code_list.append(reason_code['coding'][0]['code'])
                reason_code_name.append(reason_code['coding'][0]['display'])
        care_team_df.loc[len(care_team_df.index)] = [data['id'], data['status'], data['subject']['reference'], data['encounter']['reference'], data['period']['start'], period_end, reason_code_list , reason_code_name, data['managingOrganization'][0]['display']]
    except Exception as e:
        print("An exception occured in get_care_team:- " + str(e))


# To get image study details
def get_imaging_study(data):
    try:
        imaging_study_df.loc[len(imaging_study_df.index)] = [data['id'], data['identifier'][0]['system'], data['identifier'][0]['value'], data['status'], data['subject']['reference'], data['encounter']['reference'], data['started'], data['numberOfSeries'],data['numberOfInstances'], data['procedureCode'][0]['coding'][0]['code'], data['procedureCode'][0]['coding'][0]['display'], data['location']['display']]
        for series in data['series']:
            imaging_study_series_df.loc[len(imaging_study_series_df.index)] = [data['id'], series['uid'], series['number'], series['modality']['code'], series['modality']['display'], series['numberOfInstances'], series['bodySite']['code'], series['bodySite']['display'], series['started']]
            for instance in series['instance']:
                imaging_study_instances_df.loc[len(imaging_study_instances_df.index)] = [data['id'], instance['uid'], instance['sopClass']['code'], instance['number'], instance['title']]
    except Exception as e:
        print("An exception occured in get_imaging_study:- " + str(e))


# To get allergy intolerance details
def get_allergy_intolerance(data):
    try:
        allergy_intolerance_df.loc[len(allergy_intolerance_df.index)] = [data['id'], data['clinicalStatus']['coding'][0]['code'], data['verificationStatus']['coding'][0]['code'], data['type'], data['category'][0], data['criticality'], data['code']['coding'][0]['code'], data['code']['coding'][0]['display'], data['patient']['reference'], data['recordedDate']]
    except Exception as e:
        print("An exception occured in get_allergy_intolerance:- " + str(e))


# To get encounter details
def get_encounter(data):
    try:
        encounter_df.loc[len(encounter_df.index)] = [data['id'], data['identifier'][0]['value'], data['status'], data['class']['code'], data['type'][0]['coding'][0]['code'], data['type'][0]['coding'][0]['display'], data['subject']['reference'],data['subject']['display'], data['participant'][0]['type'][0]['coding'][0]['code'], data['participant'][0]['type'][0]['coding'][0]['display'], data['participant'][0]['period']['start'], data['participant'][0]['period']['end'], data['participant'][0]['individual']['display'], data['period']['start'], data['period']['end'], data['location'][0]['location']['display'], data['serviceProvider']['display']]
    except Exception as e:
        print("An exception occured in get_encounter:- " + str(e))


# To get condition details
def get_condition(data):
    try:
        if 'abatementDateTime' in data:
            abatement_datetime = data['abatementDateTime']
        else:
            abatement_datetime = ""
        condition_df.loc[len(condition_df.index)] = [data['id'], data['clinicalStatus']['coding'][0]['code'], data['verificationStatus']['coding'][0]['code'], data['category'][0]['coding'][0]['code'], data['code']['coding'][0]['code'], data['code']['coding'][0]['display'], data['subject']['reference'], data['encounter']['reference'], data['onsetDateTime'], abatement_datetime, data['recordedDate']]
    except Exception as e:
        print("An exception occured in get_condition:- " + str(e))


# To get medication request details
def get_medication_request(data):
    try:
        reason_reference = ""
        medication_code_able_concept_code = []
        medication_code_able_concept_name = []
        if 'medicationCodeableConcept' in data:
            for medication_code_able_concept in data['medicationCodeableConcept']['coding']:
                medication_code_able_concept_code.append(medication_code_able_concept['code'])
                medication_code_able_concept_name.append(medication_code_able_concept['display'])
        if 'reasonReference' in data:
            reason_reference = data['reasonReference'][0]['reference']
        medication_request_df.loc[len(medication_request_df.index)] = [data['id'], data['status'], data['intent'], medication_code_able_concept_code, medication_code_able_concept_name, data['subject']['reference'], data['encounter']['reference'], data['authoredOn'], data['requester']['display'], reason_reference]
        if 'dosageInstruction' in data:
            for dosage_instruction in data['dosageInstruction']:
                frequency = ""
                period = ""
                period_unit = ""
                dosage_instruction_text = ""
                dose_code = ""
                dose_name = ""
                dose_quantity = ""
                if 'timing' in dosage_instruction:
                    frequency = dosage_instruction['timing']['repeat']['frequency']
                    period = dosage_instruction['timing']['repeat']['period']
                    period_unit = dosage_instruction['timing']['repeat']['periodUnit']
                else:
                    dosage_instruction_text = dosage_instruction['text']
                if dosage_instruction['asNeededBoolean'] == False:
                    for doseandrate in dosage_instruction['doseAndRate']:
                        dose_code = doseandrate['type']['coding'][0]['code']
                        dose_name = doseandrate['type']['coding'][0]['display']
                        dose_quantity = doseandrate['doseQuantity']['value']
                medication_request_dosage_instruction_df.loc[len(medication_request_dosage_instruction_df.index)] = [data['id'], dosage_instruction['sequence'], frequency, period, period_unit, dosage_instruction_text, dosage_instruction['asNeededBoolean'], dose_code, dose_name, dose_quantity]
    except Exception as e:
        print("An exception occured in get_medication_request:- " + str(e))


# To get claim details
def get_claim(data):
    try:
        facility = ""
        patient_name = ""
        procedure_sequence = ""
        encounter = ""
        value = ""
        currency = ""
        sequence = []
        procedure_reference = []
        if 'display' in data['patient']:
            patient_name = data['patient']['display']
        if 'facility' in data:
            facility = data['facility']['display']
        if 'procedure' in data:
            for procedure in data['procedure']:
                sequence.append(procedure['sequence'])
                procedure_reference.append(procedure['procedureReference']['reference'])
        for item in data['item']:
            if 'procedureSequence' in item:
                procedure_sequence = item['procedureSequence'][0]
            if 'encounter' in item:
                encounter = item['encounter'][0]['reference']
            if 'net' in item:
                value = item['net']['value']
                currency = item['net']['currency']
            claim_item_df.loc[len(claim_item_df.index)] = [data['id'], item['sequence'], procedure_sequence, item['productOrService']['coding'][0]['code'], item['productOrService']['coding'][0]['display'], encounter, value, currency]
        claim_df.loc[len(claim_df.index)] = [data['id'], data['status'], data['type']['coding'][0]['code'], data['use'], data['patient']['reference'], patient_name,data['billablePeriod']['start'], data['billablePeriod']['end'], data['created'], data['provider']['display'], data['priority']['coding'][0]['code'], facility, sequence, procedure_reference, data['insurance'][0]['sequence'] ,data['insurance'][0]['focal'], data['insurance'][0]['coverage']['display'], data['total']['value'], data['total']['currency']]
    except Exception as e:
        print("An exception occured in get_claim:- " + str(e))


# To get observation details
def get_observation(data):
    try:
        value = ""
        quantity = ""
        category_name, observation_code, obervation_name, value_code_able_concept_code, value_code_able_concept_name = ( [] for i in range(5))
        for i, category in enumerate(data['category']):
            category_name.append(category['coding'][i]['code'])
        for code in data['code']['coding']:
            observation_code.append(code['code'])
            obervation_name.append(code['display'])
        if 'valueQuantity' in data:
            value = data['valueQuantity']['value']
            quantity = data['valueQuantity']['unit']
        if 'valueCodeableConcept' in data:
            for code in data['valueCodeableConcept']['coding']:
                value_code_able_concept_code.append(code['code'])
                value_code_able_concept_name.append(code['display'])
        observation_df.loc[len(observation_df.index)] = [data['id'], data['status'], category_name, observation_code, obervation_name, data['subject']['reference'], data['encounter']['reference'], data['effectiveDateTime'], data['issued'], value, quantity, value_code_able_concept_code, value_code_able_concept_name]
        if 'component' in data:
            for component in data['component']:
                component_value = ""
                component_unit = ""
                component_code = ""
                component_name = ""
                if 'valueQuantity' in data['component']:
                    component_value = component['valueQuantity']['value']
                    component_unit = component['valueQuantity']['unit']
                if 'valueCodeableConcept' in data['component']:
                    component_code = component['valueCodeableConcept']['coding'][0]['code']
                    component_name = component['valueCodeableConcept']['coding'][0]['display']
                observation_component_df.loc[len(observation_component_df.index)] = [data['id'], component['code']['coding'][0]['code'], component['code']['coding'][0]['display'], component_value, component_unit, component_code, component_name]
    except Exception as e:
        print("An exception occured in get_observation:- " + str(e))


# To get immunization details
def get_immunization(data):
    try:
        immunization_df.loc[len(immunization_df.index)] = [data['id'], data['status'], data['patient']['reference'], data['encounter']['reference'], data['occurrenceDateTime'], data['primarySource'], data['location']['display']]
        for vaccine_code in data['vaccineCode']['coding']:
            immunization_vaccine_code_df.loc[len(immunization_vaccine_code_df.index)] = [data['id'], vaccine_code['code'], vaccine_code['display']]
    except Exception as e:
        print("An exception occured in get_immunization:- " + str(e))


# To get care plan details
def get_care_plan(data):
    try:
        end = ""
        address = ""
        category_code = []
        category_name = []
        if 'end' in data['period']:
            end = data['period']['end']

        for category in data['category']:
            category_code.append(category['coding'][0]['code'])
            if 'display' in category['coding'][0]:
                category_name.append(category['coding'][0]['display'])
            else:
                category_name.append(" ")
        if 'addresses' in data:
           address = data['addresses'][0]['reference']
        care_plan_df.loc[len(care_plan_df.index)] = [data['id'], data['status'], data['intent'], category_code, category_name, data['subject']['reference'], data['encounter']['reference'], data['period']['start'], end, data['careTeam'][0]['reference'], address]
        if 'activity' in data:
            for activity in data['activity']:
                care_plan_activity_df.loc[len(care_plan_activity_df.index)] = [data['id'], activity['detail']['code']['coding'][0]['code'], activity['detail']['code']['coding'][0]['display'], activity['detail']['status'], activity['detail']['location']['display']]
    except Exception as e:
        print("An exception occured in get_care_plan:- " + str(e))


# To get medication administration details
def get_medication_administration(data):
    try:
        if 'reasonReference' in data:
            reason_reference = data['reasonReference'][0]['reference']
        else:
            reason_reference = ""
        medication_administration_df.loc[len(medication_administration_df.index)] = [data['id'], data['status'], data['medicationCodeableConcept']['coding'][0]['code'], data['medicationCodeableConcept']['coding'][0]['display'], data['subject']['reference'], data['context']['reference'], data['effectiveDateTime'], reason_reference]
    except Exception as e:
        print("An exception occured in get_medication_administration:- " + str(e))


# To get the get_device details
def get_device(data):
    try:
        device_df.loc[len(device_df.index)] = [data['id'], data['udiCarrier'][0]['deviceIdentifier'], data['udiCarrier'][0]['carrierHRF'], data['status'], data['distinctIdentifier'], data['manufactureDate'], data['expirationDate'], data['lotNumber'], data['serialNumber'], data['deviceName'][0]['name'], data['type']['coding'][0]['code'], data['patient']['reference']]
    except Exception as e:
        print("An exception occured in get_device:- " + str(e))


# To get the patient details
def get_patient(data):
    try:
        patient_core, patient_value, identifier_code, identifier_name, identifier_no = ([] for i in range(5))
        for extension in data['extension']:
            if 'extension' in extension:
                patient_core.append(extension['extension'][0]['valueCoding']['code'])
                patient_value.append(extension['extension'][0]['valueCoding']['display'])
        for i,identifier in enumerate(data['identifier']):
            if 'type' in identifier:
                identifier_code.append(identifier['type']['coding'][0]['code'])
                identifier_name.append(identifier['type']['coding'][0]['display'])
            if i != 0:
                identifier_no.append(identifier['value'])
        name = str(data['name'][0]['given'][0]) + str(data['name'][0]['family'])
        patient_df.loc[len(patient_df.index)] = [data['id'], patient_core, patient_value, data['extension'][2]['valueString'], data['extension'][3]['valueCode'], data['extension'][4]['valueAddress']['city'], data['extension'][4]['valueAddress']['state'], data['extension'][4]['valueAddress']['country'], data['extension'][5]['valueDecimal'], data['extension'][6]['valueDecimal'], identifier_code, identifier_name, identifier_no, name, data['telecom'][0]['use'], data['telecom'][0]['value'], data['gender'], data['birthDate'], data['address'][0]['line'][0], data['address'][0]['city'], data['address'][0]['state'], data['address'][0]['country'], data['maritalStatus']['coding'][0]['code'], data['communication'][0]['language']['coding'][0]['code']]
    except Exception as e:
        print("An exception occured in get_patient:- " + str(e))


def read_json_data(files, dir_location):
    try:
        print("Extracting data...")
        # To read the json file one by one
        for file in files:
            f = open(dir_location+file, encoding="utf8")
            data_format = json.load(f)
            for data in data_format['entry']:
                if data['resource']['resourceType'] == 'Patient':
                    get_patient(data['resource'])
                elif data['resource']['resourceType'] == 'Device':
                    get_device(data['resource'])
                elif data['resource']['resourceType'] == 'MedicationAdministration':
                    get_medication_administration(data['resource'])
                elif data['resource']['resourceType'] == 'CarePlan':
                    get_care_plan(data['resource'])
                elif data['resource']['resourceType'] == 'Immunization':
                    get_immunization(data['resource'])
                elif data['resource']['resourceType'] == 'Observation':
                    get_observation(data['resource'])
                elif data['resource']['resourceType'] == 'Claim':
                    get_claim(data['resource'])
                elif data['resource']['resourceType'] == 'MedicationRequest':
                    get_medication_request(data['resource'])
                elif data['resource']['resourceType'] == 'Condition':
                    get_condition(data['resource'])
                elif data['resource']['resourceType'] == 'Encounter':
                    get_encounter(data['resource'])
                elif data['resource']['resourceType'] == 'AllergyIntolerance':
                    get_allergy_intolerance(data['resource'])
                elif data['resource']['resourceType'] == 'CareTeam':
                    get_care_team(data['resource'])
                elif data['resource']['resourceType'] == 'Provenance':
                    get_provenance(data['resource'])
                elif data['resource']['resourceType'] == 'DocumentReference':
                    get_document_reference(data['resource'])
                elif data['resource']['resourceType'] == 'SupplyDelivery':
                    get_supply_delivery(data['resource'])
                elif data['resource']['resourceType'] == 'ExplanationOfBenefit':
                    get_explanation_of_benefit(data['resource'])
                elif data['resource']['resourceType'] == 'DiagnosticReport':
                    get_diagnostic_report(data['resource'])
                elif data['resource']['resourceType'] == 'Medication':
                    get_medication(data['resource'])
                elif data['resource']['resourceType'] == 'ImagingStudy':
                    get_imaging_study(data['resource'])
                else:
                    get_procedure(data['resource'])
            f.close()
        output_location = os.path.dirname(__file__) + r"\\output\\"
        # To write csv file
        print("Writing data to CSV file...")
        procedure_df.to_csv(output_location+'procedure.csv', sep=',', encoding='utf-8',index=False)
        medication_df.to_csv(output_location+'medication.csv', sep=',', encoding='utf-8',index=False)
        diagnostic_report_df.to_csv(output_location+'diagnostic_report.csv', sep=',', encoding='utf-8',index=False)
        diagnostic_report_result_df.to_csv(output_location+'diagnostic_report_result.csv', sep=',', encoding='utf-8',index=False)
        supply_delivery_df.to_csv(output_location+'supply_delivery.csv', sep=',', encoding='utf-8',index=False)
        device_df.to_csv(output_location+'device.csv', sep=',', encoding='utf-8',index=False)
        medication_administration_df.to_csv(output_location+'medication_administration.csv', sep=',', encoding='utf-8',index=False)
        immunization_df.to_csv(output_location+'immunization.csv', sep=',', encoding='utf-8',index=False)
        immunization_vaccine_code_df.to_csv(output_location+'immunization_vaccine_code.csv', sep=',', encoding='utf-8',index=False)
        allergy_intolerance_df.to_csv(output_location+'allergy_intolerance.csv', sep=',', encoding='utf-8',index=False)
        encounter_df.to_csv(output_location+'encountert.csv', sep=',', encoding='utf-8',index=False)
        condition_df.to_csv(output_location+'condition.csv', sep=',', encoding='utf-8',index=False)
        provenance_df.to_csv(output_location+'provenance.csv', sep=',', encoding='utf-8',index=False)
        provenance_participant_df.to_csv(output_location+'provenance_participant.csv', sep=',', encoding='utf-8',index=False)
        care_team_df.to_csv(output_location+'care_team.csv', sep=',', encoding='utf-8',index=False)
        care_team_participant_df.to_csv(output_location+'care_team_participant.csv', sep=',', encoding='utf-8',index=False)
        imaging_study_df.to_csv(output_location+'imaging_study.csv', sep=',', encoding='utf-8',index=False)
        imaging_study_series_df.to_csv(output_location+'imaging_study_series.csv', sep=',', encoding='utf-8',index=False)
        imaging_study_instances_df.to_csv(output_location+'imaging_study_instances.csv', sep=',', encoding='utf-8',index=False)
        care_plan_df.to_csv(output_location+'care_plan.csv', sep=',', encoding='utf-8',index=False)
        care_plan_activity_df.to_csv(output_location+'care_plan_activity.csv', sep=',', encoding='utf-8',index=False)
        document_reference_df.to_csv(output_location+'document_reference.csv', sep=',', encoding='utf-8',index=False)
        document_reference_file_df.to_csv(output_location+'document_reference_file.csv', sep=',', encoding='utf-8')
        claim_df.to_csv(output_location+'claim.csv', sep=',', encoding='utf-8',index=False)
        claim_item_df.to_csv(output_location+'claim_item.csv', sep=',', encoding='utf-8',index=False)
        medication_request_df.to_csv(output_location+'medication_request.csv', sep=',', encoding='utf-8',index=False)
        medication_request_dosage_instruction_df.to_csv(output_location+'medication_request_dosage_instruction.csv', sep=',', encoding='utf-8',index=False)
        observation_df.to_csv(output_location+'observation.csv', sep=',', encoding='utf-8',index=False)
        observation_component_df.to_csv(output_location+'observation_component.csv', sep=',', encoding='utf-8',index=False)
        explanation_of_benefit_df.to_csv(output_location+'explanation_of_benefit.csv', sep=',', encoding='utf-8',index=False)
        explanation_of_benefit_item_df.to_csv(output_location+'explanation_of_benefit_item.csv', sep=',', encoding='utf-8',index=False)
        explanation_of_benefit_adjudication_df.to_csv(output_location+'explanation_of_benefit_adjudication.csv', sep=',', encoding='utf-8',index=False)
        patient_df.to_csv(output_location+'patient.csv', sep=',', encoding='utf-8',index=False)
        print("Execution complete.")
    except Exception as e:
        print("An exception occured in read_json_data:- " + str(e))


# Main func
if __name__ == "__main__":
    try:
        print("Execution started....")
        config = configparser.ConfigParser()
        config.read('config.ini')
        # Data frame
        print("Creating Dataframe....")
        procedure_cols = ast.literal_eval(config.get("data_category", "Procedure"))
        procedure_df = pd.DataFrame(columns=procedure_cols)
        medication_cols = ast.literal_eval(config.get("data_category", "Medication"))
        medication_df = pd.DataFrame(columns=medication_cols)
        diagnostic_report_cols = ast.literal_eval(config.get("data_category", "DiagnosticReport"))
        diagnostic_report_df = pd.DataFrame(columns=diagnostic_report_cols)
        diagnostic_report_result_cols = ast.literal_eval(config.get("data_category", "DiagnosticReportResult"))
        diagnostic_report_result_df = pd.DataFrame(columns=diagnostic_report_result_cols)
        supply_delivery_cols = ast.literal_eval(config.get("data_category", "SupplyDelivery"))
        supply_delivery_df = pd.DataFrame(columns=supply_delivery_cols)
        device_cols = ast.literal_eval(config.get("data_category", "Device"))
        device_df = pd.DataFrame(columns=device_cols)
        medication_administration_cols = ast.literal_eval(config.get("data_category", "MedicationAdministration"))
        medication_administration_df = pd.DataFrame(columns=medication_administration_cols)
        immunization_cols = ast.literal_eval(config.get("data_category", "Immunization"))
        immunization_df = pd.DataFrame(columns=immunization_cols)
        immunization_vaccine_code_cols = ast.literal_eval(config.get("data_category", "Immunization_vaccineCode"))
        immunization_vaccine_code_df = pd.DataFrame(columns=immunization_vaccine_code_cols)
        allergy_intolerance_cols = ast.literal_eval(config.get("data_category", "AllergyIntolerance"))
        allergy_intolerance_df = pd.DataFrame(columns=allergy_intolerance_cols)
        encounter_cols = ast.literal_eval(config.get("data_category", "Encounter"))
        encounter_df = pd.DataFrame(columns=encounter_cols)
        condition_cols = ast.literal_eval(config.get("data_category", "Condition"))
        condition_df = pd.DataFrame(columns=condition_cols)
        provenance_cols = ast.literal_eval(config.get("data_category", "Provenance"))
        provenance_df = pd.DataFrame(columns=provenance_cols)
        provenance_participant_cols = ast.literal_eval(config.get("data_category", "Provenance_participant"))
        provenance_participant_df = pd.DataFrame(columns=provenance_participant_cols)
        care_team_cols = ast.literal_eval(config.get("data_category", "CareTeam"))
        care_team_df = pd.DataFrame(columns=care_team_cols)
        care_team_participant_cols = ast.literal_eval(config.get("data_category", "CareTeam_Participant"))
        care_team_participant_df = pd.DataFrame(columns=care_team_participant_cols)
        imaging_study_cols = ast.literal_eval(config.get("data_category", "ImagingStudy"))
        imaging_study_df = pd.DataFrame(columns=imaging_study_cols)
        imagingStudy_series_cols = ast.literal_eval(config.get("data_category", "ImagingStudy_series"))
        imaging_study_series_df = pd.DataFrame(columns=imagingStudy_series_cols)
        imaging_study_instances_cols = ast.literal_eval(config.get("data_category", "ImagingStudy_instances"))
        imaging_study_instances_df = pd.DataFrame(columns=imaging_study_instances_cols)
        care_plan_cols = ast.literal_eval(config.get("data_category", "CarePlan"))
        care_plan_df = pd.DataFrame(columns=care_plan_cols)
        care_plan_activity_cols = ast.literal_eval(config.get("data_category", "CarePlan_activity"))
        care_plan_activity_df = pd.DataFrame(columns=care_plan_activity_cols)
        document_reference_cols = ast.literal_eval(config.get("data_category", "DocumentReference"))
        document_reference_df = pd.DataFrame(columns=document_reference_cols)
        document_reference_file_cols = ast.literal_eval(config.get("data_category", "DocumentReference_file"))
        document_reference_file_df = pd.DataFrame(columns=document_reference_file_cols)
        claim_cols = ast.literal_eval(config.get("data_category", "Claim"))
        claim_df = pd.DataFrame(columns=claim_cols)
        claim_item_cols = ast.literal_eval(config.get("data_category", "Claim_item"))
        claim_item_df = pd.DataFrame(columns=claim_item_cols)
        medication_request_cols = ast.literal_eval(config.get("data_category", "MedicationRequest"))
        medication_request_df = pd.DataFrame(columns=medication_request_cols)
        medication_request_dosage_instruction_cols = ast.literal_eval(config.get("data_category", "MedicationRequest_dosage_instruction"))
        medication_request_dosage_instruction_df = pd.DataFrame(columns=medication_request_dosage_instruction_cols)
        observation_cols = ast.literal_eval(config.get("data_category", "Observation"))
        observation_df = pd.DataFrame(columns=observation_cols)
        observation_component_cols = ast.literal_eval(config.get("data_category", "Observation_component"))
        observation_component_df = pd.DataFrame(columns=observation_component_cols)
        explanation_of_benefit_cols = ast.literal_eval(config.get("data_category", "ExplanationOfBenefit"))
        explanation_of_benefit_df = pd.DataFrame(columns=explanation_of_benefit_cols)
        explanation_of_benefit_item_cols = ast.literal_eval(config.get("data_category", "ExplanationOfBenefit_item"))
        explanation_of_benefit_item_df = pd.DataFrame(columns=explanation_of_benefit_item_cols)
        explanation_of_benefit_adjudication_cols = ast.literal_eval(config.get("data_category", "ExplanationOfBenefit_adjudication"))
        explanation_of_benefit_adjudication_df = pd.DataFrame(columns=explanation_of_benefit_adjudication_cols)
        patient_cols = ast.literal_eval(config.get("data_category", "Patient"))
        patient_df = pd.DataFrame(columns=patient_cols)
        # Load the json files
        dir_location = os.path.dirname(__file__)+r"\\data\\"
        isdir = os.path.isdir(dir_location)
        if isdir == True:
            file = os.listdir(dir_location)  
            if len(file) > 0:
                read_json_data(file, dir_location)
            else:
                print("There is no file: " + str(dir_location))
        else:
            print("The directory is not exists: " + str(dir_location))
    except Exception as e:
        print("An exception occured in main func:- " + str(e))
