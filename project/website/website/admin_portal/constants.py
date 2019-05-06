token_name = "csrfmiddlewaretoken"

encounter_fields = ['Encounter ID', 'Age', 'A1c Result', 'Glucose Result', '# of lab procedures',
                    '# of medications', 'Admission type', 'Duration (days)', 'Readmitted?',
                    'Diagnosis 1', 'Diagnosis 2', 'Diagnosis 3', 'Medication']

pie_graphs = ["Gender", "Race", "Age"]

def createGiantPreparedStatement(patient_id):
    return "select encounter_id, age, a1c_result, glucose_result, num_lab_procedures, num_medications, admiss_type, duration, readmitted, " \
         "diag_1, diag_2, diag_3, " \
         "group_concat(Medicine SEPARATOR ', ') as Medicines " \
         "FROM (" \
         "SELECT encounter_id, age, a1c_result, glucose_result, num_lab_procedures, num_medications, admiss_type, duration, readmitted, " \
         "max(CASE WHEN priority = '1' THEN diag_name ELSE NULL END) as diag_1, " \
         "max(CASE WHEN priority = '2' THEN diag_name ELSE NULL END) as diag_2, " \
         "max(CASE WHEN priority = '3' THEN diag_name ELSE NULL END) as diag_3, " \
         "concat(med_name, ': ', dosage_change) as Medicine " \
         "FROM (SELECT encounter.encounter_id, icd_code, priority, diag_name, med_name, dosage_change, " \
         "age, a1c_result, glucose_result, num_lab_procedures, num_medications, admiss_type, duration, readmitted " \
         "FROM patient natural join has natural join encounter natural join diagnoses natural join diagnosis natural join vitals " \
         "LEFT JOIN prescribes on encounter.encounter_id = prescribes.encounter_id " \
         "WHERE patient_id = " + patient_id + ") as subsub " \
         "GROUP BY encounter_id) as sub " \
         "GROUP BY encounter_id;"
