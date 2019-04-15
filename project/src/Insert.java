import java.io.File;
import java.io.FileNotFoundException;
import java.sql.*;
import java.util.*;

public class Insert {

    private static final String JDBC_DRIVER = "com.mysql.cj.jdbc.Driver";
    private static final String TIMEZONE_THING = "?useUnicode=true&useJDBCCompliantTimezoneShift=true&useLegacyDatetimeCode=false&serverTimezone=UTC";
    private static final String DB = "admin_portal";
    private static final String DB_URL = "jdbc:mysql://localhost/" + DB + TIMEZONE_THING;
    private static final String USER = "root";
    private static final String PASSWORD = "password123";

    static Map<Integer, String> admissionTypeMap = new HashMap<>();

    public static void main(String[] args) {

        Connection conn = createConnection();
        /*
         insertBasicEntities(conn, "important_mappings.csv");
         insertICDCodes(conn, "icd9codes.csv");
         insertMeds(conn, "dataset.csv");
         */

        insertEntities(conn, "dataset.csv");
    }
    private static void insertBasicEntities(Connection conn, String file) {
        List<List<String>> mappings = readCSV(file);
        for(int i = 0; i < mappings.size(); i++) {
            if(i < 8) {
                admissionTypeMap.put(Integer.parseInt(mappings.get(i).get(0)),  mappings.get(i).get(1));
            } else if(i > 8 && i < 39) {
                // discharge name too long
                addDischarge(conn, Integer.parseInt(mappings.get(i).get(0)), mappings.get(i).get(1));
            } else if(i > 39 && i < 66) {
                addSource(conn, Integer.parseInt(mappings.get(i).get(0)), mappings.get(i).get(1));
            }
        }
    }
    private static void insertICDCodes(Connection conn, String file) {
        List<List<String>> icdCodes = readCSV(file);
        System.out.println(icdCodes.size());
        for(int i = 1; i < icdCodes.size(); i++) {
            System.out.println(icdCodes.get(i).toString());
            addDiagnosis(conn, icdCodes.get(i).get(0), icdCodes.get(i).get(1));
        }
    }
    private static void insertMeds(Connection conn, String file) {
        List<String> header = getHeader(file);
        for(int i = 22; i < header.size() - 3; i++) {
            addMedication(conn, header.get(i));
        }
    }
    private static void insertEntities(Connection conn, String file) {
        List<List<String>> records = readCSV(file);
        List<String> header = getHeader(file);
        for (List<String> record : records) {

            /*
            We first must check if the current patient_id has
            not already been added into the database table. Our CSV
            file only has unique Encounter entities.
            */


            int patient_id = Integer.parseInt(record.get(1));
            String race = record.get(2);
            String gender = record.get(3);
            String payer_code = record.get(9);
            boolean exists = isPatientAlreadyInDB(conn, patient_id);
            if (!exists) {
                addPatient(conn, patient_id, race, gender, payer_code);
            }
            int encounter_id = Integer.parseInt(record.get(0));
            int lab_procedures = Integer.parseInt(record.get(11));
            int medications = Integer.parseInt(record.get(13));
            int admiss_type = Integer.parseInt(record.get(5));
            int duration = Integer.parseInt(record.get(8));
            String age = record.get(4);
            String readmitted = record.get(47);
            int discharge_id = Integer.parseInt(record.get(6));
            int source_id = Integer.parseInt(record.get(7));
            addEncounter(conn, encounter_id, lab_procedures, medications, admiss_type, duration, age, readmitted);
            addHas(conn, encounter_id, patient_id);
            addGetsPatientFrom(conn, encounter_id, source_id);
            addSendsPatientTo(conn, encounter_id, discharge_id);

            String change = record.get(45);

            if (!change.equals("No")) {
                for(int i = 22; i < header.size() - 3; i++) {
                    String med_change = record.get(i);
                    if (!med_change.equals("No")) {
                        String med_name = header.get(i);
                        addPrescribes(conn, encounter_id, med_name, med_change);
                    }
                }
            }

            // diagnoses doesn't work completely because the icd_codes don't match all the way
            // i.e. V08 vs V08. , 584 vs. 584.0, and other things. :(
            //
            for(int i = 1; i < 4; i++) {
                String icd = record.get(16 + i);
                if (!icd.equals("?")) {
                    addDiagnoses(conn, encounter_id, icd, i);
                }
            }
        }
    }
    private static boolean isPatientAlreadyInDB(Connection conn, int id) {
        PreparedStatement ps;
        String selectPatient = "SELECT patient_id " +
                "FROM Patient " +
                "WHERE patient_id = ?";
        boolean exists = true;
        try {
            ps = conn.prepareStatement(selectPatient);
            ps.setInt(1, id);
            ResultSet patients = ps.executeQuery();

            exists = patients.next();
            ps.close();
        } catch(SQLException e) {
            e.printStackTrace();
        }
        return exists;
    }
    private static void addSource(Connection conn, int source_id, String source_name) {
        PreparedStatement ps;
        String insertPatient = "Insert INTO Source" +
                "(source_id, source_name)" +
                "values (?,?)";
        try {
            ps = conn.prepareStatement(insertPatient);
            ps.setInt(1, source_id);
            ps.setString(2, source_name);
            ps.executeUpdate();
            ps.close();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
    private static void addDischarge(Connection conn, int discharge_id, String discharge_name) {
        PreparedStatement ps;
        String insertPatient = "Insert INTO Discharge" +
                "(discharge_id, discharge_name)" +
                "values (?,?)";
        try {
            ps = conn.prepareStatement(insertPatient);
            ps.setInt(1, discharge_id);
            ps.setString(2, discharge_name);
            ps.executeUpdate();
            ps.close();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
    private static void addPatient(Connection conn, int id, String race, String gender, String code) {
        PreparedStatement ps;
        String insertPatient = "Insert INTO Patient" +
                "(patient_id, race, gender, payer_code)" +
                "values (?,?,?,?)";
        try {
            ps = conn.prepareStatement(insertPatient);
            ps.setInt(1, id);
            ps.setString(2, race);
            ps.setString(3, gender);
            ps.setString(4, code);
            ps.executeUpdate();
            ps.close();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
    private static void addEncounter(Connection conn, int id, int procedures, int meds, int type, int days, String age, String readmitted) {
        PreparedStatement ps;
        try {
            String insertEncounter = "Insert INTO Encounter" +
                    "(encounter_id, num_lab_procedures, num_medications, admiss_type, duration, age, readmitted)" +
                    "values (?,?,?,?,?,?,?)";

            ps = conn.prepareStatement(insertEncounter);
            ps.setInt(1, id);
            ps.setInt(2, procedures);
            ps.setInt(3, meds);
            ps.setInt(4, type);
            ps.setInt(5, days);
            ps.setString(6, age);
            ps.setString(7, readmitted);
            ps.executeUpdate();
            ps.close();
        } catch(SQLException e) {
            e.printStackTrace();
        }
    }
    private static void addHas(Connection conn, int enc_id, int pat_id){
        PreparedStatement ps;
        try {
            String insertHas = "Insert INTO has" +
                    "(encounter_id, patient_id)" +
                    "values (?,?)";
            ps = conn.prepareStatement(insertHas);
            ps.setInt(1, enc_id);
            ps.setInt(2, pat_id);
            ps.executeUpdate();
            ps.close();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
    private static void addGetsPatientFrom(Connection conn, int id, int source_id){
        PreparedStatement ps;
        try {
            String insertGetsPatientFrom = "Insert INTO GetsPatientFrom" +
                    "(encounter_id, source_id)" +
                    "values (?,?)";
            ps = conn.prepareStatement(insertGetsPatientFrom);
            ps.setInt(1, id);
            ps.setInt(2, source_id);
            ps.executeUpdate();
            ps.close();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
    private static void addSendsPatientTo(Connection conn, int id, int discharge_id){
        PreparedStatement ps;
        try {
            String insertSendsPatientTo = "Insert INTO sendspatientto" +
                    "(encounter_id, discharge_id)" +
                    "values (?,?)";
            ps = conn.prepareStatement(insertSendsPatientTo);
            ps.setInt(1, id);
            ps.setInt(2, discharge_id);
            ps.executeUpdate();
            ps.close();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
    private static void addMedication(Connection conn, String med_name) {
        PreparedStatement ps;
        try {
            String insertMedication = "Insert INTO Medication" +
                    "(med_name)" +
                    "values (?)";
            ps = conn.prepareStatement(insertMedication);
            ps.setString(1, med_name);
            ps.executeUpdate();
            ps.close();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
    private static void addPrescribes(Connection conn, int id, String med_name, String dosage_change){
        PreparedStatement ps;
        try {
            String insertPrescribes = "Insert INTO Prescribes" +
                    "(encounter_id, med_name, dosage_change)" +
                    "values (?,?,?)";
            ps = conn.prepareStatement(insertPrescribes);
            ps.setInt(1, id);
            ps.setString(2, med_name);
            ps.setString(3, dosage_change);
            ps.executeUpdate();
            ps.close();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
    private static void addDiagnoses(Connection conn, int id, String icd_code, int priority){
        PreparedStatement ps;
        try {
            String insertDiagnoses = "Insert INTO Diagnoses" +
                    "(encounter_id, icd_code, priority)" +
                    "values (?,?,?)";
            ps = conn.prepareStatement(insertDiagnoses);
            ps.setInt(1, id);
            System.out.println(icd_code);
            ps.setString(2, icd_code);
            ps.setInt(3, priority);
            ps.executeUpdate();
            ps.close();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
    private static void addDiagnosis(Connection conn, String code, String description) {
        PreparedStatement ps;
        try {
            String insertDiagnoses = "Insert INTO Diagnosis" +
                    "(icd_code, diag_name)" +
                    "values (?,?)";
            ps = conn.prepareStatement(insertDiagnoses);
            ps.setString(1, code);
            ps.setString(2, description);
            ps.executeUpdate();
            ps.close();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
    private static Connection createConnection() {
        Connection conn;
        try {
            Class.forName(JDBC_DRIVER);
            conn = DriverManager.getConnection(DB_URL, USER, PASSWORD);
            return conn;
        } catch(SQLException e) {
            e.printStackTrace();
        } catch (ClassNotFoundException e) {
            e.printStackTrace();
        }
        return null;
    }
    private static List<List<String>> readCSV(String file) {
        List<List<String>> records = new ArrayList<List<String>>();
        try {
            Scanner scan = new Scanner(new File(file));
            String header = scan.nextLine();
            System.out.println(header);
            while(scan.hasNextLine()) {
                records.add(getRecordFromLine(scan.nextLine()));
            }
        } catch(FileNotFoundException e) {
            e.printStackTrace();
        }
        return records;
    }
    private static List<String> getHeader(String file){
        List<String> header = new ArrayList<String>();
        try {
            Scanner scan = new Scanner(new File(file));
            String headerStr = scan.nextLine();
            header = getRecordFromLine(headerStr);
        } catch (FileNotFoundException e){
            e.printStackTrace();
        }
        return header;
    }
    private static List<String> getRecordFromLine(String line) {
        List<String> values = new ArrayList<String>();
        Scanner rowScanner = new Scanner(line);
        rowScanner.useDelimiter(",");
        while (rowScanner.hasNext()) {
            values.add(rowScanner.next().replace("\"", ""));
        }
        return values;
    }
}