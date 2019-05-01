function sendData(row){
    var patient_id = row.getElementsByTagName('td')[0].innerText;
    document.getElementById("patient-id").value = patient_id;
    console.log(document.getElementById("patient-id").value);
    form = document.getElementById("patient-form");
    form.submit();
};

function hidePopup() {
    document.getElementById("popup-container").style.visibility = "hidden";
    console.log("changed to hidden");
};
