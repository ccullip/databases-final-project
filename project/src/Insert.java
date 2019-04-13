import java.io.File;
import java.io.FileNotFoundException;
import java.sql.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;
import java.math.BigDecimal;

public class Insert {

    private static final String JDBC_DRIVER = "com.mysql.cj.jdbc.Driver";
    private static final String TIMEZONE_THING = "?useUnicode=true&useJDBCCompliantTimezoneShift=true&useLegacyDatetimeCode=false&serverTimezone=UTC";
    private static final String DB = "admin_portal";
    private static final String DB_URL = "jdbc:mysql://localhost/" + DB; //+ TIMEZONE_THING;
    private static final String USER = "root";
    private static final String PASSWORD = "";

    public static void main(String[] args) {

        Connection conn = createConnection();
        insertEntities(conn, "../../dataset.csv");
    }

    private static void insertEntities(Connection conn, String file) {
        List<List<String>> records = readCSV(file);
        List<String> header = getHeader(file);
        for (List<String> record : records) {
            // patient attributes
            int patient_id = Integer.parseInt(record.get(1));
            String race = record.get(2);
            String gender = record.get(3);
            String payer_code = record.get(9);

            /*
            We first must check if the current patient_id has
            not already been added into the database table. Our CSV
            file only has unique Encounter entities.
            */

            boolean exists = isPatientAlreadyInDB(conn, patient_id);
            if (!exists) {
                addPatient(conn, patient_id, race, gender, payer_code);
            }

            // encounter attributes
            int encounter_id = Integer.parseInt(record.get(0));
            int lab_procedures = Integer.parseInt(record.get(11));
            int medications = Integer.parseInt(record.get(13));
            int admiss_type = Integer.parseInt(record.get(5));
            int duration = Integer.parseInt(record.get(8));
            String age = record.get(4);
            String readmitted = record.get(47);

            addEncounter(conn, encounter_id, lab_procedures, medications, admiss_type, duration, age, readmitted);

            // patient has encounter relationship
            addHas(conn, encounter_id, patient_id);

            // gets patient from relationship
            int source_id = Integer.parseInt(record.get(7));
            addGetsPatientFrom(conn, encounter_id, source_id);

            // sends patient to relationship
            int discharge_id = Integer.parseInt(record.get(6));
            addSendsPatientTo(conn, encounter_id, discharge_id);

            // prescribes relationship
            for (int i = 0; i < 23; i++){
                String med_name = header.get(23 + i);
                String dosage_change = record.get(23 + i);
                if (!dosage_change.equals("No")){
                    addPrescribes(conn, encounter_id, med_name, dosage_change);
                }
            }

            // diagnoses relationship
            for (int i = 1; i < 4; i++){
                String icd = record.get(16 + i);
                if (!icd.equals("?")){
                    BigDecimal icd_code = new BigDecimal(icd);
                    addDiagnoses(conn, encounter_id, icd_code, i);
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
                    "(encounter_id, pat_id)" +
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
            String insertGetsPatientFrom = "Insert INTO getspatientfrom" +
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
    private static void addPrescribes(Connection conn, int id, String med_name, String dosage_change){
        PreparedStatement ps;
        try {
            String insertPrescribes = "Insert INTO prescribes" +
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
    private static void addDiagnoses(Connection conn, int id, BigDecimal icd_code, int priority){
        PreparedStatement ps;
        try {
            String insertDiagnoses = "Insert INTO diagnoses" +
                    "(encounter_id, icd_code, priority)" +
                    "values (?,?,?)";
            ps = conn.prepareStatement(insertDiagnoses);
            ps.setInt(1, id);
            ps.setBigDecimal(2, icd_code);
            ps.setInt(3, priority);
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
