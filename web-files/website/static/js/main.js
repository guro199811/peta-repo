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

	// Re-add the newly sorted rows
	tBody.append(...sortedRows);

	// Remember how the column is currently sorted
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