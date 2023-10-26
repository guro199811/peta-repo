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
//const speciesInput = document.getElementById(`species_${petId}`);
//const breedInput = document.getElementById(`breed_${petId}`);
const vaccinationInput = document.getElementById(`recent_vaccination_${petId}`);
const saveButton = document.getElementById(`save_${petId}`);

// Check if the inputs are already enabled
if ( nameInput.disabled == false || vaccinationInput.disabled == false) {
  nameInput.disabled = true;
  /*speciesInput.disabled = true;*/
  //breedInput.disabled = true;
  vaccinationInput.disabled = true;
  saveButton.style.display = "none";
  // Return early if already enabled
}
else{
  nameInput.disabled = false;
  /*speciesInput.disabled = false;*/
  //breedInput.disabled = false;
  vaccinationInput.disabled = false;
  saveButton.style.display = "block";
}}

// map code goes here





function initializeMap() {
  var map = L.map('map').setView([41.7151377, 44.827096], 8);
  L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
  }).addTo(map);

  map.locate({ setView: true, maxZoom: 16 });

  // Add a marker at the user's location
  function onLocationFound(e) {
    var radius = e.accuracy / 2;
    L.marker(e.latlng).addTo(map)
      .bindPopup("ჩემი ლოკაცია").openPopup();
    L.circle(e.latlng, radius).addTo(map);
  }

  map.on('locationfound', onLocationFound);
}


if (document.getElementById('map')) {
  initializeMap();
}

/* map for clinics */
function initializeClinicMap() {
  var map = L.map('clinic-map').setView([41.7151377, 44.827096], 8);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
  }).addTo(map);

  var marker;

  map.on('click', function(e) {
    if (marker) {
      map.removeLayer(marker);
    }
    marker = L.marker(e.latlng).addTo(map);
    document.getElementById('coordinates').value = e.latlng.lat + ',' + e.latlng.lng;
  });

  // Find My Location button
  var findMyLocationButton = L.easyButton('fa-map-marker', function() {
    map.locate({ setView: true, maxZoom: 16 });
  }).addTo(map);

  // Add a handler for location found
  map.on('locationfound', function(e) {
    // Center the map on the user's location
    map.setView(e.latlng, 16);


    // Add a circle to represent accuracy
    L.circle(e.latlng, {
      radius: e.accuracy / 2,
      fillColor: 'blue',
      fillOpacity: 0.2,
    }).addTo(map);
  });
}

if (document.getElementById('clinic-map')) {
  initializeClinicMap();
}



/**
 * Sorts a HTML table.
 *
 * @param {HTMLTableElement} table The table to sort
 * @param {number} column The index of the column to sort
 * @param {boolean} asc Determines if the sorting will be in ascending
 */
function sortTableByColumn(table, column, asc = true) {
const dirModifier = asc ? 1 : -1;
const tBody = table.tBodies[0];
const rows = Array.from(tBody.querySelectorAll("tr"));

// Sort each row
const sortedRows = rows.sort((a, b) => {
const aColText = a.querySelector(`td:nth-child(${column + 1})`).textContent.trim();
const bColText = b.querySelector(`td:nth-child(${column + 1})`).textContent.trim();

  return aColText > bColText ? (1 * dirModifier) : (-1 * dirModifier);
});

// Remove all existing TRs from the table
while (tBody.firstChild) {
  tBody.removeChild(tBody.firstChild);
}


tBody.append(...sortedRows);


table.querySelectorAll("th").forEach(th => th.classList.remove("th-sort-asc", "th-sort-desc"));
table.querySelector(`th:nth-child(${column + 1})`).classList.toggle("th-sort-asc", asc);
table.querySelector(`th:nth-child(${column + 1})`).classList.toggle("th-sort-desc", !asc);
}

document.querySelectorAll(".table-sortable th").forEach(headerCell => {
headerCell.addEventListener("click", () => {
  const tableElement = headerCell.parentElement.parentElement.parentElement;
  const headerIndex = Array.prototype.indexOf.call(headerCell.parentElement.children, headerCell);
  const currentIsAscending = headerCell.classList.contains("th-sort-asc");

  sortTableByColumn(tableElement, headerIndex, !currentIsAscending);
});
});


