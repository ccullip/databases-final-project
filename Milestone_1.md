### Project Description
The project will involve a database of diabetic patient encounters in US hospitals from the years 1999-2008. The dataset includes information such as medications, diagnoses, vitals results, along with more generic data such as weight, age, race, and gender. The end product will be a mockup of an administration portal web page where the user can filter the data by selecting various attribute values. This will allow the “administrator” to see macroscopic patient data or, perhaps, view one hospital visit of a single patient. By filtering for specific results, the user will be able to see the data visualized and perhaps even find their own correlations within the dataset. 

### Data
The majority of the sample data has already been collected, which is represented in the ER diagram below. Although some rows have missing attributes, the construction of the database system ensures that these attributes will not be primary keys. Some entities still also need more info, such as the Diagnosis entity, which will need names of diagnoses assigned to ICD codes. This will be done by downloading a .csv spreadsheet of ICD-9 codes and their corresponding names, then using a program to populate the Diagnosis entity table. Additionally, more attributes for the Diagnosis and/or Medication entities may be added manually to make those tables larger and more interesting. Sample data can be viewed in the attached Excel spreadsheet. Ten instances have been chosen as a subset of the larger dataset which includes over 100,000 entries. 

### Assumptions
* Every patient must have at least one hospital visit.
* Physicians can facilitate multiple hospital visits.
* Diagnoses can be diagnosed by multiple physicians and physicians can diagnose multiple diagnoses (max. 3)
* A physician can prescribe many medications and each medication can be prescribed by many physicians.
* Although each physician can measure multiple vitals, they can only measure one set of vitals for each patient, so relationship is 1:1.
* Each set of vitals can be measured by only one physician.
* The specialty attribute of Physician can be null, but this is acceptable because it is a dependent of Encounter.
* The payer_code attribute can also be null.

### ER Diagram

<img src="ER_V7.png">

### Relation Schema
Patient(**patient_nbr**, race, payer_code, gender) <br>
Encounter(**encounter_id**, duration, height, readmitted, age, admiss_type, num_procedure)<br>
Diagnosis(**ICD_code**, diag_name) <br>
Medication(**med_name**) <br>
Vitals(**encounter_id**, A1c_result, glucose_result) <br>
Physician(**encounter_id**, specialty) <br>
Source(**source_id**, source_name) <br>
Discharge(**discharge_id**, discharge_name) <br>
measures(**encounter_id**) <br>
prescribes(**encounter_id**, **med_name**, dosage_change, new_prescript) <br>
facilitated_by(**encounter_id**) <br>
diagnoses(**encounter_id**, **ICD_code**, priority) <br>
has(**encounter_id**) <br>
gets_patient_from(**encounter_id**) <br>
sends_patient_to(**encounter_id**) <br>

### Application Description
The application will consist of an administration portal web page (created with vanilla HTML/CSS/JavaScript) where the user can make queries, such as finding all male patients who were 40-50 years old having the condition “Diabetes with peripheral circulatory disorders”. This will most likely be done by having the user select specific characteristics for which they wish to filter the data. For example, there would be drop-down menus, labelled “gender”, “race”, “weight”, “medication”, etc. where the user can click on one and select their desired option. So if they wished to filter results by gender, they would click the “gender” drop-down menu and then either “male”, “female”, or “other”. Also under consideration are features that can graph results or display the data in a more engaging user interaction than simply returning a table of the filtered data.

<a href="https://www.hindawi.com/journals/bmri/2014/781670/">Data Description</a>

Not used columns: num_lab_procedures num_procedures number_outpatient number_emergency number_inpatient, num_diagnoses, num_meds

