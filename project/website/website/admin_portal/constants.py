token_name = "csrfmiddlewaretoken"
graph_key = "graphtype"

titles_options = ['Race', 'Gender', 'Age']
titles_dict = dict(zip(titles_options, [1,2,3]))
race_options = ['?','AfricanAmerican','Asian','Caucasian','Hispanic','Other']
gender_options = ['Male','Female','Other']
age_options = ['[0-10)','[10-20)','[20-30)','[30-40)','[40-50)','[50-60)','[60-70)','[70-80)','[80-90)','[90-100)']

encounter_fields = ['Encounter ID', 'Age', 'A1c Result', 'Glucose Result', '# of lab procedures',
                    '# of medications', 'Admission type', 'Duration (days)', 'Readmitted?',
                    'Diagnosis 1', 'Diagnosis 2', 'Diagnosis 3', 'Medication']

options_dict = {"Gender" : gender_options, "Race" : race_options, "Age": age_options}
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
