CREATE DATABASE Records;
USE Records;

CREATE TABLE Patient (
patient_id INT NOT NULL,
race VARCHAR(30), -- change to ENUM
gender ENUM("Male", "Female", "Other"),
payer_code ENUM("?", "BC", "CH", "CM","CP", "DM", "FR", "HM", "MC", "MD", "MP", "OG", "OT", "PO", "SI", "SP", "UN", "WC"),
PRIMARY KEY (patient_id)
);

CREATE TABLE Encounter (
encounter_id INT NOT NULL,
num_procedure INT,
admiss_type INT,
duration TINYINT, --num_days in hospital
age ENUM("[0-10]", "[10-20]", "[20-30]", "[30-40]", "[40-50]", "[50-60]", "[60-70]", "[70-80]", "[80-90]", "[90-100]"),
readmitted ENUM,
PRIMARY KEY (encounter_id)
);

CREATE TABLE Source (
source_id INT NOT NULL,
source_name VARCHAR (100),
PRIMARY KEY (source_id)
);

CREATE TABLE Discharge (
discharge_id INT NOT NULL,
discharge_name VARCHAR (100),
PRIMARY KEY (discharge_id)
);

CREATE TABLE Physician (
encounter_id INT NOT NULL,
specialty VARCHAR (100),
PRIMARY KEY (encounter_id),
FOREIGN KEY (encounter_id) REFERENCES Encounter(encounter_id)
);

CREATE TABLE Vitals (
ecounter_id INT NOT NULL,
a1c_result ENUM(), -- > 7 > 8 None, norm
glucose_result ,
PRIMARY KEY (encounter_id),
FOREIGN KEY (encounter_id) REFERENCES Encounter(encounter_id)
);

CREATE TABLE Medication (
med_name VARCHAR (100) NOT NULL,
PRIMARY KEY (med_name)
);

CREATE TABLE Diagnosis (
icd_code DECIMAL(4,2) NOT NULL,
diag_name VARCHAR (300),
PRIMARY KEY (icd_code)
);

CREATE TABLE Has (
patient_id INT NOT NULL,
encounter_id INT NOT NULL,
PRIMARY KEY (encounter_id),
FOREIGN KEY (patient_id) REFERENCES Patient(patient_id),
FOREIGN KEY (encounter_id) REFERENCES Encounter(encounter_id)
);

CREATE TABLE GetsPatientFrom (
encounter_id INT NOT NULL,
source_id TINYINT NOT NULL,
PRIMARY KEY (encounter_id),
FOREIGN KEY (source_id) REFERENCES Source(source_id),
FOREIGN KEY (encounter_id) REFERENCES Encounter(encounter_id)
);

CREATE TABLE SendsPatientTo (
encounter_id INT NOT NULL,
discharge_id INT NOT NULL,
PRIMARY KEY (encounter_id),
FOREIGN KEY (encounter_id) REFERENCES Encounter(encounter_id),
FOREIGN KEY (discharge_id) REFERENCES Discharge(discharge_id)
);

CREATE TABLE Diagnoses (
encounter_id INT NOT NULL,
icd_code DECIMAL (4, 2) NOT NULL,
priority TINYINT
PRIMARY KEY (encounter_id, icd_code),
FOREIGN KEY (encounter_id) REFERENCES Encounter(encounter_id),
FOREIGN KEY (icd_code) REFERENCES Diagnosis(diag_name)
);

CREATE TABLE Prescribes (
encounter_id INT NOT NULL,
med_name VARCHAR (50) NOT NULL,
dosage_change ENUM("Up", "Down", "Steady", "No"),
PRIVATE KEY (encounter_id, med_name),
FOREIGN KEY (encounter_id) REFERENCES Encounter(encounter_id),
FOREIGN KEY (med_name) REFERENCES Medication(med_name)

)

