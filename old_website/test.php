<?php
	$servername = "127.0.0.1";
	$username = "root";
	$password = "password123";
	$db = "admin_portal";

	// Create connection
	$conn = new mysqli($servername, $username, $password, $db);

	// Check connection
	if ($conn->connect_error) {
	    die("Connection failed: " . $conn->connect_error);
	}
	echo "Connected successfully \n";
	echo $db;
	echo "\n";
	$sql = "SELECT race, gender FROM Patient";
	$result = $conn->query($sql);

	if ($result->num_rows > 0) {
    // output data of each row
    while($row = $result->fetch_assoc()) {
        echo "race: " . $row["race"]. " - gender: " . $row["gender"]. " ". "<br>";
    }
} else {
    echo "0 results";
}
?>
<!-- ALTER USER 'mysqlUsername'@'localhost'
IDENTIFIED WITH mysql_native_password BY 'mysqlUsernamePassword';
 -->
