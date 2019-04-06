import java.io.File;
import java.io.FileNotFoundException;
import java.sql.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class Insert {

    private static final String JDBC_DRIVER = "com.mysql.cj.jdbc.Driver";
    private static final String TIMEZONE_THING = "?useUnicode=true&useJDBCCompliantTimezoneShift=true&useLegacyDatetimeCode=false&serverTimezone=UTC";
    private static final String DB = "admin_portal";
    private static final String DB_URL = "jdbc:mysql://localhost/" + DB + TIMEZONE_THING;
    private static final String USER = "root";
    private static final String PASSWORD = "password123";

    public static void main(String[] args) {

        Connection conn = createConnection();
        insertEntities(conn, "dataset.csv");
    }

    private static void insertEntities(Connection conn, String file) {
        List<List<String>> records = readCSV(file);
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
            int medications = Integer.parseInt(record.get(12));
            int admiss_type = Integer.parseInt(record.get(5));
            int duration = Integer.parseInt(record.get(8));
            String age = record.get(4);
            String readmitted = record.get(47);

            addEncounter(conn, encounter_id, lab_procedures, medications, admiss_type, duration, age, readmitted);

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
