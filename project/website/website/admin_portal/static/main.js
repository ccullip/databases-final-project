function sendData(row){
    var patient_id = row.getElementsByTagName('td')[0].innerText;
    document.getElementById("patient-id").value = patient_id;
    console.log(document.getElementById("patient-id").value);
    form = document.getElementById("patient-form");
    form.submit();
};

function getSearchBarText(){
    var patient_id_text = document.getElementById("search-patient-id").value;
    console.log(patient_id_text);
    console.log("getSearchBarText");
    var patient_id = Number(patient_id_text);
    console.log(patient_id);
    if(isNaN(patient_id)){
      console.log("not a number!");
    } else {
      console.log("its a number!");
      console.log(patient_id);
      document.getElementById("select-specific-patient").value = patient_id;
      console.log(document.getElementById("select-specific-patient").value);
      if(document.getElementById("select-specific-patient").value != ['Default']) {
        form = document.getElementById("search-form");
        form.submit();
      }
    }
};

function hidePopup() {
    document.getElementById("popup-container").style.visibility = "hidden";
};
