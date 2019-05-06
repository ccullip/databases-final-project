def createPreparedStatement(cursor, request_data):
    field_list = ['Patient Id', 'Race', 'Gender']
    keys = request_data.keys()
    values = []
    select_ps = "SELECT Patient.patient_id, Patient.race, Patient.gender"
    from_ps = "FROM Patient"
    where_ps = "WHERE "
    joins = {"Encounter": False,
             "Medication": False,
             "Vitals": False,
             "Source": False,
             "Discharge": False}
    for key in keys:
        if key != "csrfmiddlewaretoken":
            values.append(request_data.get(key))

        if key == "Gender":
            value = request_data.get(key)
            where_ps += "Patient.gender = '" + value + "'"
        elif key == "Race":
            value = request_data.get(key)
            if where_ps != "WHERE ":
                where_ps += " AND "
            where_ps += "Patient.race = '" + value + "'"
        elif key == "Age":
            value = request_data.get(key)
            field_list.append('Age')
            joins["Encounter"] = True
            # add to select statement
            select_ps += ", Encounter.age"
            # add to where statement
            if where_ps != "WHERE ":
                where_ps += " AND "
            where_ps += "Encounter.age = '" + value + "'"
        elif key == "Medication":
            value = request_data.get(key)
            field_list.append('Medication')
            joins["Encounter"] = True
            joins["Medication"] = True
            # add to select statement
            select_ps += ", Medication.med_name"
            # add to from statement
            if where_ps != "WHERE ":
                where_ps += " AND "
            where_ps += "Medication.med_name = '" + value + "'"
        elif key == "a1c_result":
            value = request_data.get(key)
            field_list.append("A1c Result")
            joins["Encounter"] = True
            joins["Vitals"] = True
            # add to select statement
            select_ps += ", Vitals.a1c_result"
            # add to from statement
            if where_ps != "WHERE ":
                where_ps += " AND "
            where_ps += "Vitals.a1c_result = '" + value + "'"
        elif key == "glucose_result":
            value = request_data.get(key)
            field_list.append("Glucose Result")
            joins["Encounter"] = True
            joins["Vitals"] = True
            # add to select statement
            select_ps += ", Vitals.glucose_result"
            # add to from statement
            if where_ps != "WHERE ":
                where_ps += " AND "
            where_ps += "Vitals.glucose_result = '" + value + "'"
        elif key == "source_id":
            value = request_data.get(key)
            field_list.append("Admission Source")
            joins["Encounter"] = True
            joins["Source"] = True
            # add to select statement
            select_ps += ", Source.source_name"
            # add to from statement
            if where_ps != "WHERE ":
                where_ps += " AND "
            where_ps += "Source.source_id = '" + value + "'"
        elif key == "discharge_id":
            value = request_data.get(key)
            field_list.append("Discharge Destination")
            joins["Encounter"] = True
            joins["Discharge"] = True
            # add to select statement
            select_ps += ", Discharge.discharge_name"
            # add to from statement
            if where_ps != "WHERE ":
                where_ps += " AND "
            where_ps += "Discharge.discharge_id = '" + value + "'"

    if joins["Encounter"]:
        from_ps += " natural join Has natural join Encounter"
    if joins["Medication"]:
        from_ps += " natural join Prescribes natural join Medication"
    if joins["Vitals"]:
        from_ps += " natural join Vitals"
    if joins["Source"]:
        from_ps += " natural join GetsPatientFrom natural join Source "
    if joins["Discharge"]:
        from_ps += " natural join SendsPatientTo natural join Discharge "

    ps = select_ps + " " + from_ps + " " + where_ps + ";"
    print(ps)
    cursor.execute(ps)
    return cursor.fetchall(), field_list, values
