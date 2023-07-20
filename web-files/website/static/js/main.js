//enable input script
function enableInput(inputId) {
    var inputField = document.getElementById(inputId);
    
    if (inputField.disabled == false) {
      inputField.disabled = true;
      inputField.select();
      document.getElementById('save-button').style.display = 'none';
    }
    else {
      inputField.disabled = false;
      inputField.focus();
      document.getElementById('save-button').style.display = 'block';
    } 
}

//editing pet script
function enableEdit(petId) {
  const nameInput = document.getElementById(`name_${petId}`);
  /*const speciesInput = document.getElementById(`species_${petId}`); */
  const breedInput = document.getElementById(`breed_${petId}`);
  const vaccinationInput = document.getElementById(`recent_vaccination_${petId}`);
  const saveButton = document.getElementById(`save_${petId}`);

  // Check if the inputs are already enabled
  if ( nameInput.disabled == false || breedInput.disabled == false || vaccinationInput.disabled == false) {
    nameInput.disabled = true;
    /*speciesInput.disabled = true;*/
    breedInput.disabled = true;
    vaccinationInput.disabled = true;
    saveButton.style.display = "none";
    // Return early if already enabled
  }
  else{
  nameInput.disabled = false;
  /*speciesInput.disabled = false;*/
  breedInput.disabled = false;
  vaccinationInput.disabled = false;
  saveButton.style.display = "block";
}}

//map script
var map = L.map('map').setView([51.505, -0.09], 13);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);
