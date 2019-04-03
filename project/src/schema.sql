CREATE DATABASE Records;
USE Records;

CREATE TABLE Patient (
patient_id INT NOT NULL,
race VARCHAR(30),
gender ENUM("Male", "Female"),
payer_code VARCHAR(30),
PRIMARY KEY (patient_id)
);

CREATE TABLE Encounter (
encounter_id INT NOT NULL,
num_procedure INT,
admiss_type INT,
duration ,
age ENUM("[0-10]", "[10-20]", "[20-30]", "[30-40]", "[40-50]", "[50-60]", "[60-70]", "[70-80]", "[80-90]", "[90-100]"),
readmitted ,
weight INT,
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
a1c_result ,
glucose_result ,
PRIMARY KEY (encounter_id),
FOREIGN KEY (encounter_id) REFERENCES Encounter(encounter_id)
);

CREATE TABLE Medication (
med_name VARCHAR (100) NOT NULL,
PRIMARY KEY (med_name)
);

CREATE TABLE Diagnosis (
icd_code VARCHAR (10) NOT NULL,
diag_name VARCHAR (300),
PRIMARY KEY (icd_code)
);