// getting pet breeds based on pet species
document.addEventListener('DOMContentLoaded', function() {
  // Function to fetch and populate the pet breeds dropdown
  function populatePetBreeds(species_id) {
      fetch('/get_pet_breeds', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify({
              species_id: species_id,
          }),
      })
      .then(response => response.json())
      .then(data => {
          // Clear the existing options
          const petBreedSelect = document.getElementById('pet_breed');
          petBreedSelect.innerHTML = '';

          // Add the new options based on the data received
          for (const breed of data) {
              const option = document.createElement('option');
              option.value = breed;
              option.textContent = breed;
              petBreedSelect.appendChild(option);
          }
      });
  }

  // Add an event listener to the species dropdown to trigger breed population
  const petSpeciesSelect = document.getElementById('pet_species');
  petSpeciesSelect.addEventListener('change', function() {
      const selectedSpeciesId = petSpeciesSelect.value;
      populatePetBreeds(selectedSpeciesId);
  });

  // Initialize the breeds dropdown based on the initial selected value (if any)
  const initialSelectedSpeciesId = petSpeciesSelect.value;
  populatePetBreeds(initialSelectedSpeciesId);
});


function enableEditNote(note_id){
  const commentTextarea = document.getElementById(`comment_${note_id}`);
  
  let isEditable = false;

  commentTextarea.disabled = !commentTextarea.disabled;

  if (!commentTextarea.disabled) {
    isEditable = true;
  }
  if (saveButton) {
    saveButton.disabled = !isEditable;
  }
}


function enableEditHistory(petId) {
  const treatmentSelect = document.getElementById(`treatment_${petId}`);
  const dateInput = document.getElementById(`date_${petId}`);
  const commentTextarea = document.getElementById(`comment_${petId}`);
  const saveButton = document.getElementById(`save_${petId}`);

  let isEditable = false;

  treatmentSelect.disabled = !treatmentSelect.disabled;
  dateInput.disabled = !dateInput.disabled;
  commentTextarea.disabled = !commentTextarea.disabled;

  if (!treatmentSelect.disabled || !dateInput.disabled || !commentTextarea.disabled) {
    isEditable = true;
  }

  if (saveButton) {
    saveButton.disabled = !isEditable;
  }
}

window.onload = function(){
  const sidebar = document.querySelector(".sidebar");
  const closeBtn = document.querySelector("#btn");
  const searchBtn = document.querySelector(".bx-search")

  closeBtn.addEventListener("click",function(){
      sidebar.classList.toggle("open")
      menuBtnChange()
  })

  searchBtn.addEventListener("click",function(){
      sidebar.classList.toggle("open")
      menuBtnChange()
  })

  function menuBtnChange(){
      if(sidebar.classList.contains("open")){
          closeBtn.classList.replace("bx-menu","bx-menu-alt-right")
      }else{
          closeBtn.classList.replace("bx-menu-alt-right","bx-menu")
      }
  }
}


//owner actions


function enableEditUser(user_id) {
const inputs = document.querySelectorAll(`#name_${user_id}, #lastname_${user_id},
 #mail_${user_id}, #type_${user_id}, #created_${user_id}, #address_${user_id},
 #phone_${user_id}`);
const saveButton = document.querySelector(`#save_${user_id}`);

let isEditable = false;

for (const input of inputs) {
  if (input.disabled) {
    input.disabled = false;
    isEditable = true;
  } else {
    input.disabled = true;
  }
}

if (saveButton) {
  if (isEditable) {
    saveButton.style = 'display: inline-block';
  } else {
    saveButton.style = 'display: none';
  }
}
}

const searchIcon = document.querySelector('.search i');
const searchForm = document.getElementById('search-form');

searchIcon.addEventListener('click', () => {
searchForm.classList.toggle('show-search');
});



